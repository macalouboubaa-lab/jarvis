#!/usr/bin/env bash
# .devcontainer/start-docker.sh
# Démarre dockerd de façon idempotente. Appelé par postStartCommand.
set -euo pipefail

SOCKET=/var/run/docker.sock
LOG=/tmp/dockerd.log

if docker info >/dev/null 2>&1; then
  echo "[start-docker] daemon déjà accessible"
  exit 0
fi

if [ -S "$SOCKET" ]; then
  echo "[start-docker] suppression d'un socket orphelin"
  sudo rm -f "$SOCKET"
fi

echo "[start-docker] démarrage de dockerd (log: $LOG)"
sudo sh -c "nohup dockerd >'$LOG' 2>&1 &"

deadline=$(( $(date +%s) + 60 ))
until docker info >/dev/null 2>&1; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "[start-docker] ERREUR : dockerd pas prêt après 60s"
    sudo tail -n 40 "$LOG" || true
    exit 1
  fi
  sleep 1
done

echo "[start-docker] daemon prêt"