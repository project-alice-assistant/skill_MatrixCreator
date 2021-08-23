#!/usr/bin/env bash

curl https://s3.amazonaws.com/apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
apt-get update
apt-get install matrixio-creator-init libmatrixio-creator-hal libmatrixio-creator-hal-dev
