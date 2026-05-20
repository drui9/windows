#!/usr/bin/bash
SERVER_KEY=keys/server.key
SERVER_CRT=keys/server.crt
KEYDIR=keys
EXPIRY=365

mkdir -p $KEYDIR
openssl req -x509 -newkey rsa:4096 -keyout $SERVER_KEY -out $SERVER_CRT -days $EXPIRY -nodes
