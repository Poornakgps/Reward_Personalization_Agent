#!/bin/bash

if [ "$1" = "api" ]; then
    exec uvicorn workspace.app:app --host 0.0.0.0 --port 8000
elif [ "$1" = "test" ]; then
    exec pytest
elif [ "$1" = "setup" ]; then
    exec make seed-data
elif [ "$1" = "shell" ]; then
    exec /bin/bash
elif [ "$1" = "notebook" ]; then
    exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
elif [ "$1" = "phi" ]; then
    shift
    exec phi "$@"
else
    exec "$@"
fi
