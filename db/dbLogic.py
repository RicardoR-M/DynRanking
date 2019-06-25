# from datetime import date

import json

from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy import create_engine, select, and_, not_

import util.config as config
from util.CalificacionV2 import calcula_nota


class EngineBase:
    def __init__(self):
        driver = "mssql+pymssql"
        user = "sa"
        pwd = "***REMOVED***"
        ip = "192.168.3.100"
        db = "WEB_CALIDAD"
        source = f"{driver}://{user}:{pwd}@{ip}/{db}"
        metadata = self.get_tables_metadata()
        self.engine = create_engine(source, echo=False)
        self.items = metadata.tables["TB_TECNICO"]

    @staticmethod
    def get_tables_metadata():
        metadata = MetaData()

        Table(
            "TB_TECNICO",
            metadata,
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
        return metadata

    def pedido(self):
        s = select([self.items]).where(
            and_(self.items.c.MesMonitoreo == "Junio", self.items.c.TipoEvaluacion == config.perfil_evaluador(),
                 not_(self.items.c.Asesor.like('E3%'))))
        rp = self.engine.execute(s)

        csr_notas = {}

        for _ in rp:
            nota = round(calcula_nota(_.values()), 2)

            if _.Asesor in csr_notas:
                csr_notas[_.Asesor]['notas'] += " / " + str(nota)
                csr_notas[_.Asesor]['sumatoria'] = round(csr_notas[_.Asesor]['sumatoria'] + nota, 2)
                csr_notas[_.Asesor]['q'] += 1
                csr_notas[_.Asesor]['promedio'] = round(csr_notas[_.Asesor]['sumatoria'] / csr_notas[_.Asesor]['q'], 2)
                csr_notas[_.Asesor]['promedio_color'] = get_bootstrap_bolor(csr_notas[_.Asesor]['promedio'])

            else:
                csr_notas[_.Asesor] = {
                    'csr': _.Asesor,
                    'super': _.Supervisor,
                    'notas': str(nota),
                    'sumatoria': nota,
                    'q': 1,
                    'promedio': nota,
                    'promedio_color': get_bootstrap_bolor(nota)
                }

        csr_notas = list(csr_notas.values())
        csr_notas.sort(key=lambda k: k['promedio'], reverse=True)
        return csr_notas


def get_bootstrap_bolor(n):
    if n >= 80.0:
        color = 'bg-success'
    elif n >= 75.0:
        color = 'bg-warning text-secondary'
    else:
        color = 'bg-danger'
    return color


if __name__ == "__main__":
    print(json.dumps(EngineBase().pedido(), indent=4))
