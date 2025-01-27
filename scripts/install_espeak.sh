#!/bin/bash
set -e

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install it first: https://brew.sh/"
        exit 1
    fi
    
    # Install build dependencies
    brew install \
        autoconf \
        automake \
        libtool \
        pkg-config \
        make \
        gcc
else
    # Linux
    apt-get update && apt-get install -y \
        git \
        autoconf \
        automake \
        libtool \
        pkg-config \
        make \
        gcc \
        g++
fi

# Clone the specific espeak-ng fork
git clone https://github.com/rhasspy/espeak-ng.git
cd espeak-ng

# Build and install
./autogen.sh
./configure --prefix=/usr
make
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo make install
else
    make install
fi

# Clean up
cd ..
rm -rf espeak-ng

echo "eSpeak-ng (Rhasspy fork) installation completed successfully" 