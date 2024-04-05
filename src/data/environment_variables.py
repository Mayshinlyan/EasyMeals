import os

from dotenv import find_dotenv, load_dotenv

# project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
# dotenv_path = os.path.join(project_dir, '.env')


dotenv_path = "/Users/maylyan/Documents/AI/Project 01/.env"
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
