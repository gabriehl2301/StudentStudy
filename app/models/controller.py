import hashlib
import os
from app import login, db
from sqlalchemy import select
from .schema import User

def hash_password(password: str) -> str: 
    salt = os.urandom(16) # Generate a 16byte salt 
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    pwd_hash = salt + pwd_hash #Prepend the salt to the hash for storgae 
    return pwd_hash.hex()

def verify_password(stored_password: str, provided_password: str ) ->bool:
    salt = bytes.fromhex(
        stored_password[:32]
) # First 16 bytes are the salt 32 hex
    actual_password = bytes.fromhex(stored_password[32:])
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", provided_password.encode("utf-8"), salt, 100000
    )

    return pwd_hash == actual_password

@login.user_loader
def get_user_by_id(id:int):
    stmnt = select(User).where(User.id==id)
    user = db.session.execute(stmnt).scalar()
    return user