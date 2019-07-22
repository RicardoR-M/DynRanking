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


class WebCalidadTEC(db.Model):
    __bind_key__ = 'inde'
    __tablename__ = 'TB_TECNICO'
    id = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.String(250))
    TipoEvaluacion = db.Column(db.String(250))
    MesMonitoreo = db.Column(db.String(250))
    Asesor = db.Column(db.String(250))
    Cbo_estado = db.Column(db.String(150))  # Motivo de llamada
    Nivel_1 = db.Column(db.String(250))  # FCR
    DetalleLlamada = db.Column(db.String(2000))
    ObservacionesAspectoMejora = db.Column(db.String(2000))
    SaludaCliente = db.Column(db.String(250))
    SeDirigePorNombre = db.Column(db.String(250))
    InteractuaConCliente = db.Column(db.String(250))
    EvitaUsoTecnicismos = db.Column(db.String(250))
    SeDespideComoIndicaManual = db.Column(db.String(250))
    ValidaConsultaTransaccion = db.Column(db.String(250))
    RealizaPreguntasPrecision = db.Column(db.String(250))
    ValidaMotivoReal = db.Column(db.String(250))
    ValidaAtencionPrevia = db.Column(db.String(250))
    ValidaCES = db.Column(db.String(250))
    AtencionPasoAPaso = db.Column(db.String(250))
    SolicitaDNIRUC = db.Column(db.String(250))
    ValidaTRACER = db.Column(db.String(250))
    VerificaWebAverias = db.Column(db.String(250))
    VerificaParametrosServicios = db.Column(db.String(250))
    ProblemasInternetIngresaEMTA = db.Column(db.String(250))
    ProblemasTelefoniaIngresaJANUS = db.Column(db.String(250))
    ProblemasInternetSmarTV = db.Column(db.String(250))
    ExplicacionBrindadaCorresponde = db.Column(db.String(250))
    ValidaConClienteInformacion = db.Column(db.String(250))
    EjecutaAccionesAplicativos = db.Column(db.String(250))
    SeTipificaSIACSGA = db.Column(db.String(250))
    NotasPlantillaTipificacion = db.Column(db.String(250))
    SeTipificaEnSIAC = db.Column(db.String(250))
    EvitaComentariosNegativos = db.Column(db.String(250))
    EvitaPalabraSoeces = db.Column(db.String(250))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(250))
    MotivoRealNecesidad = db.Column(db.String(250))


class WebCalidadADM(db.Model):
    __bind_key__ = 'inde'
    __tablename__ = 'TB_ADMINISTRATIVO'
    id = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.String(250))
    Asesor = db.Column(db.String(250))
    TipoEvaluacion = db.Column(db.String(250))
    MesMonitoreo = db.Column(db.String(250))
    Cbo_estado = db.Column(db.String(150))  # Motivo de llamada
    Nivel_1 = db.Column(db.String(250))  # FCR
    DetalleLlamada = db.Column(db.String(2000))
    ObservacionesAspectoMejora = db.Column(db.String(2000))
    # Bloque 1
    SaludaCliente = db.Column(db.String(250))
    SeDirigePorNombre = db.Column(db.String(250))
    InteractuaConCliente = db.Column(db.String(250))
    EvitaUsoTecnicismos = db.Column(db.String(250))
    SeDespideComoIndicaManual = db.Column(db.String(250))
    # BLoque 2
    ValidaConsultaTransaccion = db.Column(db.String(250))
    RealizaPreguntasPrecision = db.Column(db.String(250))
    ValidaMotivoReal = db.Column(db.String(250))
    ValidaAtencionPrevia = db.Column(db.String(250))
    # BLoque 3
    SolicitaDNIRUC = db.Column(db.String(250))
    ValidaCES = db.Column(db.String(250))
    ValidaTRACER = db.Column(db.String(250))
    VerificaWebAverias = db.Column(db.String(250))
    AtencionPasoAPaso = db.Column(db.String(250))
    UsaCorrectamenteHerramientaCambioPlan = db.Column(db.String(250))
    ValidaServiciosEMTA = db.Column(db.String(250))
    AsesorUsaHerramientaRecibos = db.Column(db.String(250))
    ConsultaClienteRecepcionRecibo = db.Column(db.String(250))
    OfrecionAfiliacionNotificaciones = db.Column(db.String(250))
    SolicitaNumeroTransaccionPostVenta = db.Column(db.String(250))
    RealizaValidacionesTitularidad = db.Column(db.String(250))
    ExplicacionBrindadaCorresponde = db.Column(db.String(250))
    ValidaConClienteInformacion = db.Column(db.String(250))
    # BLoque 4
    EjecutaAccionesAplicativos = db.Column(db.String(250))
    SeTipificaSIACSGA = db.Column(db.String(250))
    NotasPlantillaTipificacion = db.Column(db.String(250))
    SeTipificaEnSIAC = db.Column(db.String(250))
    # BLoque 5
    EvitaComentariosNegativos = db.Column(db.String(250))
    EvitaPalabraSoeces = db.Column(db.String(250))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(250))
    # BLoque 6
    MotivoRealNecesidad = db.Column(db.String(75))
    VerificaOfertaDisponible = db.Column(db.String(75))


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
    SaludaCliente = db.Column(db.String(5))
    SeDirigePorNombre = db.Column(db.String(5))
    InteractuaConCliente = db.Column(db.String(5))
    EvitaUsoTecnicismos = db.Column(db.String(5))
    SeDespideComoIndicaManual = db.Column(db.String(5))
    # bloque 2
    ValidaConsultaTransaccion = db.Column(db.String(5))
    RealizaPreguntasPrecision = db.Column(db.String(5))
    ValidaMotivoReal = db.Column(db.String(5))
    ValidaAtencionPrevia = db.Column(db.String(5))
    # bloque 3
    ValidaCES = db.Column(db.String(5))
    AtencionPasoAPaso = db.Column(db.String(5))
    SolicitaDNIRUC = db.Column(db.String(5))
    ValidaTRACER = db.Column(db.String(5))
    VerificaWebAverias = db.Column(db.String(5))
    VerificaParametrosServicios = db.Column(db.String(5))
    ProblemasInternetIngresaEMTA = db.Column(db.String(5))
    ProblemasTelefoniaIngresaJANUS = db.Column(db.String(5))
    ProblemasInternetSmarTV = db.Column(db.String(5))
    ExplicacionBrindadaCorresponde = db.Column(db.String(5))
    ValidaConClienteInformacion = db.Column(db.String(5))
    # bloque 4
    EjecutaAccionesAplicativos = db.Column(db.String(5))
    SeTipificaSIACSGA = db.Column(db.String(5))
    NotasPlantillaTipificacion = db.Column(db.String(5))
    SeTipificaEnSIAC = db.Column(db.String(5))
    # bloque 5
    EvitaComentariosNegativos = db.Column(db.String(5))
    EvitaPalabraSoeces = db.Column(db.String(5))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(5))
    # bloque 6
    MotivoRealNecesidad = db.Column(db.String(5))


