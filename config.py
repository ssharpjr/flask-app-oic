class Config:
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://iqms:iqtest@iqtest'

    @staticmethod
    def init_app(app):
        pass

config = Config
