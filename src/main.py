from fastapi import FastAPI
import requests
import datetime
import pandas as pd
import json
from .sanitize import Sanitize
from .database import engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

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
    df_scaled = __get_scaled_data(df)
    
    kmeans = KMeans(n_clusters=2, random_state=0)
    kmeans.fit(df_scaled)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    return df.to_json(orient='records')

@app.get("/optimal-centroid-number")
def best_value_for_k_elbow_method():
    WSS = []
    K = range(1, 10)

    df = pd.read_sql("b3_data", engine)
    scaled_data = __get_scaled_data(df)
    
    for k in K:
        kmeansInstance = KMeans(n_clusters=k)
        kmeansInstance.fit(scaled_data)
        WSS.append(kmeansInstance.inertia_)

    plt.figure(figsize=(10,5))
    plt.plot(K, WSS, '-bo')
    plt.xlabel('k')
    plt.ylabel('WSS')
    plt.title('Elbow Method - Optimal Centroid Number')
    
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    file_path = os.path.join(images_dir, 'elbow_method.png')

    plt.savefig(file_path, format='png')

    return {"message": f"Gráfico salvo em: {file_path}"}
 
def __get_scaled_data(df):
    scaler = StandardScaler()
    return scaler.fit_transform(df[['quantidade_teorica', 'porcentagem_participacao']])