class Config:
    DB_USERNAME = 'root'
    DB_PASSWORD = '9900w16a'
    DB_HOST = 'localhost'
    DB_NAME = '9900'
    # 构建SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
