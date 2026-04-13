Run the blog locally using

```sh
# Create/sync the environment
uv sync

# Build the site into _site/
uv run build.py

# Serve the generated site locally
uv run python -m http.server 8000 --directory _site
```

For local editing, use the dev server:

```sh
# Rebuild on file changes and serve _site/ on port 8000
uv run dev.py
```
