from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Configure SQLALCHEMY DB
#SQLALCHEMY_DATABASE_URL = "sqlite:///./todoapp.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#Configure Postgres DB
#DATABASE_URL = "postgresql://postgres:1916@localhost:5432/todoapp"
DATABASE_URL = "postgresql://todoapp_vl5v_user:yuaPYie5z2hLzCyVwvPg1otRAxhZORKI@dpg-d9o5netaeets73d53r7g-a.ohio-postgres.render.com/todoapp_vl5v"

#Configure Mysql DB
#DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/todoapp"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()