#!/bin/bash
# lxc-setup.sh — Deploy Lighthouse Waiting Room into LXC container
# Run on Jetson (nvidia-aiui): sudo bash lxc-setup.sh
set -e

CONTAINER="lighthouse-waiting-room"
APP_DIR="/opt/waiting-room"

echo "[1/7] Creating LXC container: $CONTAINER"
lxc launch ubuntu:22.04 "$CONTAINER" || echo "Container exists, continuing..."

echo "[2/7] Config: autostart on, 128MB RAM, 1 CPU"
lxc config set "$CONTAINER" boot.autostart true
lxc config set "$CONTAINER" limits.memory 128MB
lxc config set "$CONTAINER" limits.cpu 1

echo "[3/7] Installing base deps"
lxc exec "$CONTAINER" -- bash -c "
    apt-get update -qq &&
    apt-get install -y -qq curl ca-certificates python3
"

echo "[4/7] Installing uv"
lxc exec "$CONTAINER" -- bash -c "
    curl -LsSf https://astral.sh/uv/install.sh | sh &&
    ln -sf /root/.local/bin/uv /usr/local/bin/uv &&
    uv --version
"

echo "[5/7] Pushing app files into container"
lxc exec "$CONTAINER" -- mkdir -p "$APP_DIR"
for f in main.py router.py pyproject.toml MEMORY.md .env; do
    if [ -f "$f" ]; then
        lxc file push "$f" "$CONTAINER$APP_DIR/$f" && echo "  pushed: $f"
    else
        echo "  SKIP (not found): $f — copy manually before running"
    fi
done

echo "[6/7] Installing Python deps with uv"
lxc exec "$CONTAINER" -- bash -c "cd $APP_DIR && uv sync"

echo "[7/7] Creating and enabling systemd service"
lxc exec "$CONTAINER" -- bash -c "
cat > /etc/systemd/system/waiting-room.service << 'EOF'
[Unit]
Description=Lighthouse Waiting Room
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/uv run uvicorn main:app --host 0.0.0.0 --port 8443
Restart=always
RestartSec=5
EnvironmentFile=$APP_DIR/.env

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable waiting-room
systemctl start waiting-room
systemctl status waiting-room --no-pager
"

CONTAINER_IP=\$(lxc list "$CONTAINER" --format csv -c 4 | cut -d' ' -f1)
echo ""
echo "========================================"
echo "Waiting Room deployed: $CONTAINER"
echo "Container IP: \$CONTAINER_IP  Port: 8443"
echo ""
echo "Health check:"
echo "  curl http://\$CONTAINER_IP:8443/health"
echo ""
echo "Auth test:"
echo "  curl -X POST http://\$CONTAINER_IP:8443/auth \\"
echo "    -H 'X-Spring-Token: YOUR_TOKEN' \\"
echo "    -H 'X-AI-Model: claude-sonnet-4-6' \\"
echo "    -H 'X-Node-ID: nvidia-aiui'"
echo "========================================"
