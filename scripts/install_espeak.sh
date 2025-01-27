#!/bin/bash
set -e

# Check if espeak-ng directory exists and handle it
if [ -d "espeak-ng" ]; then
    read -p "espeak-ng directory already exists. Delete it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf espeak-ng
    else
        echo "Installation cancelled. Please remove or rename the espeak-ng directory and try again."
        exit 1
    fi
fi

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install it first: https://brew.sh/"
        exit 1
    fi

    # Ensure Xcode Command Line Tools are installed
    if ! command -v xcode-select &> /dev/null; then
        echo "Installing Xcode Command Line Tools..."
        xcode-select --install
        echo "After Xcode Command Line Tools installation completes, please run this script again."
        exit 1
    fi
    
    # Install build dependencies
    brew install \
        autoconf \
        automake \
        libtool \
        pkg-config \
        make \
        gcc \
        sonic \
        pcaudiolib

    # Set environment variables for compiler
    export CC=/opt/homebrew/bin/gcc-13
    export CXX=/opt/homebrew/bin/g++-13
    export PATH="/opt/homebrew/opt/make/libexec/gnubin:$PATH"
    export CFLAGS="-I/opt/homebrew/include"
    export CXXFLAGS="-I/opt/homebrew/include"
    export LDFLAGS="-L/opt/homebrew/lib"
    export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"

    # Clone the specific espeak-ng fork
    git clone https://github.com/rhasspy/espeak-ng.git
    cd espeak-ng

    # Build and install for macOS
    ./autogen.sh
    ./configure --prefix=/opt/homebrew
    make
    sudo make install
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
        g++ \
        libsonic-dev \
        libpcaudio-dev

    # Clone the specific espeak-ng fork
    git clone https://github.com/rhasspy/espeak-ng.git
    cd espeak-ng

    # Build and install for Linux
    ./autogen.sh
    ./configure --prefix=/usr
    make
    make install
fi

# Clean up
cd ..
rm -rf espeak-ng

echo "eSpeak-ng (Rhasspy fork) installation completed successfully" 