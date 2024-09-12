from fastapi import FastAPI
import requests
import datetime
import pandas as pd
import json
from .sanitize import Sanitize
from .database import engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = FastAPI()

@app.get("/extract-data")
def download_and_extract():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJQk9WIiwic2VnbWVudCI6IjIifQ=="

    response = requests.get(url, verify=False)

    if response.ok:
        response = json.loads(response.content.decode()).get("results")
        df = pd.DataFrame(response)

        df = Sanitize.clean_df(df)
        df["data_pregao"] = current_date
        df.to_sql("b3_data",engine,index=False, if_exists="replace")

        return {"message": "Dados coletados e armazenados com sucesso!"}
    else:
        return {"error": "Erro ao coletar os dados"}

@app.get("/training-model")
def trainingModel():
    df = pd.read_sql("b3_data", engine)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[['quantidade_teorica', 'porcentagem_participacao']])
    
    kmeans = KMeans(n_clusters=4, random_state=0)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    return df.to_json(orient='records')