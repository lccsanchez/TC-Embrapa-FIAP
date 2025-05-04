from app.database import SessionLocal
from app.database_operations import inserir_usuario
import os

session = SessionLocal()
inserir_usuario(session, os.getenv("usuario"), os.getenv("senha"))
session.close()
