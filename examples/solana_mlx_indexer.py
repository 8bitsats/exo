#!/usr/bin/env python3
"""
Solana Transaction Indexer with MLX Integration

This example demonstrates how to use the Exo framework to process Solana transactions
in real-time using MLX for analysis.

Requirements:
- Helius API key
- Running MLX node
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from exo.networking.solana.main import main

if __name__ == "__main__":
    print("Starting Solana Transaction Indexer with MLX Integration")
    print("======================================================")
    print("This example will:")
    print("1. Connect to Helius RPC for real-time Solana transaction data")
    print("2. Process transactions using MLX community node")
    print("3. Index and analyze transaction patterns")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nIndexer stopped by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
