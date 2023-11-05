from flask import Flask, render_template, request, redirect, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.veiculos
collection_carros = db.carro

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar")
def lista():
    retorno_carros = list(collection_carros.find())
    return render_template("listar.html", carros = retorno_carros)

@app.route("/cadastrar")
def insere_veiculo():
    return render_template("cadastrar.html")

@app.route("/cadastrar_bd", methods=['POST'])
def cadastra_veiculo():
    carro = {
        "marca": request.form['marca'],
        "modelo": request.form['modelo'],
        "ano": request.form['ano'],
        "preco": request.form['preco'],
        "categoria": request.form['categoria'],
        "tipo": request.form['tipo']
    }
    collection_carros.insert_one(carro)
    return redirect("/listar")

@app.route("/<id>/editar")
def editar_carro(id):
    carro = collection_carros.find_one({"_id": ObjectId(id)})
    return render_template("/atualizar.html", carro = carro)

@app.route("/atualizar_bd", methods=["POST"])
def atualiza_carro():
    id = request.form['id']
    carro = {
        "marca": request.form['marca'],
        "modelo": request.form['modelo'],
        "ano": request.form['ano'],
        "preco": request.form['preco'],
        "categoria": request.form['categoria'],
        "tipo": request.form['tipo']
    }
    collection_carros.update_one({"_id": ObjectId(id)}, {"$set": carro})

    return redirect("/listar")

@app.route("/<id>/excluir")
def excluir_veiculo(id):
    collection_carros.delete_one({"_id": ObjectId(id)})

    retorno_carros = list(collection_carros.find())
    return redirect("/listar")

if __name__ == '__main__':
    app.run(debug=True)
