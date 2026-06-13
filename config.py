class Config:
    SECRET_KEY = "gizli_anahtar"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:fdm3535@localhost/inventory_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False