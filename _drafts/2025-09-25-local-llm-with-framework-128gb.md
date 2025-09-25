---
title: Running Qwen3 32B locally on Framework Desktop with 128GB RAM
layout: default
---

# Local LLM Setup: No More API Limits

Just set up Qwen3 32B running locally on my Framework Desktop with 128GB RAM. The setup is surprisingly straightforward and gives you a ChatGPT-like interface without any API calls or rate limits.

## The Stack

Framework Desktop with 128GB RAM running Qwen3 32B via Ollama, Open WebUI for the chat interface, and Tailscale for remote access.

## Setup Commands

```bash
curl -fsSL https://ollama.com/install.sh | sh

ollama pull qwen3:32b

docker run -d --network=host -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui \
  --restart always ghcr.io/open-webui/open-webui:main

sudo tailscale serve --bg 8080
```

Access from anywhere on your Tailscale network at `http://YOUR_MACHINE:8080`

![Open WebUI Interface](/assets/open-webui-screenshot.png)