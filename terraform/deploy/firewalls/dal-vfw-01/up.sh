#! /bin/bash

IP_ADDRESS=$1

if [ -z "$IP_ADDRESS" ]; then
    echo "Usage: $0 <IP_ADDRESS>"
    exit 1
fi

while true; do
    if [[ $(curl -s -o /dev/null -w '%{http_code}' -k https://"$IP_ADDRESS"/php/login.php?) == "200" ]]; then
        echo "200 OK received"
        break
    else
        echo "Waiting for 200 OK response"
        sleep 5
    fi
done
