# MEUS-MAPS-API

Este é o projeto que se encontra o MVP da disciplina  **Desenvolvimento Qualidade de Software, Segurança e Sistemas Inteligentes** 
esse projeto é uma continuação do projeto do Fullstack Básico.

## Objetivo 
- Inicialmente o é criar mapas e seus pontos de interesse georeferenciados. 
- Foi adicionado que dado um tiroteio um momento em que aconteça um tiroteio com ação policial no ponto de interesse a possibilidade de haver vítimas feridas, mortes ou não haver vítimas.

## Arquitetura

Foi pensada a seguinte arquitetura:
- **[database](./database/)** -> Diretório onde será criada a base de dados do backend atualmente SQL Lite. 
- **[exceptions](./exceptions/)** -> Erros pré definidos na aplicação para tratamento interno
- **[log](./log/)** -> Diretório onde serão criados os arquivos de log da aplicação. Com a chamada de métodos e os erros 
- **[MachineLearning](./MachineLearning/)** -> Diretório onde se encontram os dados de MachineLearning criados com o dataset completo dos tiroteios pro treinamento, codigo de recuperação de novas informações e notebooks para avaliação e explicação do processo de construção do modelo
- **[models](./models/)** -> Meus modelos com a configuração das entidadades de mapeamento para a base
- **[repositories](./repositories/)** -> Classes que realizam as operações com a base de dados.
- **[schemas](./schemas/)** -> schemas que serão entregues pelo endpoint.
- **[services](./services/)** -> Classes que controlam as regras de negócio da aplicação e interagem com os repositories
- **[test](./test/)** -> Classes de test da aplicação 
- **[util](./util/)** -> Classes utilitárias 
- **[app.py](app.py)** -> Arquivo com todos os endpoints exposto pela aplicação e a configuração do Swager.

---
## Como executar 

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
- Para criar o ambiente execute 
```
python -m venv meus_mapas_env
```
- Para ativar seu ambiente
```
.\meus_mapas_env\Scripts\activate
```
- Para instalar todas as bibliotecas necessárias descritas no `requirements.txt`
```
(env)$ pip install -r requirements.txt
```
- Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```
- Para executar os testes basta 
```
pytest -v
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

O front end dessa aplicação se encontra no [https://github.com/cjcnetto/meus-mapas-web](https://github.com/cjcnetto/meus-mapas-web)