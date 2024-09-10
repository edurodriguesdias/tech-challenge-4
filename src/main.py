from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import requests
import datetime
import pandas as pd
import json
from .sanitize import Sanitize
from .database import SessionLocal, engine
from . import models


# Inicializa a aplicação FastAPI
app = FastAPI()

# Inicializa o banco de dados
models.Base.metadata.create_all(bind=engine)


# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint para coletar os dados
@app.post("/collect/")
def download_and_extract(db: Session = Depends(get_db)):
    # Obtém a data atual
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # URL de origem dos dados
    url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJQk9WIiwic2VnbWVudCI6IjIifQ=="

    # Faz a requisição HTTP
    response = requests.get(url, verify=False)

    if response.ok:
        # Processa a resposta
        response = json.loads(response.content.decode()).get("results")
        df = pd.DataFrame(response)

        # Limpeza e sanitização dos dados usando o sanitize.py
        df = Sanitize.clean_df(df)
        df["data_pregao"] = current_date

        # Armazena os dados no banco de dados
        for index, row in df.iterrows():
            db_data = models.B3Data(
                setor=row['setor'],
                codigo=row['codigo'],
                acao=row['acao'],
                tipo=row['tipo'],
                quantidade_teorica=row['quantidade_teorica'],
                porcentagem_participacao=row['porcentagem_participacao'],
                porcentagem_participacao_acumulada=row['porcentagem_participacao_acumulada'],
                data_pregao=row['data_pregao']
            )
            db.add(db_data)
        db.commit()

        return {"message": "Dados coletados e armazenados com sucesso!"}
    else:
        return {"error": "Erro ao coletar os dados"}
