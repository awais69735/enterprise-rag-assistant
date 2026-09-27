from app.auth.users import USERS

def authenticate_user(username:str, password:str):
    user= USERS.get(username)

    if not user:
        return None

    if user["password"] != password:
        return None

    return {
        "username":username,
        "role": user["role"]
    }