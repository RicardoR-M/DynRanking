# from datetime import date
from _mssql import MSSQLDriverException
from sqlalchemy import MetaData, Table, Column, String, Integer, Float
from sqlalchemy import create_engine, select, and_, not_
from sqlalchemy.exc import OperationalError

from app import config
from app.util.CalificacionV2 import calcula_nota


class BaseRanking:
    def __init__(self):
        self.local = False
        self.size = 0
        driver = "mssql+pymssql"
        user = "sa"
        pwd = "***REMOVED***"
        ip = "192.168.3.100"
        db = "WEB_CALIDAD"
        source = f"{driver}://{user}:{pwd}@{ip}/{db}"
        metadata_inde = MetaData()
        metadata_local = MetaData()
        self.items = Table("TB_TECNICO", metadata_inde,
                           Column("SaludaCliente", String(150)),
                           Column("SeDirigePorNombre", String(150)),
                           Column("InteractuaConCliente", String(150)),
                           Column("EvitaUsoTecnicismos", String(150)),
                           Column("SeDespideComoIndicaManual", String(150)),
                           Column("ValidaConsultaTransaccion", String(150)),
                           Column("RealizaPreguntasPrecision", String(150)),
                           Column("ValidaMotivoReal", String(150)),
                           Column("ValidaAtencionPrevia", String(150)),
                           Column("ValidaCES", String(150)),
                           Column("AtencionPasoAPaso", String(150)),
                           Column("SolicitaDNIRUC", String(150)),
                           Column("ValidaTRACER", String(150)),
                           Column("VerificaWebAverias", String(150)),
                           Column("VerificaParametrosServicios", String(150)),
                           Column("ProblemasInternetIngresaEMTA", String(150)),
                           Column("ProblemasTelefoniaIngresaJANUS", String(150)),
                           Column("ProblemasInternetSmarTV", String(150)),
                           Column("ExplicacionBrindadaCorresponde", String(150)),
                           Column("ValidaConClienteInformacion", String(150)),
                           Column("EjecutaAccionesAplicativos", String(150)),
                           Column("SeTipificaSIACSGA", String(150)),
                           Column("NotasPlantillaTipificacion", String(150)),
                           Column("SeTipificaEnSIAC", String(150)),
                           Column("EvitaComentariosNegativos", String(150)),
                           Column("EvitaPalabraSoeces", String(150)),
                           Column("EscuchaClienteSinInterrumpirlo", String(150)),
                           Column("MotivoRealNecesidad", String(150)),
                           Column("TipoEvaluacion", String(250)),
                           Column("MesMonitoreo", String(250)),
                           Column("Asesor", String(250)),
                           Column("Supervisor", String(250))
                           )

        self.ranking_interno = Table('interno', metadata_local,
                                     Column('id', Integer(), primary_key=True),
                                     Column('e', String(50), index=True, nullable=False),
                                     Column('sumatoria', Float(precision='3,2'), nullable=False),
                                     Column('q', Integer(), nullable=False)
                                     )

        self.rankingCruzado = Table('cruzado', metadata_local,
                                    Column('id', Integer(), primary_key=True),
                                    Column('e', String(50), index=True, nullable=False),
                                    Column('sumatoria', Float(precision='3,2'), nullable=False),
                                    Column('q', Integer(), nullable=False)
                                    )

        self.nomina = Table('nomina', metadata_local,
                            Column('id', Integer(), primary_key=True),
                            Column('e', String(50), index=True, nullable=False),
                            Column('nombre', String(100), nullable=False),
                            Column('supervisor', String(100), nullable=False)
                            )

        self.engineInde = create_engine(source, connect_args={'login_timeout': 2}, echo=False)
        self.engineLocal = create_engine('sqlite:///local.db', echo=False)
        metadata_local.create_all(self.engineLocal)

    def get_interno(self):
        interno = {}
        self.local = False
        conn = ''

        try:
            conn = self.engineInde.connect()
        except OperationalError:
            self.local = True
        except MSSQLDriverException:
            self.local = True

        if not self.local:
            s = select([self.items]).where(
                and_(self.items.c.MesMonitoreo == "Junio", self.items.c.TipoEvaluacion == config.perfil_evaluador(),
                     not_(self.items.c.Asesor.like('E3%'))))
            # rp = self.engineInde.execute(s)
            rp = conn.execute(s)

            for _ in rp:
                nota = round(calcula_nota(_.values()), 2)

                if _.Asesor in interno:
                    interno[_.Asesor]['sumatoria'] = round(interno[_.Asesor]['sumatoria'] + nota, 2)
                    interno[_.Asesor]['q'] += 1
                else:
                    interno[_.Asesor] = {
                        'e': _.Asesor,
                        'sumatoria': nota,
                        'q': 1
                    }
            self.insert_interno(list(interno.values()))
        else:
            s = select([self.ranking_interno.c.e,
                        self.ranking_interno.c.sumatoria,
                        self.ranking_interno.c.q])
            rp = self.engineLocal.execute(s)

            for _ in rp:
                interno[_['e']] = dict(_)

        return interno

    def insert_interno(self, lista):
        self.engineLocal.execute(self.ranking_interno.delete())
        ins = self.ranking_interno.insert()
        self.engineLocal.execute(ins, lista)

    def insert_cruzado(self, lista):
        self.engineLocal.execute(self.rankingCruzado.delete())
        ins = self.rankingCruzado.insert()
        self.engineLocal.execute(ins, lista)

    def get_cruzado(self):
        cruzado = {}

        s = select([self.rankingCruzado.c.e,
                    self.rankingCruzado.c.sumatoria,
                    self.rankingCruzado.c.q])
        rp = self.engineLocal.execute(s)

        for _ in rp:
            cruzado[_['e']] = dict(_)
        return cruzado

    def insert_nomina(self, lista):
        self.engineLocal.execute(self.nomina.delete())
        s = self.nomina.insert()
        self.engineLocal.execute(s, lista)

    def get_nomina(self):
        nomina = {}
        s = select([self.nomina.c.e,
                    self.nomina.c.nombre,
                    self.nomina.c.supervisor])
        rp = self.engineLocal.execute(s)

        for _ in rp:
            nomina[_['e']] = dict(_)
        return nomina

    def get_status_local(self):
        """ Devuelve un bool si se esta usando la base local (True) o MSSQL (False) """
        return self.local

    def get_todo(self):
        ranking = {}
        nomina = self.get_nomina()
        interno = self.get_interno()
        cruzado = self.get_cruzado()

        # Carga la data interna a ranking
        for _ in interno:
            if _ in ranking:
                ranking[_]['sumatoria_interno'] = interno[_]['sumatoria']
                ranking[_]['q_interno'] = interno[_]['q']
            else:
                ranking[_] = {
                    'e': interno[_]['e'],
                    'sumatoria_interno': interno[_]['sumatoria'],
                    'q_interno': interno[_]['q'],
                    'sumatoria_cruzado': None
                }
        # Carga la data de cruzado a ranking
        for _ in cruzado:
            if _ in ranking:
                ranking[_]['sumatoria_cruzado'] = cruzado[_]['sumatoria']
                ranking[_]['q_cruzado'] = cruzado[_]['q']
            else:
                ranking[_] = {
                    'e': cruzado[_]['e'],
                    'sumatoria_cruzado': cruzado[_]['sumatoria'],
                    'q_cruzado': cruzado[_]['q'],
                    'sumatoria_interno': None
                }

        # Calcula los promedios
        for _ in ranking:
            # Calcula el promedio interno y cruzado
            if ranking[_]['sumatoria_interno'] is None:
                ranking[_]['promedio_interno'] = '-'
            else:
                ranking[_]['promedio_interno'] = round(ranking[_]['sumatoria_interno'] / ranking[_]['q_interno'], 2)

            if ranking[_]['sumatoria_cruzado'] is None:
                ranking[_]['promedio_cruzado'] = '-'
            else:
                ranking[_]['promedio_cruzado'] = round(ranking[_]['sumatoria_cruzado'] / ranking[_]['q_cruzado'], 2)

            # Setea el progress bar de los promedios interno y cruzado
            ranking[_]['pbar_interno'] = get_bootstrap_progressbar(ranking[_]['promedio_interno'])
            ranking[_]['pbar_cruzado'] = get_bootstrap_progressbar(ranking[_]['promedio_cruzado'])

            # Calcula promedio global
            if ranking[_]['promedio_interno'] == '-':
                ranking[_]['promedio_global'] = ranking[_]['promedio_cruzado']
            elif ranking[_]['promedio_cruzado'] == '-':
                ranking[_]['promedio_global'] = ranking[_]['promedio_interno']
            else:
                ranking[_]['promedio_global'] = round((ranking[_]['sumatoria_interno'] + ranking[_]['sumatoria_cruzado'])
                                                      / (ranking[_]['q_interno'] + ranking[_]['q_cruzado']), 2)

            # Asigna Nombre y supervisor
            if _ in nomina:
                ranking[_]['nombre'] = nomina[_]['nombre']
                ranking[_]['supervisor'] = nomina[_]['supervisor']
            else:
                ranking[_]['nombre'] = _
                ranking[_]['supervisor'] = '-'

        ranking = list(ranking.values())
        ranking.sort(key=lambda k: k['promedio_global'], reverse=True)

        # Asigna levels despues de que la lista fue ordenada
        for i, _ in enumerate(ranking):
            _['level'] = get_level_img(i + 1, len(ranking))

        self.size = len(ranking)

        return ranking


def get_bootstrap_progressbar(n):
    if n == '-':
        return ''

    if n >= 80.0:
        pbar = 'bg-success'
    elif n >= 75.0:
        pbar = 'bg-warning text-secondary'
    else:
        pbar = 'bg-danger'

    return pbar


def get_level_img(rank, total):
    segment = int(total / config.get_total_levels())

    if total == 0:
        level = ''
    elif rank == 1:
        level = 'lvl1.png'
    elif rank == 2:
        level = 'lvl2.png'
    elif rank == 3:
        level = 'lvl3.png'
    elif rank <= segment:
        level = 'lvl4.png'
    elif rank <= segment * 2:
        level = 'lvl5.png'
    elif rank <= segment * 3:
        level = 'lvl6.png'
    elif rank <= segment * 4:
        level = 'lvl7.png'
    else:
        level = 'lvl8.png'
    return level


if __name__ == "__main__":
    pass
    # print(json.dumps(BaseRanking().get_interno(), indent=4))
    # print(get_todo())
