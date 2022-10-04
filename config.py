# database configuration
# fill up your own database information
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = ''
USERNAME = ''
PASSWORD = ''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = ''  # set up your own secret key

# Email configuration, you need to set your own email address
# Here the tencent QQ mail service is applied, POP3/SMTP
# you can use your own preferred mail service provider
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True  # when the app is used, set it to False
MAIL_USERNAME = ''  # qq email address
MAIL_PASSWORD = ''  # your pop3/smtp service password
MAIL_DEFAULT_SENDER = ''  # your default sender, usually it is email address aforesaid
