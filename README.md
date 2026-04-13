Run the blog locally using

```sh
# Create/sync the environment
uv sync

# Build the site into _site/
uv run build.py

# Serve the generated site locally
uv run python -m http.server 8000 --directory _site
```
