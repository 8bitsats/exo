#!/bin/bash

# Use either IP or domain name
RPC_ENDPOINT="https://rpc.chesh.ai"  # Using HTTPS since we set up SSL

# Configure Solana CLI
solana config set --url $RPC_ENDPOINT
solana config set --keypair ~/solana-validator/identity.json

# Verify configuration
echo "=== Solana CLI Configuration ==="
solana config get

# Test RPC connection
echo -e "\n=== Testing RPC Connection ==="
curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' \
  $RPC_ENDPOINT

echo -e "\n=== Setup Complete ==="
