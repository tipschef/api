from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.service.secret_manager_service import get_secret_manager_service

# SQLALCHEMY_DATABASE_URL = "mysql:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:@localhost/tipschef"
secret_manager_service = get_secret_manager_service()
secret_content = secret_manager_service.get_secret_json()

SQLALCHEMY_DATABASE_URL = f'mysql+mysqldb://{secret_content.get("mysql_id")}:{secret_content.get("mysql_password")}@34.78.72.151/tipschef'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()