from flask import Flask, render_template

from db.dbLogic import EngineBase

app = Flask(__name__)
lista = EngineBase()


@app.route('/')
def hello_world():
    return render_template("main.html", RANKING_RES=lista.pedido())


if __name__ == '__main__':
    app.run(debug=True)
