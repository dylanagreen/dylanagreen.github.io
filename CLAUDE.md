# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is Dylan Green's personal academic website, built with [Hugo](https://gohugo.io/) using the [Hextra theme](https://github.com/imfing/hextra) (included as a git submodule at `themes/hextra`). It is deployed to GitHub Pages via the workflow in `.github/workflows/hugo.yml`.

## Commands

```bash
# Local development server (live reload)
hugo server

# Build for production
hugo build --gc --minify

# Create a new blog post
hugo new content/blog/posts/YYYY/MM-DD-YY-slug.md
```

## Architecture

### Content structure
- `content/_index.md` — homepage
- `content/about.md` — personal/hobbies page
- `content/research.md` — research experience and publications list
- `content/blog/posts/YYYY/` — blog posts organized by year

### Theme customization
- `assets/css/custom.css` — site-specific CSS overrides loaded on top of Hextra's styles. Contains `.lefty` (float-left figure class), `.first_author` (orange color for highlighting author names), and `#floatleft`/`#floatright` image URL fragment helpers.
- `data/icons.yaml` — custom SVG icon definitions (ORCiD variants) referenced by name in `hugo.yaml` nav menu entries via `params.icon`.
- `layouts/shortcodes/code.html` — a shortcode that reads and renders a file from disk as markdown: `{{< code file="path" >}}`.

### Configuration
`hugo.yaml` is the sole config file. Key settings:
- MathJax is enabled for math rendering; use `\(...\)` for inline and `\[...\]` or `$$...$$` for block math.
- The `page.width: full` param uses Hextra's full-width page layout.
- Image caching uses Hugo's built-in cache at `:cacheDir/images`.

### Static assets
- `assets/images/` — photos used in content pages
- `assets/presentations/` — PDF slide decks linked from `research.md`
- `assets/ctf/` — CTF write-up assets linked from blog posts
- `static/` — files copied as-is to `public/` (currently empty)

### Deployment
Pushing to `main` triggers `.github/workflows/hugo.yml`, which builds with Hugo Extended and deploys to GitHub Pages. The `public/` directory is the build output and is tracked in git as an untracked directory (not committed).
