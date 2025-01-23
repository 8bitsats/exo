import asyncio
from typing import Optional, Dict, List, Any
import numpy as np
from datetime import datetime

from ..grpc.grpc_peer_handle import GRPCPeerHandle
from exo.inference.shard import Shard
from .helius_client import HeliusClient

class TransactionProcessor:
    def __init__(self, helius_client: HeliusClient, mlx_peer: GRPCPeerHandle):
        self.helius_client = helius_client
        self.mlx_peer = mlx_peer
        self.processing_queue = asyncio.Queue()
        self._running = False
        self.shard = Shard(
            model_id="mlx-community/Llama-3.2-3B-Instruct-4bit",
            start_layer=0,
            end_layer=-1,
            n_layers=32
        )

    def _prepare_transaction_data(self, transaction: Dict) -> np.ndarray:
        """Convert transaction data to a format suitable for MLX processing"""
        # Extract relevant features from the transaction
        features = []
        
        # Basic transaction data
        features.extend([
            float(transaction.get("blockTime", 0)),
            float(transaction.get("slot", 0)),
            len(transaction.get("transaction", {}).get("signatures", [])),
        ])
        
        # Account keys
        account_keys = transaction.get("transaction", {}).get("message", {}).get("accountKeys", [])
        features.append(len(account_keys))
        
        # Instructions
        instructions = transaction.get("transaction", {}).get("message", {}).get("instructions", [])
        features.append(len(instructions))
        
        # Convert to numpy array and reshape for model input
        return np.array(features, dtype=np.float32).reshape(1, -1)

    async def _process_transaction(self, transaction: Dict):
        try:
            # Prepare transaction data
            transaction_data = self._prepare_transaction_data(transaction)
            
            # Process with MLX node
            request_id = f"tx_{transaction.get('signature', '')}_{int(datetime.now().timestamp())}"
            
            # Send tensor to MLX node for processing
            result = await self.mlx_peer.send_tensor(self.shard, transaction_data, request_id)
            
            if result is not None:
                # Get final inference result
                final_result, is_finished = await self.mlx_peer.get_inference_result(request_id)
                if final_result is not None and is_finished:
                    # Process the result (e.g., store in database, trigger alerts)
                    await self._handle_processed_result(transaction, final_result)
        
        except Exception as e:
            print(f"Error processing transaction: {str(e)}")

    async def _handle_processed_result(self, transaction: Dict, result: np.ndarray):
        """Handle the processed transaction result"""
        # Example: Print analysis results
        print(f"Transaction {transaction.get('signature', 'unknown')} processed:")
        print(f"Analysis result: {result}")
        
        # Here you could:
        # - Store results in a database
        # - Trigger alerts based on certain patterns
        # - Forward to other systems
        pass

    async def start_processing(self):
        """Start processing Solana transactions"""
        self._running = True
        
        async def transaction_callback(params: Dict):
            await self.processing_queue.put(params)
        
        # Start transaction subscription
        subscription_task = asyncio.create_task(
            self.helius_client.subscribe_transactions(
                transaction_callback,
                filter_options={"commitment": "confirmed"}
            )
        )
        
        # Process transactions from queue
        while self._running:
            try:
                transaction = await self.processing_queue.get()
                await self._process_transaction(transaction)
                self.processing_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in transaction processing loop: {str(e)}")
        
        # Cleanup
        subscription_task.cancel()
        try:
            await subscription_task
        except asyncio.CancelledError:
            pass

    async def stop_processing(self):
        """Stop processing transactions"""
        self._running = False
        await self.helius_client.close()
        # Wait for queue to be empty
        if not self.processing_queue.empty():
            await self.processing_queue.join()
