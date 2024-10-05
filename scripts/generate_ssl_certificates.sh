#!/bin/sh

echo "Enter server ip or domain name"
read -r ip
echo "Setup ssl ceritificates"
openssl req -newkey rsa:2048 -days 365 -sha256 -nodes -keyout headman_bot.key -x509 -out headman_bot.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=$ip"
cp headman_bot.pem headman_bot.key nginx/
