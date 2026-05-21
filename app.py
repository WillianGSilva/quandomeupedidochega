from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "quality_entregas_secret"

CUPONS_VALIDOS = ["QUALITY2026", "PRAZOQUALITY", "QENTREGAS"]

# Base de clientes/remetentes
# Tipo:
# - Quality = Cliente que a Quality já opera
# - Prospectar = Possível cliente/remetente
clientes_lista = [
    {"tipo": "Quality", "cliente": "4 BIO MEDICAMENTOS S.A", "cidade": "São Paulo", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "VALDEQUIMICA PRODUTOS QUIMICOS LTDA", "cidade": "São Paulo", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "Farmacia Buenos Ayres Ltda", "cidade": "São Paulo", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "GALENA QUIMICA E FARMACEUTICA LTDA", "cidade": "Campinas", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "ASTRA FARMA COMERCIO DE MATERIAL MEDICO HOSPITALAR LTDA", "cidade": "Pouso Alegre", "uf": "MG", "segmento": "Hospitalar"},
    {"tipo": "Quality", "cliente": "IBEROQUIMICA FARMACEUTICA LTDA", "cidade": "Jundiaí", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "SODROGAS DIST. DE MED. E MAT. MED. HOSP. LTDA", "cidade": "Aparecida de Goiânia", "uf": "GO", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "Ativa Comercial Hospitalar Ltda", "cidade": "Catalão", "uf": "MG", "segmento": "Hospitalar"},
    {"tipo": "Quality", "cliente": "BELIVE COMERCIO DE PRODUTOS HOSPITALARES LTDA", "cidade": "Campinas", "uf": "SP", "segmento": "Hospitalar"},
    {"tipo": "Quality", "cliente": "CRISTALIA PRODUTOS QUIMICOS FARMACEUTICOS", "cidade": "Itapira", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "Medihosp Distribuidora de Materiais Médicos Hospitalar", "cidade": "São Paulo", "uf": "SP", "segmento": "Hospitalar"},
    {"tipo": "Quality", "cliente": "Singular Drogaria e Medicamentos Especiais Ltda", "cidade": "São Paulo", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "CIMED INDUSTRIA DE MEDICAMENTOS LTDA", "cidade": "Pouso Alegre", "uf": "MG", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "Dental Med Sul", "cidade": "São José dos Pinhais", "uf": "PR", "segmento": "Odontológico"},
    {"tipo": "Quality", "cliente": "CIAMED - Distribuidora de Medicamentos Ltda", "cidade": "Encantado", "uf": "RS", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "QUANTIQ DISTRIBUIDORA LTDA (Active Caldic)", "cidade": "Palhoça", "uf": "SC", "segmento": "Químico"},
    {"tipo": "Quality", "cliente": "PN Farmaceutica LTDA", "cidade": "Palhoça", "uf": "SC", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "FITISSIMO", "cidade": "Belo Horizonte", "uf": "MG", "segmento": "Alimenticio"},
    {"tipo": "Quality", "cliente": "SURYA", "cidade": "Maringá", "uf": "PR", "segmento": "Odontológico"},
    {"tipo": "Quality", "cliente": "UNIÃO QUÍMICA FARMACÊUTICA NACIONAL S.A.", "cidade": "Pouso Alegre", "uf": "MG", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "EMS S.A.", "cidade": "Hortolândia", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "ACHÉ LABORATÓRIOS FARMACÊUTICOS S.A.", "cidade": "Guarulhos", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "HYPERA PHARMA", "cidade": "Anápolis", "uf": "GO", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "BLAU FARMACÊUTICA S.A.", "cidade": "Cotia", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Quality", "cliente": "BIOLAB SANUS FARMACÊUTICA", "cidade": "Taboão da Serra", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "LIBBS FARMACÊUTICA LTDA", "cidade": "Embu das Artes", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "TORRENT PHARMACEUTICALS", "cidade": "Barueri", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "SERVIMED COMERCIAL LTDA", "cidade": "Bauru", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "DROGACENTER DISTRIBUIDORA", "cidade": "Ribeirão Preto", "uf": "SP", "segmento": "Farmacêutico"},
    {"tipo": "Prospectar", "cliente": "CIRÚRGICA FERNANDES", "cidade": "Santana de Parnaíba", "uf": "SP", "segmento": "Hospitalar"},
    {"tipo": "Prospectar", "cliente": "BECTON DICKINSON BRASIL", "cidade": "Curitiba", "uf": "PR", "segmento": "Hospitalar"},
    {"tipo": "Prospectar", "cliente": "BAXTER HOSPITALAR LTDA", "cidade": "São Paulo", "uf": "SP", "segmento": "Hospitalar"},
    {"tipo": "Prospectar", "cliente": "MEDTRONIC COMERCIAL LTDA", "cidade": "São Paulo", "uf": "SP", "segmento": "Hospitalar"},
    {"tipo": "Prospectar", "cliente": "NEODENT", "cidade": "Curitiba", "uf": "PR", "segmento": "Odontológico"},
    {"tipo": "Prospectar", "cliente": "DENTSPLY SIRONA BRASIL", "cidade": "Petrópolis", "uf": "RJ", "segmento": "Odontológico"},
    {"tipo": "Prospectar", "cliente": "STRAUMANN BRASIL", "cidade": "Curitiba", "uf": "PR", "segmento": "Odontológico"},
    {"tipo": "Prospectar", "cliente": "GROWTH SUPPLEMENTS", "cidade": "São José do Rio Preto", "uf": "SP", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "INTEGRALMÉDICA", "cidade": "Embu das Artes", "uf": "SP", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "MAX TITANIUM", "cidade": "Matão", "uf": "SP", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "VITAFOR", "cidade": "Araçatuba", "uf": "SP", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "ESSENTIAL NUTRITION", "cidade": "São José", "uf": "SC", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "NUTRIFY", "cidade": "São Paulo", "uf": "SP", "segmento": "Suplementos"},
    {"tipo": "Prospectar", "cliente": "OUROFINO SAÚDE ANIMAL", "cidade": "Cravinhos", "uf": "SP", "segmento": "Veterinário"},
    {"tipo": "Prospectar", "cliente": "VETNIL", "cidade": "Louveira", "uf": "SP", "segmento": "Veterinário"},
    {"tipo": "Prospectar", "cliente": "CEVA SAÚDE ANIMAL", "cidade": "Paulínia", "uf": "SP", "segmento": "Veterinário"},
    {"tipo": "Prospectar", "cliente": "ZOETIS INDÚSTRIA DE PRODUTOS VETERINÁRIOS", "cidade": "Campinas", "uf": "SP", "segmento": "Veterinário"},
    {"tipo": "Prospectar", "cliente": "MSD SAÚDE ANIMAL", "cidade": "Cruzeiro", "uf": "SP", "segmento": "Veterinário"},
    {"tipo": "Prospectar", "cliente": "NATURA COSMÉTICOS", "cidade": "Cajamar", "uf": "SP", "segmento": "Cosméticos"},
    {"tipo": "Prospectar", "cliente": "GRUPO BOTICÁRIO", "cidade": "São José dos Pinhais", "uf": "PR", "segmento": "Cosméticos"},
    {"tipo": "Prospectar", "cliente": "MANTECORP SKINCARE", "cidade": "São Paulo", "uf": "SP", "segmento": "Cosméticos"},
    {"tipo": "Prospectar", "cliente": "ADCOS COSMÉTICA", "cidade": "Serra", "uf": "ES", "segmento": "Cosméticos"},
    {"tipo": "Prospectar", "cliente": "ISDIN BRASIL", "cidade": "São Paulo", "uf": "SP", "segmento": "Cosméticos"},
]

clientes = {
    item["cliente"]: {
        "segmento": item["segmento"],
        "tipo": item["tipo"],
        "cidade": item["cidade"],
        "uf": item["uf"],
        "performance": "96,8%" if item["tipo"] == "Quality" else "95,2%"
    }
    for item in clientes_lista
}

segmentos = sorted({item["segmento"] for item in clientes_lista})
cidades = sorted({item["cidade"] for item in clientes_lista} | {
    "São Paulo", "Campinas", "Curitiba", "São José dos Pinhais", "Goiânia",
    "Hortolândia", "Pouso Alegre", "Belo Horizonte", "Rio de Janeiro",
    "Florianópolis", "Porto Alegre", "Jundiaí", "Aparecida de Goiânia",
    "Catalão", "Itapira", "Encantado", "Palhoça", "Maringá", "Guarulhos",
    "Anápolis", "Cotia", "Taboão da Serra", "Embu das Artes", "Barueri",
    "Bauru", "Ribeirão Preto", "Santana de Parnaíba", "Petrópolis",
    "São José do Rio Preto", "Matão", "Araçatuba", "São José", "Cravinhos",
    "Louveira", "Paulínia", "Cruzeiro", "Cajamar", "Serra"
})

ufs = ["SP", "PR", "GO", "MG", "RJ", "SC", "RS", "ES"]

# Mapa para preencher UF automaticamente pela cidade
cidades_uf = {}
for item in clientes_lista:
    cidades_uf[item["cidade"]] = item["uf"]

cidades_uf.update({
    "São Paulo": "SP",
    "Campinas": "SP",
    "Curitiba": "PR",
    "São José dos Pinhais": "PR",
    "Goiânia": "GO",
    "Hortolândia": "SP",
    "Pouso Alegre": "MG",
    "Belo Horizonte": "MG",
    "Rio de Janeiro": "RJ",
    "Florianópolis": "SC",
    "Porto Alegre": "RS",
})

# Prazo por UF origem x UF destino
prazos = {
    ("SP", "SP"): 1, ("SP", "PR"): 1, ("SP", "GO"): 2, ("SP", "MG"): 2,
    ("SP", "RJ"): 2, ("SP", "SC"): 2, ("SP", "RS"): 3, ("SP", "ES"): 3,

    ("PR", "SP"): 1, ("PR", "PR"): 1, ("PR", "SC"): 1, ("PR", "GO"): 3,
    ("PR", "MG"): 3, ("PR", "RJ"): 3, ("PR", "RS"): 2, ("PR", "ES"): 4,

    ("GO", "SP"): 2, ("GO", "GO"): 1, ("GO", "MG"): 2, ("GO", "PR"): 3,
    ("GO", "RJ"): 3, ("GO", "SC"): 4, ("GO", "RS"): 4, ("GO", "ES"): 4,

    ("MG", "SP"): 2, ("MG", "MG"): 1, ("MG", "PR"): 3, ("MG", "GO"): 2,
    ("MG", "RJ"): 2, ("MG", "SC"): 3, ("MG", "RS"): 4, ("MG", "ES"): 2,

    ("SC", "SP"): 2, ("SC", "PR"): 1, ("SC", "SC"): 1, ("SC", "RS"): 1,
    ("SC", "MG"): 3, ("SC", "RJ"): 3, ("SC", "GO"): 4, ("SC", "ES"): 4,

    ("RS", "SP"): 3, ("RS", "PR"): 2, ("RS", "SC"): 1, ("RS", "RS"): 1,
    ("RS", "MG"): 4, ("RS", "RJ"): 4, ("RS", "GO"): 4, ("RS", "ES"): 5,

    ("RJ", "SP"): 2, ("RJ", "MG"): 2, ("RJ", "RJ"): 1, ("RJ", "ES"): 2,
    ("RJ", "PR"): 3, ("RJ", "SC"): 3, ("RJ", "RS"): 4, ("RJ", "GO"): 3,

    ("ES", "SP"): 3, ("ES", "MG"): 2, ("ES", "RJ"): 2, ("ES", "ES"): 1,
    ("ES", "PR"): 4, ("ES", "SC"): 4, ("ES", "RS"): 5, ("ES", "GO"): 4,
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
        cliente = request.form.get("cliente", "").strip()
        origem = request.form.get("origem", "").strip()
        cidade_origem = request.form.get("cidade_origem", "").strip()
        cidade_destino = request.form.get("cidade_destino", "").strip()
        uf_destino = request.form.get("uf_destino", "").strip()

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
        cidades=cidades,
        ufs=ufs,
        cidades_uf=cidades_uf,
        resultado=resultado
    )


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("cupom"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
