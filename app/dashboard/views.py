from flask import render_template, flash

from app import db
from app.config import perfil_cruzado_mdy
from app.models import Nomina, EvaluacionesTEC
from . import dash_blueprint
from .ExcelToDic import load_nomina, load_cruzado
from ..dashboard.forms import NominaForm, CruzadoForm


@dash_blueprint.route('/nomina', methods=['GET', 'POST'])
def nomina():
    form = NominaForm()
    if form.validate_on_submit():
        f = form.file.data
        nomina_list = load_nomina(f)
        db.session.query(Nomina).delete()
        db.session.execute(Nomina.__table__.insert(), nomina_list)
        db.session.commit()
        flash('Se actualizó la nomina correctamente')
        # return redirect(url_for('index.index'))
    return render_template('dashboard/nomina.html', form=form)


@dash_blueprint.route('/cruzado', methods=['GET', 'POST'])
def cruzado():
    form = CruzadoForm()
    if form.validate_on_submit():
        f = form.file.data
        cruzado_list = load_cruzado(f)
        # db.session.query(EvaluacionesTEC).delete() Borra el contenido de toda la tabla
        EvaluacionesTEC.query.filter_by(TipoEvaluacion=perfil_cruzado_mdy()).delete()
        db.session.execute(EvaluacionesTEC.__table__.insert(), cruzado_list)
        db.session.commit()
        flash('Se actualizaron las notas del informe cruzado')
    return render_template('dashboard/cruzado.html', form=form)
