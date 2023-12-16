#!/bin/bash

if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'Error: virtualenv is not installed.' >&2
  exit 1
fi

#Virtual environment
virtualenv venv

source venv/bin/activate

pip install Flask
