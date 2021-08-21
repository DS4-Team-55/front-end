#! /bin/bash

clear
echo "the script starts now"

docker run -p 8050:8050 -p 8051:8051 -p 5000:5000\
  -v "$PWD":/home/project \
  -it jcgarciaca/ds4a-project