from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "quality_entregas_secret"

CUPONS_VALIDOS = ["QUALITY2026", "PRAZOQUALITY", "QENTREGAS"]

segmentos = [
    "Produtos Farmacêuticos",
    "Suplementos",
    "Hospitalar",
    "Cosméticos"
]

clientes = {
    "Dental Medsul": {
        "segmento": "Produtos Farmacêuticos",
        "tipo": "Cliente Quality",
        "cidade": "São José dos Pinhais",
        "uf": "PR",
        "performance": "96,1%"
    },
    "Galena": {
        "segmento": "Produtos Farmacêuticos",
        "tipo": "Cliente Quality",
        "cidade": "Campinas",
        "uf": "SP",
        "performance": "97,4%"
    },
    "Medilar": {
        "segmento": "Produtos Farmacêuticos",
        "tipo": "Cliente Quality",
        "cidade": "São Paulo",
        "uf": "SP",
        "performance": "96,8%"
    },
    "Supermedica": {
        "segmento": "Hospitalar",
        "tipo": "Cliente Quality",
        "cidade": "Goiânia",
        "uf": "GO",
        "performance": "94,9%"
    },
    "EMS": {
        "segmento": "Produtos Farmacêuticos",
        "tipo": "Possível Cliente",
        "cidade": "Hortolândia",
        "uf": "SP",
        "performance": "95,2%"
    },
    "Cimed": {
        "segmento": "Produtos Farmacêuticos",
        "tipo": "Possível Cliente",
        "cidade": "Pouso Alegre",
        "uf": "MG",
        "performance": "95,2%"
    },
    "Nutrify": {
        "segmento": "Suplementos",
        "tipo": "Possível Cliente",
        "cidade": "São Paulo",
        "uf": "SP",
        "performance": "95,2%"
    }
}

prazos = {
    ("SP", "SP"): 1,
    ("SP", "PR"): 1,
    ("SP", "GO"): 2,
    ("SP", "MG"): 2,
    ("SP", "RJ"): 2,
    ("SP", "SC"): 2,
    ("SP", "RS"): 3,

    ("PR", "SP"): 1,
    ("PR", "PR"): 1,
    ("PR", "SC"): 1,
    ("PR", "GO"): 3,
    ("PR", "MG"): 3,
    ("PR", "RJ"): 3,

    ("GO", "SP"): 2,
    ("GO", "GO"): 1,
    ("GO", "MG"): 2,
    ("GO", "PR"): 3,

    ("MG", "SP"): 2,
    ("MG", "MG"): 1,
    ("MG", "PR"): 3,
    ("MG", "GO"): 2,
}


@app.route("/", methods=["GET", "POST"])
def cupom():
    erro = None

    if request.method == "POST":
        cupom_digitado = request.form.get("cupom", "").strip().upper()

        if cupom_digitado in CUPONS_VALIDOS:
            session["autorizado"] = True
            return redirect(url_for("consulta"))
        else:
            erro = "Cupom inválido ou expirado."

    return render_template("cupom.html", erro=erro)


@app.route("/consulta", methods=["GET", "POST"])
def consulta():
    if not session.get("autorizado"):
        return redirect(url_for("cupom"))

    resultado = None

    if request.method == "POST":
        cliente = request.form.get("cliente")
        origem = request.form.get("origem")
        cidade_origem = request.form.get("cidade_origem")

        cidade_destino = request.form.get("cidade_destino")
        uf_destino = request.form.get("uf_destino")

        performance_regiao = "95,2%"
        tipo_cliente = "Consulta manual"

        if cliente in clientes:
            origem = clientes[cliente]["uf"]
            cidade_origem = clientes[cliente]["cidade"]
            performance_regiao = clientes[cliente]["performance"]
            tipo_cliente = clientes[cliente]["tipo"]

        prazo = prazos.get((origem, uf_destino), 3)

        resultado = {
            "cliente": cliente or "Não informado",
            "origem": origem,
            "cidade_origem": cidade_origem,
            "cidade_destino": cidade_destino,
            "uf_destino": uf_destino,
            "prazo": prazo,
            "performance_geral": "96,8%",
            "performance_regiao": performance_regiao,
            "tipo_cliente": tipo_cliente
        }

    return render_template(
        "index.html",
        clientes=clientes,
        segmentos=segmentos,
        resultado=resultado
    )


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("cupom"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
