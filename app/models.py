from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password no es un atributo leible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Nomina(db.Model):
    __tablename__ = 'nomina'
    id = db.Column(db.Integer, primary_key=True)
    e = db.Column(db.String(10), index=True, nullable=False)
    nombre = db.Column(db.String(100))
    supervisor = db.Column(db.String(100))

    def __repr__(self):
        return '<Nomina %r>' % self.e


class Cruzado(db.Model):
    __tablename__ = 'cruzado'
    id = db.Column(db.Integer, primary_key=True)
    e = db.Column(db.String(10), index=True, nullable=False)
    sumatoria = db.Column(db.Float(precision='3,2'))
    q = db.Column(db.Integer)

    def __repr__(self):
        return '<Cruzado %r>' % self.e


class Interno(db.Model):
    __tablename__ = 'interno'
    id = db.Column(db.Integer, primary_key=True)
    e = db.Column(db.String(10), index=True, nullable=False)
    sumatoria = db.Column(db.Float(precision='3,2'))
    q = db.Column(db.Integer)

    def __repr__(self):
        return '<Interno %r>' % self.e


class WebCalidad(db.Model):
    __bind_key__ = 'inde'
    __tablename__ = 'TB_TECNICO'
    id = db.Column(db.Integer, primary_key=True)
    SaludaCliente = db.Column(db.String(150))
    SeDirigePorNombre = db.Column(db.String(150))
    InteractuaConCliente = db.Column(db.String(150))
    EvitaUsoTecnicismos = db.Column(db.String(150))
    SeDespideComoIndicaManual = db.Column(db.String(150))
    ValidaConsultaTransaccion = db.Column(db.String(150))
    RealizaPreguntasPrecision = db.Column(db.String(150))
    ValidaMotivoReal = db.Column(db.String(150))
    ValidaAtencionPrevia = db.Column(db.String(150))
    ValidaCES = db.Column(db.String(150))
    AtencionPasoAPaso = db.Column(db.String(150))
    SolicitaDNIRUC = db.Column(db.String(150))
    ValidaTRACER = db.Column(db.String(150))
    VerificaWebAverias = db.Column(db.String(150))
    VerificaParametrosServicios = db.Column(db.String(150))
    ProblemasInternetIngresaEMTA = db.Column(db.String(150))
    ProblemasTelefoniaIngresaJANUS = db.Column(db.String(150))
    ProblemasInternetSmarTV = db.Column(db.String(150))
    ExplicacionBrindadaCorresponde = db.Column(db.String(150))
    ValidaConClienteInformacion = db.Column(db.String(150))
    EjecutaAccionesAplicativos = db.Column(db.String(150))
    SeTipificaSIACSGA = db.Column(db.String(150))
    NotasPlantillaTipificacion = db.Column(db.String(150))
    SeTipificaEnSIAC = db.Column(db.String(150))
    EvitaComentariosNegativos = db.Column(db.String(150))
    EvitaPalabraSoeces = db.Column(db.String(150))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(150))
    MotivoRealNecesidad = db.Column(db.String(150))
    TipoEvaluacion = db.Column(db.String(250))
    MesMonitoreo = db.Column(db.String(250))
    Asesor = db.Column(db.String(250))
    SN = db.Column(db.String(250))
    Cbo_estado = db.Column(db.String(150))  # Motivo de llamada
    Nivel_1 = db.Column(db.String(250))  # FCR
    DetalleLlamada = db.Column(db.String(2000))
    ObservacionesAspectoMejora = db.Column(db.String(2000))


class EvaluacionesTEC(db.Model):
    __tablename__ = 'evaluaciones_tec'
    id = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.String(250), index=True)
    MesMonitoreo = db.Column(db.String(250))
    TipoEvaluacion = db.Column(db.String(250))
    Asesor = db.Column(db.String(250), index=True)
    Cbo_estado = db.Column(db.String(150))  # Motivo de llamada
    Nivel_1 = db.Column(db.String(250))  # FCR
    DetalleLlamada = db.Column(db.String(2000))
    ObservacionesAspectoMejora = db.Column(db.String(2000))
    Calificacion = db.Column(db.Float(precision='3,2'))
    # bloque 1
    SaludaCliente = db.Column(db.String(150))
    SeDirigePorNombre = db.Column(db.String(150))
    InteractuaConCliente = db.Column(db.String(150))
    EvitaUsoTecnicismos = db.Column(db.String(150))
    SeDespideComoIndicaManual = db.Column(db.String(150))
    # bloque 2
    ValidaConsultaTransaccion = db.Column(db.String(150))
    RealizaPreguntasPrecision = db.Column(db.String(150))
    ValidaMotivoReal = db.Column(db.String(150))
    ValidaAtencionPrevia = db.Column(db.String(150))
    # bloque 3
    ValidaCES = db.Column(db.String(150))
    AtencionPasoAPaso = db.Column(db.String(150))
    SolicitaDNIRUC = db.Column(db.String(150))
    ValidaTRACER = db.Column(db.String(150))
    VerificaWebAverias = db.Column(db.String(150))
    VerificaParametrosServicios = db.Column(db.String(150))
    ProblemasInternetIngresaEMTA = db.Column(db.String(150))
    ProblemasTelefoniaIngresaJANUS = db.Column(db.String(150))
    ProblemasInternetSmarTV = db.Column(db.String(150))
    ExplicacionBrindadaCorresponde = db.Column(db.String(150))
    ValidaConClienteInformacion = db.Column(db.String(150))
    # bloque 4
    EjecutaAccionesAplicativos = db.Column(db.String(150))
    SeTipificaSIACSGA = db.Column(db.String(150))
    NotasPlantillaTipificacion = db.Column(db.String(150))
    SeTipificaEnSIAC = db.Column(db.String(150))
    # bloque 5
    EvitaComentariosNegativos = db.Column(db.String(150))
    EvitaPalabraSoeces = db.Column(db.String(150))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(150))
    # bloque 6
    MotivoRealNecesidad = db.Column(db.String(150))
