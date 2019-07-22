import os

basedir = os.path.abspath(os.path.dirname(__file__))


def q_max_evas():
    return 6


def perfil_calidad():
    return 'Monitoreo Calidad_Dynamicall'


def perfil_cruzado_mdy():
    return 'Cruzado'


def get_total_levels():
    return 8


def get_pesos_tec():
    tec = (1, 2, 2, 2, 1, 5, 4, 10, 4, 4, 22, 0, 0, 0, 0, 0, 0, 0, 7, 2, 15, 3, 3, 3, 2, 2, 3, 3)
    return tec


def get_pesos_adm():
    adm = (1, 2, 2, 2, 1, 3, 4, 10, 3, 2, 3, 2, 2, 14, 0, 0, 0, 2, 2, 2, 2, 5, 2, 15, 3, 3, 3, 2, 2, 3, 0, 3)
    return adm


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pymssql://sa:***REMOVED***@192.168.3.100/WEB_CALIDAD'
    SQLALCHEMY_BINDS = {
        'inde': 'mssql+pymssql://readonly:readonly@192.168.3.100/WEB_CALIDAD'
    }
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'connect_args': {'login_timeout': 2}
    # }
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    DEBUG = True


config = {
    'dev': DevConfig,
    'test': TestConfig
}
