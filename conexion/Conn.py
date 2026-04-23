import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class Conn:
    @staticmethod
    def mysql():
        HOST = os.environ.get('HOST')
        USER = os.environ.get('USER')
        PASSWORD = os.environ.get('PASSWORD')
        DATABASE = os.environ.get('DATABASE')

        try:
            db = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
            )
            
            print(f"Conectado a la base de datos")
            return db

        except Exception as e:
            print(f"ERROR AL CONECTAR: {e}")
            return None
            
