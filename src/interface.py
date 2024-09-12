import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import json


if st.button("Gerar Clusteres"):
    api_url = "http://api:8000/training-model"

    response = requests.get(api_url)
    data = json.loads(response.text)
    df = pd.read_json(data)
    plt.scatter(df['quantidade_teorica'], df['porcentagem_participacao'], c=df['Cluster'], cmap='viridis')
    plt.xlabel('Quantidade Teórica')
    plt.ylabel('Porcentagem de Participação')
    plt.title('K-Means Clustering das Ações B3')

    st.pyplot(plt)
