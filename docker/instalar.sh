#!/bin/bash
cd /src
git pull
cd docker/src
#pip install -e .
python setup.py sdist upload -r internal
