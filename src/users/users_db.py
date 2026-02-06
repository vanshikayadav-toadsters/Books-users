from sqlmodel import Session, select
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate
from src.auth.utils import generate_password_hash


# CREATE USER
def create_user(session: Session, user_data: UserCreate):
    # Hash the password before creating the user
    password_hash = generate_password_hash(user_data.password)
    user_data_dict = user_data.dict()
    user_data_dict.pop('password')  # Remove the password field
    user_data_dict['password_hash'] = password_hash  # Add the hashed password
    
    user = User(**user_data_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# GET ALL USERS
def get_users(session: Session):
    statement = select(User)
    return session.exec(statement).all()


# UPDATE USER
def update_user(session: Session, user_id, user_data: UserUpdate):
    user = session.get(User, user_id)
    if not user:
        return None

    for key, value in user_data.dict(exclude_unset=True).items():
        if key == 'password' and value is not None:
            # Hash the password if it's being updated
            setattr(user, 'password_hash', generate_password_hash(value))
        else:
            setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# DELETE USER
def delete_user(session: Session, user_id):
    user = session.get(User, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
