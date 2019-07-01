from flask import Flask, render_template

from db.dbLogic import BaseRanking

app = Flask(__name__)

ranking = BaseRanking()


@app.route('/')
def hello_world():
    return render_template("main.html", RANKING_RES=ranking.get_todo(), LOCAL=ranking.get_status_local(), SIZE=ranking.size)


if __name__ == '__main__':
    app.run(debug=True)
