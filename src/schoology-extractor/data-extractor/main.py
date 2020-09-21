from lib.users import Users
from dotenv import load_dotenv
import os

load_dotenv()

SCHOOLOGY_KEY = os.getenv("SCHOOLOGY_KEY")
SCHOOLOGY_SECRET = os.getenv("SCHOOLOGY_SECRET")

users = Users(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

users.get_all()
