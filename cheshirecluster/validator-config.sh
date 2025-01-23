#!/bin/bash

# Validator settings
IDENTITY_PATH="$HOME/solana-validator/identity.json"
LEDGER_PATH="$HOME/solana-validator/ledger"
NETWORK_PORT=8000
GOSSIP_PORT=8001
RPC_PORT=8899

# Initialize ledger if it doesn't exist
if [ ! -d "$LEDGER_PATH" ]; then
  solana-ledger-tool create-new-ledger \
    --force \
    --max-genesis-archive-unpacked-size 1073741824 \
    "$LEDGER_PATH"
fi

# Start local test validator
solana-test-validator \
  --ledger $LEDGER_PATH \
  --rpc-port $RPC_PORT \
  --bind-address 0.0.0.0 \
  --faucet-port 9900 \
  --limit-ledger-size 50000000 \
  --quiet \
  --reset && \
touch /tmp/validator-init-complete
