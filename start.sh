#! /bin/bash

clear
echo "the script starts now"

docker run -p 8050:8050 -p 8051:8051\
  -v "$PWD":/home/project \
  -it jcgarciaca/digital-urban-greenhouse

