from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class NominaForm(FlaskForm):
    file = FileField('Nómina (*.xlsx, *.xlsm)', validators=[FileRequired(),
                                                            FileAllowed(['xlsx', 'xlsm'], 'Solo se permiten archivos excel!')])
    submit = SubmitField('Upload')


class CruzadoForm(FlaskForm):
    file = FileField('Informe - Cruzado (*.xlsx, *.xlsm)', validators=[FileRequired(),
                                                                       FileAllowed(['xlsx', 'xlsm'],
                                                                                   'Solo se permiten archivos excel!')])
    submit = SubmitField('Upload')
