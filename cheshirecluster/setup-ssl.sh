#!/bin/bash

# Install certbot if not already installed
if ! command -v certbot &> /dev/null; then
    brew install certbot
fi

# Get SSL certificates
sudo certbot certonly --standalone \
    -d rpc.chesh.ai \
    --agree-tos \
    --non-interactive \
    --preferred-challenges http \
    --email admin@chesh.ai

# Create Nginx symlink
sudo mkdir -p /etc/nginx/sites-enabled
sudo ln -sf $(pwd)/nginx.conf /etc/nginx/sites-enabled/solana-rpc.conf

# Reload Nginx
sudo nginx -t && sudo nginx -s reload

echo "SSL certificates have been installed and Nginx configured"
