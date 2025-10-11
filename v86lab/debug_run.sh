#!/bin/bash

IMAGE_NAME=i386/alpine-v86-debug
docker build . --file Dockerfile.alpine_image --platform linux/386 --rm --tag "$IMAGE_NAME"
docker run -it --rm --platform linux/386 $IMAGE_NAME su user42 -c 'cd /home/user42/shell_rpg_engine; ./install.sh engine.py; export PATH=/tmp/bin:$PATH ;/bin/ash'
