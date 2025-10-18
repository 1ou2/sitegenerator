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
CSS_FILE="style.css"
TOP_TAGS=5
NB_ARTICLES_PER_PAGE=2
```

MARKDOWN_DIR : location for the sources articles
HTML_DIR="html" : output directory
CSS_FILE="style.css" : CSS stylesheet that will be used - must be in the assets folder 
TOP_TAGS=5 : number of tags to display
NB_ARTICLES_PER_PAGE=2 : number of articles per pages

# Articles
Articles are created in markdown format and stored in `articles` directory

# RUN
`python3 website.py`

