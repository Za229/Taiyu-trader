# VPS deployment (Ubuntu 22.04/24.04, Docker)

Taiyu-trader currently uses CoinDCX's public candle endpoint and runs in paper mode. It does not place orders.

## 1. Prepare the VPS
Provision an Ubuntu VPS. In its provider firewall/security group, allow inbound TCP 22 from your IP and TCP 80/443 as needed. Do not expose port 8000 publicly in production.

SSH in, then install Docker Engine and the Docker Compose plugin using Docker's official Ubuntu instructions:
https://docs.docker.com/engine/install/ubuntu/

## 2. Give the VPS read-only access to the private GitHub repository

This repository is private, so a plain HTTPS clone may not work without authentication. On the VPS, create a dedicated SSH deploy key:
```bash
ssh-keygen -t ed25519 -C "taiyu-trader-vps-deploy" -f ~/.ssh/taiyu_trader_deploy
cat ~/.ssh/taiyu_trader_deploy.pub
```
Copy only the printed **public** key into GitHub: repository → Settings → Deploy keys → Add deploy key. Leave write access unchecked. Keep the private key on the VPS; never paste it into chat or commit it.

Configure SSH for that key:
```bash
cat >> ~/.ssh/config <<'EOF'
Host github-taiyu-trader
  HostName github.com
  User git
  IdentityFile ~/.ssh/taiyu_trader_deploy
  IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
ssh -T git@github-taiyu-trader
```

## 3. Deploy
```bash
sudo apt-get update
sudo apt-get install -y git
git clone git@github-taiyu-trader:Za229/Taiyu-trader.git
cd Taiyu-trader
cp .env.example .env
```

Leave `TRADING_MODE=paper`, `ENABLE_LIVE_TRADING=false`, and API key fields empty. Then build and run:
```bash
sudo docker build -t taiyu-trader .
sudo docker run -d --name taiyu-trader --restart unless-stopped \
  --env-file .env -e PORT=8000 -p 127.0.0.1:8000:8000 taiyu-trader
```

Verify on the VPS:
```bash
curl http://127.0.0.1:8000/api/health
curl -I http://127.0.0.1:8000/
sudo docker logs --tail 100 taiyu-trader
```

## 4. HTTPS / public URL
For a production public URL, point a domain's DNS A record to the VPS IP and configure a reverse proxy such as Caddy or Nginx with HTTPS. Keep the app bound to 127.0.0.1:8000; expose only SSH (restricted to your IP) and web ports 80/443. Use the proxy's TLS automation and security updates.

## 5. Updates
```bash
cd ~/Taiyu-trader
git pull
sudo docker build -t taiyu-trader .
sudo docker rm -f taiyu-trader
sudo docker run -d --name taiyu-trader --restart unless-stopped \
  --env-file .env -e PORT=8000 -p 127.0.0.1:8000:8000 taiyu-trader
```

## Important
- The CoinDCX public candle API is documented at https://docs.coindcx.com/ and uses pair names such as `B-BTC_USDT`.
- CoinDCX spot candle intervals documented here are `1m`, `15m`, `1h`, and `1d`.
- Confirm symbol/pair availability on CoinDCX for the exact market you want.
- Do not assume a sandbox exists; confirm the current test environment with CoinDCX before any order testing.
- This project does not implement order placement. Do not add production trading keys until execution, reconciliation, rate limits, loss caps, duplicate-order prevention, and emergency stop have been independently tested.
- Never share SSH passwords/private keys or exchange secrets in chat or commit them to GitHub.
