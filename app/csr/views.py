from pprint import pprint

from flask import render_template
from sqlalchemy import exists

from app import db
from . import csr_blueprint
from ..models import EvaluacionesTEC, EvaluacionesADM


@csr_blueprint.route('/<e>')
def csr(e):
    existe_tec = db.session.query(exists().where(EvaluacionesTEC.Asesor == e.upper())).scalar()
    existe_adm = db.session.query(exists().where(EvaluacionesADM.Asesor == e.upper())).scalar()
    if not (existe_tec or existe_adm):
        return 'No se encontro nada'

    if existe_tec:
        base = EvaluacionesTEC
        skill = 'tec'
    else:
        base = EvaluacionesADM
        skill = 'adm'

    # resultado = db.session.query(base.TipoEvaluacion, base.SN, base.Calificacion).filter_by(Asesor=e).all()
    resultado = base.query.filter_by(Asesor=e).all()
    return render_template('csr/tabla.html', tabla=resultado, asesor=e, skill=skill)


@csr_blueprint.route('sn/<sn>')
def get_sn_data(sn):
    existe_tec = db.session.query(exists().where(EvaluacionesTEC.SN == sn)).scalar()

    if existe_tec:
        base = EvaluacionesTEC
    else:
        base = EvaluacionesADM

    resultado = base.query.filter_by(SN=sn).all()

    print(resultado[0])

    return 'SN'
