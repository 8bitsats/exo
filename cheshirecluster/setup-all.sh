#!/bin/bash

echo "=== Setting up Solana Validator and RPC Endpoint ==="

# Make all scripts executable
chmod +x setup-network.sh setup-ngrok.sh validator-config.sh monitor.sh

# 1. Set up network and firewall
echo -e "\n=== Setting up network... ==="
./setup-network.sh

# 2. Start the validator in a new terminal
echo -e "\n=== Starting Solana validator... ==="
osascript -e 'tell app "Terminal" to do script "cd ~/solana-validator && '"$(pwd)"'/validator-config.sh"'

# Wait for validator to start
echo "Waiting for validator to initialize..."
sleep 10

# Test if validator is responding
echo "Testing validator RPC..."
curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' \
  http://localhost:8899

if [ $? -ne 0 ]; then
    echo "Error: Validator is not responding"
    exit 1
fi

# 3. Set up ngrok tunnel in a new terminal
echo -e "\n=== Setting up ngrok tunnel... ==="
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && ./setup-ngrok.sh"'

# 4. Start monitoring in a new terminal
echo -e "\n=== Starting monitoring... ==="
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && ./monitor.sh"'

echo -e "\n=== Setup Complete ==="
echo "Your Solana validator is running in a separate terminal"
echo "Ngrok tunnel is running in another terminal"
echo "Monitor your validator status in the monitoring terminal window"
