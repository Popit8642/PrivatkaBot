from .database import session_factory
from .models import UsersOrm


def insert_user(username: str) -> bool:
    with session_factory() as session:
        user = session.query(UsersOrm).filter(UsersOrm.username == username).first()
        return user is not None
    
def is_admin(user_id: int) -> bool:
    with session_factory() as session:
        user = session.query(UsersOrm).filter(UsersOrm.id == user_id).first()
        return user is not None and user.admin
    
def get_admins():
    with session_factory() as session:
        admins = session.query(UsersOrm.id).filter(UsersOrm.admin == True).all()
        return [admin[0] for admin in admins]