import json
from datetime import datetime

def inicializarBancoDeDados():
    try:
        banco = open("log.dat","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat","w")

def salvar_log(nome, pontos):
    try:
        with open("log.dat", "r") as f:
            conteudo = f.read().strip()
            if conteudo:
                logs = json.loads(conteudo)
            else:
                logs = []
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")

    logs.append({"nome": nome, "data": data, "hora": hora, "pontos": pontos})

    with open("log.dat", "w") as f:
        json.dump(logs, f)