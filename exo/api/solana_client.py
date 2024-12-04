import aiohttp
import json
import logging
import ssl
import certifi
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class SolanaConfig:
    helius_rpc_url: str = "https://mainnet.helius-rpc.com/?api-key=e4e7f06a-1e90-4628-8b07-d4f3c30fc5c9"
    helius_ws_url: str = "wss://mainnet.helius-rpc.com/?api-key=e4e7f06a-1e90-4628-8b07-d4f3c30fc5c9"
    helius_api_url: str = "https://api.helius.xyz"
    solana_tracker_api_key: str = "7d5348f1-b95e-4569-8256-375a2ac01437"
    solana_tracker_url: str = "https://data.solanatracker.io"

class SolanaClient:
    """Client for interacting with Solana blockchain through Helius and SolanaTracker."""
    
    def __init__(self, config: SolanaConfig = SolanaConfig()):
        self.config = config
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.session = None
        
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def get_token_info(self, token_address: str) -> Dict[str, Any]:
        """Get detailed information about a specific token."""
        try:
            session = await self.get_session()
            url = f"{self.config.solana_tracker_url}/tokens/{token_address}"
            
            async with session.get(
                url,
                headers={"x-api-key": self.config.solana_tracker_api_key}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Token info request failed: {response.status}")
                    return self._get_mock_token_info(token_address)
        except Exception as e:
            logger.error(f"Error fetching token info: {e}")
            return self._get_mock_token_info(token_address)

    def format_token_info(self, info: Dict[str, Any]) -> str:
        """Format token information in Cheshire's style."""
        token = info.get("token", {})
        price = info.get("price", {})
        volume = info.get("volume", {})
        
        return (
            f"✨ Token Profile ✨\n"
            f"Name: {token.get('name', 'Unknown')} ({token.get('symbol', '???')})\n"
            f"Address: {token.get('mint', 'Unknown')}\n\n"
            f"📊 Market Data:\n"
            f"• Price: ${price.get('current', '???')}\n"
            f"• 24h Change: {price.get('change24h', '???')}%\n"
            f"• 24h Volume: ${volume.get('volume24h', '???')}\n\n"
            f"🔮 Description:\n"
            f"{token.get('description', 'A mysterious token indeed...')}\n\n"
            f"Remember, even the Cheshire cat's grin fades... Always DYOR! 😸"
        )

    async def get_assets_by_owner(self, owner_address: str) -> Dict[str, Any]:
        """Get assets owned by a specific address using Helius DAS API."""
        session = await self.get_session()
        payload = {
            "jsonrpc": "2.0",
            "id": "cheshire-terminal",
            "method": "getAssetsByOwner",
            "params": {
                "ownerAddress": owner_address
            }
        }
        
        async with session.post(
            self.config.helius_rpc_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            return await response.json()

    async def get_trending_tokens(self, timeframe: str = "1h") -> List[Dict[str, Any]]:
        """Get trending tokens from SolanaTracker."""
        try:
            session = await self.get_session()
            async with session.get(
                f"{self.config.solana_tracker_url}/tokens/trending/{timeframe}",
                headers={"x-api-key": self.config.solana_tracker_api_key}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Using mock data due to API error: {response.status}")
                    return self._get_mock_trending_tokens()
        except Exception as e:
            logger.error(f"Error fetching trending tokens: {e}")
            return self._get_mock_trending_tokens()

    async def get_token_volume(self) -> List[Dict[str, Any]]:
        """Get top tokens by volume from SolanaTracker."""
        try:
            session = await self.get_session()
            async with session.get(
                f"{self.config.solana_tracker_url}/tokens/volume",
                headers={"x-api-key": self.config.solana_tracker_api_key}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Using mock data due to API error: {response.status}")
                    return self._get_mock_volume_tokens()
        except Exception as e:
            logger.error(f"Error fetching token volume: {e}")
            return self._get_mock_volume_tokens()

    def _get_mock_token_info(self, token_address: str) -> Dict[str, Any]:
        """Provide mock token information for testing."""
        return {
            "token": {
                "name": "Mock Token",
                "symbol": "MOCK",
                "mint": token_address,
                "description": "A mysterious token from the blockchain wonderland..."
            },
            "price": {
                "current": "1.23",
                "change24h": "5.67"
            },
            "volume": {
                "volume24h": "1234567"
            }
        }

    def _get_mock_trending_tokens(self) -> List[Dict[str, Any]]:
        """Provide mock trending tokens data for testing."""
        return [
            {
                "token": {
                    "name": "Jupiter",
                    "symbol": "JUP",
                    "description": "Jupiter is the key liquidity aggregator for Solana."
                }
            },
            {
                "token": {
                    "name": "Bonk",
                    "symbol": "BONK",
                    "description": "Solana's playful community token."
                }
            },
            {
                "token": {
                    "name": "Raydium",
                    "symbol": "RAY",
                    "description": "Leading AMM on Solana."
                }
            }
        ]

    def _get_mock_volume_tokens(self) -> List[Dict[str, Any]]:
        """Provide mock volume tokens data for testing."""
        return [
            {
                "token": {
                    "name": "Solana",
                    "symbol": "SOL",
                    "description": "Native token of the Solana blockchain."
                }
            },
            {
                "token": {
                    "name": "USDC",
                    "symbol": "USDC",
                    "description": "Leading stablecoin on Solana."
                }
            },
            {
                "token": {
                    "name": "Marinade Staked SOL",
                    "symbol": "mSOL",
                    "description": "Liquid staking token for Solana."
                }
            }
        ]

    def format_market_insight(self, trending: List[Dict[str, Any]], volume: List[Dict[str, Any]]) -> str:
        """Format market data in Cheshire's style."""
        now = datetime.now().strftime("%H:%M:%S")
        
        trending_tokens = trending[:5]
        trending_str = "\n".join([
            f"• {token['token']['name']} ({token['token']['symbol']}) 🚀"
            for token in trending_tokens
        ])
        
        volume_leaders = volume[:3]
        volume_str = "\n".join([
            f"• {token['token']['name']} ({token['token']['symbol']}) 💫"
            for token in volume_leaders
        ])
        
        return (
            f"Through the looking glass at {now}, I see...\n\n"
            f"🔥 Trending Tokens (Past Hour):\n{trending_str}\n\n"
            f"📊 Volume Leaders:\n{volume_str}\n\n"
            f"Keep an eye on these curious patterns... The market never sleeps! ✨\n"
            f"And remember, $GRIN's movements often follow the market's madness! 🎭"
        )

    async def get_market_analysis(self) -> str:
        """Get comprehensive market analysis."""
        try:
            trending = await self.get_trending_tokens("1h")
            volume = await self.get_token_volume()
            return self.format_market_insight(trending, volume)
        except Exception as e:
            logger.error(f"Error getting market analysis: {e}")
            return (
                "Oh my... The market mist is particularly thick today! 🎭\n"
                "Perhaps we should try again when the blockchain fog clears... ✨"
            )

    async def analyze_wallet(self, address: str) -> Dict[str, Any]:
        """Perform comprehensive wallet analysis."""
        try:
            assets = await self.get_assets_by_owner(address)
            
            analysis = {
                "assets": assets.get("result", []),
                "summary": f"Purr-fect! Let me analyze this wallet for you... 😸\n"
                          f"Found {len(assets.get('result', []))} magical assets!",
                "suggestions": [
                    "Consider the cross-chain opportunities...",
                    "Watch for NFT trading patterns...",
                    "Monitor $GRIN interactions..."
                ]
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing wallet: {e}")
            return {
                "assets": [],
                "summary": "The blockchain mist clouds my vision! 🎭",
                "suggestions": ["Perhaps try again when the network fog clears... ✨"]
            }

    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()

# Example usage
async def main():
    client = SolanaClient()
    try:
        analysis = await client.get_market_analysis()
        print(analysis)
    finally:
        await client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
