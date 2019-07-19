from datetime import datetime

from flask import render_template
from sqlalchemy import func, desc

from app import db
from app.config import perfil_calidad, perfil_cruzado_mdy, get_total_levels
from app.dbase.dbLogic import BaseRanking
from app.models import WebCalidad, EvaluacionesTEC, Nomina
from app.util.CalificacionV2 import calcula_nota
from . import index_blueprint

ranking = BaseRanking()


@index_blueprint.route('/')
def index():
    return render_template('baseDashboard.html')


@index_blueprint.route('/adm')
def adm():
    return 'ADM'


@index_blueprint.route('/inde')
def load_inde():
    # time_start = time.time()
    # for u in WebCalidad.query.all():
    #     # print(u.__dict__)
    #     # print(WebCalidad.row2dict(u))
    #     d.append(u.__dict__)
    # time_end = time.time()
    # print(f'Tiempo: {time_end-time_start}')
    # pprint(d[0])
    # db.session.query(EvaluacionesTEC(TipoEvaluacion='Monitoreo Calidad_Dynamicall')).delete()
    EvaluacionesTEC.query.filter_by(TipoEvaluacion=perfil_calidad()).delete()
    for row in WebCalidad.query.filter_by(TipoEvaluacion=perfil_calidad()):
        row_dict = row.__dict__
        row_dict.pop('_sa_instance_state', None)
        row_dict['Calificacion'] = calcula_nota(row_dict, 'TEC')
        db.session.add(EvaluacionesTEC(**row_dict))
    db.session.commit()


@index_blueprint.route('/tec')
def tec():
    lista = []
    evaluaciones = db.session.query(EvaluacionesTEC.Asesor,
                                    func.round(func.avg(EvaluacionesTEC.Calificacion), 2).label('Promedio_global')) \
        .group_by(EvaluacionesTEC.Asesor).order_by(desc('Promedio_global')).all()

    evaluaciones_cant = len(evaluaciones)

    for i, row in enumerate(evaluaciones):
        # lista[row.Asesor] = dict(zip(row.keys(), row))  # Tuple result to dict
        nota_interno = tuple_to_value(db.session.query(func.round(func.avg(EvaluacionesTEC.Calificacion), 2).label('Interno')
                                                       ).filter_by(Asesor=row.Asesor,
                                                                   TipoEvaluacion=perfil_calidad()).first())
        nota_cruzado = tuple_to_value(db.session.query(func.round(func.avg(EvaluacionesTEC.Calificacion), 2).label('Cruzado')
                                                       ).filter_by(Asesor=row.Asesor,
                                                                   TipoEvaluacion=perfil_cruzado_mdy()).first())
        lista.append({
            'asesor': row.Asesor,
            'promedio_global': row.Promedio_global,
            'interno': nota_interno,
            'cruzado': nota_cruzado,
            'nombre': tuple_to_value(db.session.query(Nomina.nombre).filter_by(e=row.Asesor).first()),
            'supervisor': tuple_to_value(db.session.query(Nomina.supervisor).filter_by(e=row.Asesor).first()),
            'pbar_interno': get_bootstrap_progressbar(nota_interno),
            'pbar_cruzado': get_bootstrap_progressbar(nota_cruzado),
            'level': get_level_img(i + 1, evaluaciones_cant)
        })
    return render_template("ranking.html",
                           RANKING_RES=lista,
                           SIZE=evaluaciones_cant,
                           ctime=datetime.utcnow())


def tuple_to_value(tup):
    if tup is None:
        return None
    else:
        return tup[0]


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def get_bootstrap_progressbar(n):
    if n is None:
        return ''

    if n >= 80.0:
        pbar = 'bg-success'
    elif n >= 75.0:
        pbar = 'bg-warning text-secondary'
    else:
        pbar = 'bg-danger'
    return pbar


def get_level_img(rank, total):
    segment = int(total / get_total_levels())

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
