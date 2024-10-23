import argparse
import os,shutil
from dotenv import load_dotenv
from articles import Article

class Website:
    def __init__(self,md_dir,html_dir):
        self.md_dir = md_dir
        self.html_dir = html_dir
        self.articles = []
        self.articles_by_tag = {}

    # get list of all markdown files
    def get_markdown_files(self):
        md_files = []
        for root, dirs, files in os.walk(self.md_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        return md_files

    # clean html dir
    def clean_html_dir(self):
        # delete html dir
        shutil.rmtree(self.html_dir,ignore_errors=True)
        os.makedirs(self.html_dir)

    def init_html(self):
        self.clean_html_dir()
        # copy md_dir to html_dir  # cp -r md_dir/* html_dir
        shutil.copytree(self.md_dir, self.html_dir, dirs_exist_ok=True)
        # copy assets to html_dir/assets
        assets_dir = os.path.join(self.html_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        shutil.copytree("assets", assets_dir, dirs_exist_ok=True)
        # copy static files to html_dir
        static_dir = os.path.join(self.html_dir)
        os.makedirs(static_dir, exist_ok=True)
        shutil.copytree("static", static_dir, dirs_exist_ok=True)

    def init_articles(self):
        md_files = self.get_markdown_files()
       
        for md_file in md_files:
            article = Article(md_file)
            self.add(article)

        tag_count = {}
        for article in self.articles:
            for tag in article.tags:
                if tag not in tag_count:
                    tag_count[tag] = 0
                tag_count[tag] += 1
        # array of tags in count order from max to min
        self.sorted_tags =  [k for k,v in sorted(tag_count.items(), key=lambda x:x[1],reverse=True)]

    # html article has been created
    def add(self,article):
        self.articles.append(article)

        for tag in article.tags:
            if tag not in self.articles_by_tag:
                self.articles_by_tag[tag] = []
            self.articles_by_tag[tag].append(article)


    def get_top_tags(self,top):
        """ Return the top most used tags """

        return self.sorted_tags[:top]

    def get_template(self,filename):
        template_dir = "templates"
        filename = os.path.join(template_dir, filename)
        with open(filename, 'r') as file:
            return file.read()
    
    # create html file, in html_dir, by transforming the markdown into html
    def generate_html_article(self,article):
        # md files were copied in the html directory, we currently have 
        # html_dir/YYYY/MM/DD/article_dir/article.md
        # we will create html_dir/YYYY/MM/DD/article_dir/article.html
        html_file_path = article.md_file_path.replace(self.md_dir, self.html_dir).replace(".md", ".html")
        # css file path
        # html article is in html_dir/YYYY/MM/DD/article_dir/article.html
        # css file is in html_dir/assets/style.css
        css_path = os.path.join("html","assets", "multicolor.css")
        # variables used in the template
        css_rel_path = os.path.relpath(css_path, os.path.dirname(html_file_path))
        title = article.title
  
        top_tags = self.get_top_tags(10)
        html_top_tags = "".join([f'<span class="meta-box tag-{i+1}">{tag}</span>' for i, tag in enumerate(top_tags)])

        html_template = self.get_template("article.html")
        rendered_html = eval(f"f'''{html_template}'''")
        
        

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

    # generate the main page for the site
    def generate_index(self):
        pass

        

if __name__ == "__main__":
    load_dotenv()
    md_dir = os.getenv("MARKDOWN_DIR")
    html_dir = os.getenv("HTML_DIR")

    www = Website(md_dir, html_dir)
    www.init_html()
    www.init_articles()

    for article in www.articles:
        print(f"Checking metadata for article {article.title}")
        if not article.check_metadata():
            print(f"Error: Invalid metadata")
        else:
            print(f"Generating html for article {article.title}")
            www.generate_html_article(article)
            
