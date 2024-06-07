from sqlalchemy.orm import Session
from app.models import User
from app.schema import User_Create
import hashlib 

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def hash_password(pw):
    pw_bytes = pw.encode('utf-8')
    sha256_hash = hashlib.sha256()

    sha256_hash.update(pw_bytes)
    return sha256_hash.hexdigest()

def create_user(db:Session, userdb:User_Create):
    #SHA256으로 해싱
    userdb.password = hash_password(userdb.password)

    if get_user(db, userdb.password) == userdb.password:
        return False

    #db 저장
    db_user = User(**userdb.dict())
    db.add(db_user)
    print(db_user)
    db.commit()
    db.refresh(db_user)

    return True

def delete_user(db: Session, userdb: User):
    db.delete(userdb)
    db.commit()
