#!/bin/bash

HTTP=$(which http)

if [ ! -x "$HTTP" ]; then
    echo 'You need HTTPie to run this script!'
    echo 'sudo pip3 install httpie'
    exit 1
fi

URL=:8080

set -x

http PUT $URL/stores/1 name=1 store_address=test
http $URL/stores/1
http PUT $URL/stores/1 name=1 store_address=test tags:='{"color": "red"}'
http $URL/stores/1
http $URL/stores store_address==test
http DELETE $URL/stores/1
