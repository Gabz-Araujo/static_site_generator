#!/bin/zsh
export PYTHONPATH=$(pwd)/src
python -m unittest discover -s test
