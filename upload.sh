```bash
#!/usr/bin/env bash
set -e

REPO="Cross-Lingual-Institute-Voice-Helpdesk-Project"
PROJECT_DIR="$HOME/Documents/STT AI/Project"

cd "$PROJECT_DIR"

# Verify GitHub CLI authentication
gh auth status

# Initialize Git if needed
if [ ! -d .git ]; then
    git init
fi

# Configure Git identity if not already configured
git config user.name >/dev/null 2>&1 || \
    git config user.name "rajdeepvraj"

git config user.email >/dev/null 2>&1 || \
    git config user.email "$(gh api user --jq .email 2>/dev/null || true)"

# Create or use the main branch
git branch -M main

# Stage project files
git add .

# Create a commit if there are staged changes
if ! git diff --cached --quiet; then
    git commit -m "Upload Cross-Lingual Institute Voice Helpdesk project"
fi

# Create a NEW public repository and push
gh repo create "$REPO" \
    --public \
    --source=. \
    --remote=github \
    --push

echo ""
echo "Upload completed!"
gh repo view "$REPO" --web
```
