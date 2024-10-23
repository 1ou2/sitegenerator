import markdown,yaml
import os,shutil,re
from dotenv import load_dotenv

class Article:
    def __init__(self,md_file_path=""):
        self.meta_data = {}
        self.md_content = ""
        self.md_file_path = md_file_path
        if md_file_path:
            self.parse_markdown_article()

    def __repr__(self):
        return f"Article: {self.meta_data}"
    
    def check_metadata(self):
        """Check if required metadata fields are present"""
        required_fields = ["title", "date", "tags"]
        for field in required_fields:
            if field not in self.meta_data:
                return False
            
        # create html_tags field
        # <span class="meta-box tag-1">Programming</span>, <span class="meta-box tag-2">Python</span>
        self.html_tags = "".join([f'<span class="meta-box tag-{i+1}">{tag}</span>' for i, tag in enumerate(self.tags)])
        return True
    
    def get_md_content(self):
        return self.md_content

    def parse_metadata(self):
        self.title = self.meta_data.get("title", "")
        self.date = self.meta_data.get("date", "")
        # tags are separated by commas, split the tags string and strip spaces
        self.tags = [t.strip() for t in self.meta_data.get("tags", "").split(",")]

    def parse_markdown_article(self):
        """Parse markdown file, extract meta data and content"""
        self.html = ""
        with open(self.md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Use regex to extract the YAML front matter
            yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
            match = yaml_pattern.match(content)

            if match:
                yaml_content = match.group(1)
                md_content = content[match.end():]
                self.html = markdown.markdown(md_content)
                # Parse YAML content
                try:
                    meta_data = yaml.safe_load(yaml_content)
                except yaml.YAMLError as e:
                    # If YAML parsing fails, try a custom approach
                    # some data contains ':' so we split on the first ':' encountered
                    print(f"Error parsing YAML in {self.md_file_path}: {e}")
                    meta_data = {}
                    for line in yaml_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            value = value.strip()
                            meta_data[key.strip()] = value

            else:
                meta_data = {}
                md_content = content

            self.meta_data = meta_data
            self.md_content = md_content
            self.parse_metadata()

if __name__ == "__main__":
    pass
        