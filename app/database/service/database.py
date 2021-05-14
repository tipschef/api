from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common.service.secret_manager_service import get_secret_manager_service

secret_manager_service = get_secret_manager_service()
secret_content = secret_manager_service.get_secret_json()
DATABASE_NAME = 'tipschef'

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{secret_content.get("mysql_account")}:{secret_content.get("mysql_password")}@{secret_content.get("mysql_hostname")}/{DATABASE_NAME}?unix_socket=/cloudsql/{secret_content.get("mysql_connection_name")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
