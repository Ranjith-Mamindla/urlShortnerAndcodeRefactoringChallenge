from db import session
from models import User
from utils import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

def create_user(data):
    hashed_pw = hash_password(data.password)
    user = User(name=data.name, email=data.email, password=hashed_pw)
    try:
        session.add(user)
        session.commit()
        return user.id
    except IntegrityError:
        session.rollback()
        raise ValueError("Email already exists")

def get_all_users():
    return session.query(User).all()

def get_user_by_id(user_id):
    return session.query(User).filter(User.id == user_id).first()

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

def update_user(user_id, name, email):
    user = get_user_by_id(user_id)
    if user:
        user.name = name
        user.email = email
        session.commit()
        return True
    return False

def search_users(name):
    return session.query(User).filter(User.name.ilike(f'%{name}%')).all()

def login_user(data):
    user = session.query(User).filter(User.email == data.email).first()
    if user and verify_password(data.password, user.password):
        return user
    return None
