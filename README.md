## Tech Challenge #4
Repositório criado para atender aos requisitos do Tech Challenge da fase atual do curso de Machine Learning Engineering da FIAP. 

## Integrantes
- Eduardo Dias
- Felipe Langoni

## Tecnologias utilizadas
- Python
- FastAPI
- Docker

## Proposta do Desafio
A solução apresentada tem como objetivo desenvolver um modelo preditivo utilizando dados históricos da bolsa de valores (B3). O modelo é treinado com a finalidade de prever os valores diários das ações de empresas listadas, oferecendo insights estratégicos para análise financeira.

Para implementar essa solução, utilizamos o TensorFlow como framework principal para construção e treinamento do modelo de machine learning, garantindo alta performance e flexibilidade. As métricas de desempenho do modelo são monitoradas e gerenciadas com o MLflow, permitindo rastreamento, reprodutibilidade e otimização contínua. Além disso, o FastAPI é empregado para criar um endpoint de previsão rápido e eficiente, possibilitando que as previsões sejam acessadas de forma integrada e escalável.

## Soluções Implementadas

### API Predict
`POST` [http://api.group88.hypercodetech.com.br/predict](http://api.group88.hypercodetech.com.br/predict)

```
{
    "ticker": "ITUB4.SA",
    "look_back": "10",
    "dias_para_prever": "2"
}
```

### Ações Disponíveis Para Prever
- ABEV3.SA
- ITUB4.SA
- PETR4.SA
- VALE3.SA

### Dashboard Visualização MLFlow
[http://mlflow.group88.hypercodetech.com.br:5000/](http://mlflow.group88.hypercodetech.com.br:5000/)


### Diagrama Criação Modelo + Deploy API
![diagrama drawio](https://github.com/user-attachments/assets/1f3bdf4e-411f-4da6-8c0c-48d3a0802029)

## Iniciando a aplicação
**Subir containers docker**
```
docker-compose up -d
```

**Instalar dependências do projeto**
```
docker-compose exec web pip install -r ./requirements/requirements.txt
```

**Limpar cache**
```
rm -rf __pycache__
```

## Recursos da API
- POST /predict: Retorna a predição baseada nos parâmetros informados