class EvaluacionesADM(db.Model):
    __tablename__ = 'evaluaciones_adm'
    id = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.String(250), index=True)
    Asesor = db.Column(db.String(250), index=True)
    TipoEvaluacion = db.Column(db.String(250))
    MesMonitoreo = db.Column(db.String(250))
    Cbo_estado = db.Column(db.String(150))  # Motivo de llamada
    Nivel_1 = db.Column(db.String(250))  # FCR
    DetalleLlamada = db.Column(db.String(2000))
    ObservacionesAspectoMejora = db.Column(db.String(2000))
    Calificacion = db.Column(db.Float(precision='3,2'))
    # Bloque 1
    SaludaCliente = db.Column(db.String(5))
    SeDirigePorNombre = db.Column(db.String(5))
    InteractuaConCliente = db.Column(db.String(5))
    EvitaUsoTecnicismos = db.Column(db.String(5))
    SeDespideComoIndicaManual = db.Column(db.String(5))
    # BLoque 2
    ValidaConsultaTransaccion = db.Column(db.String(5))
    RealizaPreguntasPrecision = db.Column(db.String(5))
    ValidaMotivoReal = db.Column(db.String(5))
    ValidaAtencionPrevia = db.Column(db.String(5))
    # BLoque 3
    SolicitaDNIRUC = db.Column(db.String(5))
    ValidaCES = db.Column(db.String(5))
    ValidaTRACER = db.Column(db.String(5))
    VerificaWebAverias = db.Column(db.String(5))
    AtencionPasoAPaso = db.Column(db.String(5))
    UsaCorrectamenteHerramientaCambioPlan = db.Column(db.String(5))
    ValidaServiciosEMTA = db.Column(db.String(5))
    AsesorUsaHerramientaRecibos = db.Column(db.String(5))
    ConsultaClienteRecepcionRecibo = db.Column(db.String(5))
    OfrecionAfiliacionNotificaciones = db.Column(db.String(5))
    SolicitaNumeroTransaccionPostVenta = db.Column(db.String(5))
    RealizaValidacionesTitularidad = db.Column(db.String(5))
    ExplicacionBrindadaCorresponde = db.Column(db.String(5))
    ValidaConClienteInformacion = db.Column(db.String(5))
    # BLoque 4
    EjecutaAccionesAplicativos = db.Column(db.String(5))
    SeTipificaSIACSGA = db.Column(db.String(5))
    NotasPlantillaTipificacion = db.Column(db.String(5))
    SeTipificaEnSIAC = db.Column(db.String(5))
    # BLoque 5
    EvitaComentariosNegativos = db.Column(db.String(5))
    EvitaPalabraSoeces = db.Column(db.String(5))
    EscuchaClienteSinInterrumpirlo = db.Column(db.String(5))
    # BLoque 6
    MotivoRealNecesidad = db.Column(db.String(5))
    VerificaOfertaDisponible = db.Column(db.String(5))
