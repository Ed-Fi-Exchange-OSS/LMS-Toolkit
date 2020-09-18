from dotenv import load_dotenv
from lib import users

load_dotenv()

users = users.listUsers()
print(users)
