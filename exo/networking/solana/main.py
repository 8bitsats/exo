import asyncio
import os
from typing import Optional
from exo.topology.device_capabilities import DeviceCapabilities, DeviceFlops
from ..grpc.grpc_peer_handle import GRPCPeerHandle
from .helius_client import HeliusClient
from .transaction_processor import TransactionProcessor

async def main():
    # Helius API configuration
    HELIUS_API_KEY = "e4e7f06a-1e90-4628-8b07-d4f3c30fc5c9"
    HELIUS_URL = "https://mainnet.helius-rpc.com"
    
    # MLX node configuration
    MLX_NODE_HOST = "localhost"  # Update with actual MLX node address
    MLX_NODE_PORT = 50051        # Update with actual MLX node port
    
    try:
        # Initialize Helius client
        helius_client = HeliusClient(HELIUS_API_KEY, HELIUS_URL)
        
        # Initialize MLX node connection
        mlx_capabilities = DeviceCapabilities(
            model="mlx-community/Llama-3.2-3B-Instruct-4bit",
            chip="mlx",
            memory=16 * 1024 * 1024 * 1024,  # 16GB
            flops=DeviceFlops(fp16=1e12, fp32=5e11, int8=2e12)  # Example FLOPS
        )
        
        mlx_peer = GRPCPeerHandle(
            _id="mlx_node_1",
            address=f"{MLX_NODE_HOST}:{MLX_NODE_PORT}",
            device_capabilities=mlx_capabilities
        )
        
        # Connect to MLX node
        await mlx_peer.connect()
        
        # Initialize transaction processor
        processor = TransactionProcessor(helius_client, mlx_peer)
        
        print("Starting Solana transaction processing with MLX integration...")
        print(f"Connected to Helius RPC at {HELIUS_URL}")
        print(f"Connected to MLX node at {MLX_NODE_HOST}:{MLX_NODE_PORT}")
        
        # Start processing transactions
        await processor.start_processing()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
    finally:
        # Cleanup
        if 'processor' in locals():
            await processor.stop_processing()
        if 'mlx_peer' in locals():
            await mlx_peer.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
