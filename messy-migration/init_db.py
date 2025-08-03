from models import Base
from db import engine
from utils import hash_password
from models import User
from db import session

Base.metadata.create_all(engine)

# Sample users
users = [
    ("John Doe", "john@example.com", "password123"),
    ("Jane Smith", "jane@example.com", "secret456"),
    ("Bob Johnson", "bob@example.com", "qwerty789"),
]

for name, email, pw in users:
    session.add(User(name=name, email=email, password=hash_password(pw)))

session.commit()
print("Database initialized with sample data.")
