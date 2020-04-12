from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'vedant', 'tuwani')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
