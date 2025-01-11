#!/bin/bash
set +x
set -e

echo "==>> Deploy vosk-rpyc <<=="
docker compose build
docker stack deploy --compose-file compose.yml vosk