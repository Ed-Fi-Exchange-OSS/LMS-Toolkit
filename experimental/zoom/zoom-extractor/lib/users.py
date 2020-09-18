from lib.zoomRequest import get


def listUsers():
    users = get("/users")
    # here we should handle the pagination and return a list of all users
    return users["users"]
