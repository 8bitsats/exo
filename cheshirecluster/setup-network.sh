#!/bin/bash

# Network ports needed for Solana validator
echo "Setting up network ports for Solana validator..."

# Allow incoming connections
sudo pfctl -F all # Flush existing rules
cat << EOF | sudo pfctl -f -
pass in proto tcp from any to any port 8000:8020
pass in proto tcp from any to any port 8899
pass in proto tcp from any to any port 8900
pass in proto udp from any to any port 8001
pass in proto udp from any to any port 8002
EOF

# Enable pf
sudo pfctl -e

echo "Network setup complete"
