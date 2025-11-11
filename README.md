# sitegenerator
Static website generator for blogs with markdown articles, tag system, and light/dark theme support.

## Features
- Markdown articles with YAML frontmatter
- Tag system with dedicated tag pages
- Light/dark theme toggle
- Responsive design
- Pagination support
- Thumbnail support for articles
- Static page support

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` file:
```bash
MARKDOWN_DIR="articles"
HTML_DIR="html"
CSS_FILE="style.css"
TOP_TAGS=5
NB_ARTICLES_PER_PAGE=2
SHOW_FULL_CONTENT=false
SERVER="your_server_ip"
SITE_DIR="/var/www/your_site"
```

- `MARKDOWN_DIR`: Source articles directory
- `HTML_DIR`: Generated HTML output directory
- `CSS_FILE`: CSS stylesheet (must be in assets folder)
- `TOP_TAGS`: Number of top tags to display in sidebar
- `NB_ARTICLES_PER_PAGE`: Articles per index page
- `SHOW_FULL_CONTENT`: Show full articles (true) or abstracts only (false) on index
- `SERVER`: Remote server IP for deployment
- `SITE_DIR`: Remote directory path for deployment

## Article Format
Articles use markdown with YAML frontmatter:
```yaml
---
title: "Article Title"
date: 2024-01-01
tags: "tag1, tag2, tag3"
abstract: "Brief article description"
thumbnail: "image.png"  # optional
---

Your markdown content here...
```

## Project Structure
- `articles/`: Markdown source files organized by date (YYYY/MM/DD/article-name/)
- `assets/`: CSS, images, JavaScript files
- `static/`: Static HTML pages (contact, about, etc.)
- `templates/`: HTML templates for generation
- `html/`: Generated website output

## Generate Website
```bash
python3 website.py
```

This generates:
- Index pages with pagination
- Individual article pages
- Tag pages (`/tags/tagname.html`)
- Copies assets and static files

## Deploy
```bash
python3 deploy.py
```

Deployment:
1. Creates timestamped backup of remote HTML directory
2. Copies local `html/` folder to remote server via SCP
3. Requires SSH key authentication to remote server

## Files
- `website.py`: Main generator script
- `articles.py`: Article parsing and processing
- `deploy.py`: Remote deployment script
- `templates/`: HTML templates for different page types
- `assets/style.css`: Main stylesheet with light/dark theme support
- `assets/theme-toggle.js`: Theme switching functionality

# TODO Multilang support
[] Translate articles

[] Store both versions in same folder
YYYY/MM/DD/article-name/
  fr.md
  en.md
  images/

[] Modify yaml to add language tag

[] Add crosslink between languages
<link rel="alternate" hreflang="fr" href="https://example.com/fr/floating-point/" />
<link rel="alternate" hreflang="en" href="https://example.com/en/floating-point/" />
<link rel="canonical" href="https://example.com/fr/floating-point/" />

[] Add language selector in template
FR 🇫🇷  |  EN 🇬🇧

[] Handle mono language case
Some articles will be written in only one language

[] Static pages
Translate also static pages (livres and contact)