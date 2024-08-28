#!/bin/bash

cleanup() {
    echo "Stopping servers..."
    if [[ -n $python_pid ]]; then
        kill $python_pid
    fi
    exit 0
}

source ./python-env/bin/activate

python3 mqtt_server.py &
python_pid=$!

trap cleanup INT

cd frontend
npm run dev

cleanup

