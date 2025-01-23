#!/bin/bash

while true; do
    echo "=== Solana Validator Status ==="
    echo "Time: $(date)"
    
    echo -e "\n=== RPC Health Check ==="
    curl -s -X POST -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' \
        http://localhost:8899
    
    echo -e "\n=== Validator Identity ==="
    solana address -k ~/solana-validator/identity.json
    
    echo -e "\n=== Catchup Status ==="
    solana catchup ~/solana-validator/identity.json
    
    echo -e "\n=== Resource Usage ==="
    top -l 1 | grep -E "CPU|Memory|PhysMem"
    
    echo -e "\n=== Network Status ==="
    netstat -an | grep 8899
    
    echo -e "\n================================"
    sleep 30
done
