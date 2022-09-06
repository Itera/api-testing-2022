#!/bin/sh

ACTIVATE=./venv/Scripts/activate
FLAGS="--trusted-host pypi.org --trusted-host files.pythonhosted.org"

if [ ! -f $ACTIVATE ]; then
  echo "* Creating virtual environment"
  python -m venv venv
fi

source $ACTIVATE

echo "* Installing python dependencies"
python -m pip install $FLAGS --upgrade pip
pip install $FLAGS -r requirements.txt
