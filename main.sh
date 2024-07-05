#!/bin/zsh
export PYTHONPATH=$(pwd)/src
python src/main.py
cd public && python -m http.server 8888

