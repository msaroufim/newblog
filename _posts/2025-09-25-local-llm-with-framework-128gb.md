---
title: Running Qwen3 32B locally on Framework Desktop with 128GB RAM
layout: default
---

# Local LLM Setup: No More API Limits

Just set up Qwen3 32B running locally on my Framework Desktop with 128GB RAM. The setup is surprisingly straightforward and gives you a ChatGPT-like interface without any API calls or rate limits.

## The Stack

- **Hardware**: Framework Desktop with 128GB RAM (perfect for large models)
- **Model**: Qwen3 32B (20GB on disk)
- **Backend**: Ollama for model serving
- **Frontend**: Open WebUI for the chat interface
- **Access**: Tailscale for secure remote access

## Setup Commands

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download the model
ollama pull qwen3:32b

# Run Open WebUI
docker run -d --network=host -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui \
  --restart always ghcr.io/open-webui/open-webui:main

# Expose via Tailscale
sudo tailscale serve --bg 8080
```

Access from anywhere on your Tailscale network at `http://YOUR_MACHINE:8080`

## Why This Matters

- **No API costs** - Run unlimited queries
- **Private** - Your data stays local
- **Fast** - Low latency with local inference
- **Always available** - No rate limits or downtime

The Framework Desktop's 128GB RAM handles the 32B model comfortably with room for system overhead. Perfect setup for serious AI work without cloud dependencies.

![Open WebUI Interface](/assets/open-webui-screenshot.png)