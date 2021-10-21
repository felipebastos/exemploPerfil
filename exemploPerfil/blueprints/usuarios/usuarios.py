from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from sqlalchemy.exc import IntegrityError

from exemploPerfil.ext.database import db
from exemploPerfil.blueprints.usuarios.models import Usuario


bp = Blueprint(
    "usuarios", __name__, url_prefix="/usuarios", template_folder="templates"
)


@bp.route("/")
def root():
    todos = Usuario.query.all()

    return render_template("usuarios/index.html", usuarios=todos)


@bp.route("/novo")
def novo():
    return render_template("usuarios/novo.html")


@bp.post("/add")
def adicionar():
    novoNome = request.form["nome"]

    novo = Usuario()
    novo.nome = novoNome

    db.session.add(novo)
    db.session.commit()

    return redirect(url_for('usuarios.root'))


@bp.get("/editar/<id>")
def editar(id):
    aMudar = Usuario.query.get(id)

    return render_template("usuarios/edicao.html", quem=aMudar)


@bp.post("/edita")
def atualiza():
    idPraAtualizar = request.form["id"]
    nomeNovo = request.form["nome"]

    quem = Usuario.query.get(idPraAtualizar)
    quem.nome = nomeNovo

    try:
        db.session.add(quem)
        db.session.commit()
    except IntegrityError:
        flash("O nome já é utilizado por alguém.")
        return redirect(url_for('usuarios.editar', id=idPraAtualizar))    

    return redirect(url_for('usuarios.root'))


def init_app(app):
    app.register_blueprint(bp)
