from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Role

def seed_roles(db: Session):
    existing_roles = db.query(Role).all()
    if existing_roles:
        print("Roles already exists. Skipping seeding")
        return
    
    roles = [
        Role(name="admin", description="Administrator with full access"),
        Role(name="user", description="Default application user"),
    ]

    db.add_all(roles)
    db.commit()
    print("Defaulto roles seeded succesfully.")


def run():
    db = SessionLocal()
    try:
        seed_roles(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()