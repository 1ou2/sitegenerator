# Deploy to remote server
import subprocess
import os
from dotenv import load_dotenv

def deploy():
    load_dotenv()
    
    server = os.getenv("SERVER")
    site_dir = os.getenv("SITE_DIR")
    html_dir = os.getenv("HTML_DIR", "html")
    
    if not server or not site_dir:
        print("Error: SERVER and SITE_DIR must be set in .env file")
        return
    
    # Backup remote html directory
    backup_cmd = f"ssh ubuntu@{server} 'cd {site_dir} && mv html html_backup_$(date +%Y%m%d_%H%M%S)'"
    subprocess.run(backup_cmd, shell=True)
    
    # Copy local html to remote
    copy_cmd = f"scp -r {html_dir} ubuntu@{server}:{site_dir}/"
    subprocess.run(copy_cmd, shell=True)
    
    print(f"Deployment completed to {server}:{site_dir}")

if __name__ == "__main__":
    deploy()
    