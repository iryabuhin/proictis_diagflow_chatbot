from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app_pkg_path = os.path.join(basedir, 'app')

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'dev'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', b',asdml9a8h12n')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASEDIR = basedir

    BITLY_API_TOKEN = os.environ.get('BITLY_API_TOKEN')

    VK_COMMUNITY_TOKEN = os.environ.get('VK_COMMUNITY_TOKEN')
    VK_APP_ID = int(os.environ.get('VK_APP_ID'))
    VK_APP_CLIENT_SECRET = os.environ.get('VK_APP_CLIENT_SERCRET')
    VK_APP_SERVICE_KEY = os.environ.get('VK_APP_SERVICE_KEY')
    VK_CONFIRMATION = os.environ.get('VK_CONFIRMATION')

    TELEGRAM_TOKEN_INFORMATION_MESSAGE = os.environ.get('TELEGRAM_TOKEN_INFORMATION_MESSAGE')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID_INFORMATION_MESSAGE = os.environ.get('CHAT_ID_INFORMATION_MESSAGE')

    PROJECT_ID = os.environ.get('PROJECT_ID')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

