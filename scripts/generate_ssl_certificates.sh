#!/bin/sh

echo "Setup ssl ceritificates"
openssl req -newkey rsa:4096 -sha256 -nodes -keyout headman_bot.key -x509 -out headman_bot.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=YOURDOMAIN.EXAMPLE"
cp headman_bot.pem headman_bot.key nginx/
