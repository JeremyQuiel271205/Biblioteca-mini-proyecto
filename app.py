from flask import *
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

print(os.environ.get('SECRET_KEY'))