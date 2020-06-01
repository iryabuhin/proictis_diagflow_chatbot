import sys
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from bitlyshortener import Shortener
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.join('app', 'commands')))

load_dotenv()

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

url_shortener = Shortener(tokens=[app.config['BITLY_API_TOKEN']], max_cache_size=256)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app._vk import VkAPI_
vk = VkAPI_(
    app_token=app.config['VK_APP_SERVICE_KEY'],
    app_id=app.config['VK_APP_ID'],
    group_token=app.config['VK_COMMUNITY_TOKEN'],
    client_secret=app.config['VK_APP_CLIENT_SECRET']
)

from app import models
