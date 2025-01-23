# MacBook Pro Setup (Validator Node)

# 1. Install Solana v1.18.26
sh -c "$(curl -sSfL https://release.solana.com/v1.18.26/install)"
export PATH="/home/$USER/.local/share/solana/install/active_release/bin:$PATH"

# 2. Create validator directory and files
mkdir -p ~/solana-validator
cd ~/solana-validator

# 3. Generate validator identity
solana-keygen new --outfile ~/solana-validator/identity.json

# 4. Create validator configuration
cat > validator-config.sh << 'EOF'
#!/bin/bash

# Validator settings
IDENTITY_PATH="$HOME/solana-validator/identity.json"
LEDGER_PATH="$HOME/solana-validator/ledger"
NETWORK_PORT=8000
GOSSIP_PORT=8001
RPC_PORT=8899

# Start validator with optimized settings for M-series Macs
solana-validator \
  --identity $IDENTITY_PATH \
  --ledger $LEDGER_PATH \
  --rpc-port $RPC_PORT \
  --dynamic-port-range $NETWORK_PORT-$(($NETWORK_PORT + 20)) \
  --gossip-port $GOSSIP_PORT \
  --enable-rpc-transaction-history \
  --rpc-bind-address 0.0.0.0 \
  --private-rpc \
  --no-untrusted-rpc \
  --entrypoint localhost:$GOSSIP_PORT \
  --expected-genesis-hash 4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZAMdL4VZHirAn \
  --wal-recovery-mode skip_any_corrupted_record \
  --limit-ledger-size \
  --accounts-db-caching-enabled \
  --no-port-check \
  --no-poh-speed-test
EOF

chmod +x validator-config.sh

# 5. Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash

while true; do
    echo "=== Solana Validator Status ==="
    solana validators
    echo "=== Catchup Status ==="
    solana catchup ~/solana-validator/identity.json
    echo "=== Resource Usage ==="
    top -l 1 | grep -E "CPU|Memory|PhysMem"
    sleep 60
done
EOF

chmod +x monitor.sh

# Mac Mini Setup (Control Node)
# ============================

# 1. Install Solana v1.18.26
sh -c "$(curl -sSfL https://release.solana.com/v1.18.26/install)"
export PATH="/home/$USER/.local/share/solana/install/active_release/bin:$PATH"

# 2. Create control configuration script
cat > control-config.sh << 'EOF'
#!/bin/bash

# Replace VALIDATOR_IP with your MacBook Pro's IP address
VALIDATOR_IP="192.168.1.206"

# Configure Solana CLI to connect to your validator
solana config set --url http://$VALIDATOR_IP:8899
solana config set --keypair ~/validator-keypair.json

# Verify connection
solana cluster-version
solana validators
EOF

chmod +x control-config.sh

# 3. Create utility functions
cat > utils.sh << 'EOF'
#!/bin/bash

check_validator_health() {
    echo "Checking validator health..."
    solana validators
    solana block-production
    solana slot
}

restart_validator() {
    echo "Gracefully restarting validator..."
    pkill -f solana-validator
    sleep 10
    ./validator-config.sh
}

monitor_logs() {
    echo "Monitoring validator logs..."
    tail -f ~/solana-validator/log/validator.log
}
EOF

chmod +x utils.sh