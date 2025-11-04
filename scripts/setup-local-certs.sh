#!/bin/bash
set -e

echo "🔐 Setting up local SSL certificates"

# Check that mkcert is installed
if ! command -v mkcert &> /dev/null; then
    echo "❌ mkcert is not installed"
    echo "Installation:"
    echo "  macOS: brew install mkcert nss"
    echo "  Linux: see https://github.com/FiloSottile/mkcert#installation"
    exit 1
fi

# Install CA
echo "📝 Installing local CA..."
mkcert -install

# Get local IP
MY_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n1)
echo "📍 Detected IP: $MY_IP"

# Generate certificates
echo "🔑 Generating certificates..."
mkcert $MY_IP localhost 127.0.0.1

echo "✅ Certificates generated!"
