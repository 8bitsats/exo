import aiohttp
import asyncio
from typing import Optional, Dict, List, Any
import json

class HeliusClient:
    def __init__(self, api_key: str, base_url: str = "https://mainnet.helius-rpc.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self._websocket: Optional[aiohttp.ClientWebSocketResponse] = None
        self._subscription_id: Optional[int] = None

    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self._websocket:
            await self._websocket.close()
        if self.session:
            await self.session.close()
            self.session = None

    async def get_transaction(self, signature: str) -> Dict:
        await self._ensure_session()
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {"encoding": "json", "maxSupportedTransactionVersion": 0}
            ]
        }
        async with self.session.post(f"{self.base_url}/?api-key={self.api_key}", json=payload) as response:
            return await response.json()

    async def subscribe_transactions(self, callback, filter_options: Optional[Dict] = None):
        await self._ensure_session()
        
        ws_url = f"wss://mainnet.helius-rpc.com/?api-key={self.api_key}"
        self._websocket = await self.session.ws_connect(ws_url)

        # Default subscription for all transactions
        subscribe_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "transactionSubscribe",
            "params": [
                {"commitment": "confirmed"},
                {"encoding": "json", "maxSupportedTransactionVersion": 0}
            ]
        }

        if filter_options:
            subscribe_msg["params"][0].update(filter_options)

        await self._websocket.send_str(json.dumps(subscribe_msg))
        subscription_response = await self._websocket.receive_json()
        self._subscription_id = subscription_response.get("result")

        try:
            async for msg in self._websocket:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if "params" in data:
                        await callback(data["params"])
                elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    break
        finally:
            if self._subscription_id:
                await self._unsubscribe()

    async def _unsubscribe(self):
        if self._websocket and self._subscription_id:
            unsubscribe_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "transactionUnsubscribe",
                "params": [self._subscription_id]
            }
            await self._websocket.send_str(json.dumps(unsubscribe_msg))
            self._subscription_id = None

    async def get_enhanced_transactions(self, signatures: List[str]) -> List[Dict]:
        await self._ensure_session()
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "enhancedTransactions",
            "params": [signatures]
        }
        async with self.session.post(f"{self.base_url}/?api-key={self.api_key}", json=payload) as response:
            result = await response.json()
            return result.get("result", [])
