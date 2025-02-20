# sitegenerator
Generate and manage website using scripts

# Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# GIT
```bash
# create a new feature branch
git checkout -b new-feature
# add changes
git add xx
git commit
# push to new branch
git push -u origin new-feature
# push to main branch
git checkout main
git pull
git pull origin new-feature
# resolve conflicts
git push
```
# Configuration
Create a .env
```bash
MARKDOWN_DIR="articles"
HTML_DIR="html"
TOP_TAGS=10
NB_ARTICLES_PER_PAGE=2
```

# Articles
Articles are created in markdown format and stored in `articles` directory

# RUN
`python3 website.py`

