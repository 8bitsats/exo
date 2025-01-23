#!/bin/bash

# Kill any existing ngrok processes
pkill -f ngrok

# Start ngrok tunnel for Solana RPC
echo "Starting ngrok tunnel for Solana RPC endpoint..."
ngrok http 8899 --log=stdout > ngrok.log 2>&1 &

# Wait for ngrok to start
echo "Waiting for ngrok to initialize..."
sleep 5

# Keep trying to get the URL for up to 30 seconds
for i in {1..6}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
    
    if [ ! -z "$NGROK_URL" ] && [ "$NGROK_URL" != "null" ]; then
        echo "Ngrok tunnel established at: $NGROK_URL"
        
        # Update Solana CLI config to use ngrok URL
        solana config set --url $NGROK_URL
        
        echo "Solana CLI configured to use ngrok endpoint"
        echo "You can now use this RPC endpoint for your Solana operations"
        
        # Test the connection
        echo -e "\nTesting RPC connection..."
        curl -X POST -H "Content-Type: application/json" \
            -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' \
            $NGROK_URL
        
        exit 0
    fi
    
    echo "Waiting for ngrok URL... (attempt $i/6)"
    sleep 5
done

echo "Failed to get ngrok URL. Check ngrok.log for details."
cat ngrok.log
exit 1
