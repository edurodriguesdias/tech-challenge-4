## Tech Challenge #3
Repositório criado para atender aos requisitos do Tech Challenge da fase atual do curso de Machine Learning Engineering da FIAP. Este projeto engloba a construção de uma API para coleta de dados, armazenamento em banco de dados e aplicação de um modelo de Machine Learning.

## Tecnologias utilizadas
- Python
- FastAPI
- Swagger
- Docker
- Postgresql

## O Problema
O objetivo deste projeto é construir uma API que colete dados, armazene essas informações em um banco de dados relacional e treine um modelo de Machine Learning utilizando essa base de dados. O modelo treinado deve ser utilizado para alimentar uma aplicação ou dashboard, apresentando visualmente os resultados do processo.

## Requisitos do Desafio:
- Coleta de dados: A API deve ser capaz de coletar dados e armazená-los em um banco de dados convencional, como o PostgreSQL.
- Treinamento de modelo de ML: O modelo de Machine Learning será treinado com os dados coletados pela API.
- Documentação e Repositório: Todo o código, bem como a documentação do modelo, será disponibilizado neste repositório do GitHub.
- Storytelling: Deve haver uma apresentação visual, por meio de um vídeo explicativo, contando todas as etapas do desenvolvimento do projeto.
- Aplicação produtiva: O modelo final deverá ser capaz de alimentar uma aplicação simples ou um dashboard.

## Requisitos do Projeto
- Docker: Será utilizado para containerizar a aplicação.
- Docker Compose: Para facilitar o gerenciamento dos containers.

## Deploy
Não há pipeline de deploy automatizada configurada para este projeto.

## Comandos
Use os seguintes comandos para executar as ações desejadas:

**Iniciar a aplicação localmente**

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

## Banco de Dados
Este projeto utiliza PostgreSQL como banco de dados. Certifique-se de que o container correspondente esteja rodando corretamente para o correto funcionamento da API.

## Documentação
A API está documentada usando Swagger. Com a aplicação rodando localmente, você pode acessar a documentação no seguinte endereço:

http://localhost:8000/docs
****

## Funcionalidades da API
GET /dados: Coleta os dados da fonte e os armazena no banco de dados.
POST /treinar-modelo: Inicia o processo de treinamento do modelo de Machine Learning com os dados armazenados.

## Agenda Evolutiva do Projeto:
- [x] Configuração do ambiente com Docker e PostgreSQL.
- [x] Endpoint GET /dados para coleta e armazenamento de dados.
- [x] Implementação do modelo de ML.
- [x] Testes de integração.
- [x] Storytelling e vídeo explicativo do projeto.
- [ ] Deploy da aplicação para ambiente produtivo (AWS, etc).
