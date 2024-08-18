#!/bin/sh

echo "Setup ssl ceritificates"
openssl req -newkey rsa:4096 -sha256 -nodes -keyout nginx/headman_bot.key -x509 -out nginx/headman_bot.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=YOURDOMAIN.EXAMPLE"
