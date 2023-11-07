#!/bin/bash

message="Running tests ..."
echo -e "\033[1;34mInfo: $message\033[0m"

docker-compose run --rm api pytest --cov .

if [ $? -eq 1 ]; then
    message="Tests failed, please check and fix your code"
    echo -e "\033[1;31mERROR: $message\033[0m";
    exit 1
else
    message="Success"
    echo -e "\033[1;32mOK: $message\033[0m"
    exit 0
fi
