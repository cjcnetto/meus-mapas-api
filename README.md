# MEUS-MAPS-API

Este é o projeto que se encontra para MVP da disciplina  **Desenvolvimento Full Stack Básico** 

Foi pensada a seguinte arquitura:
models -> Meus modelos de acesso a base
repositories -> Classes que realizam a conexão com a base 
services -> métodos destinados a conter as regras de negócio 
database -> Diretório onde será criada a base de dados atualmente SQL Lite
log -> Logs da aplicação com os erros e chamadas de métodos.
no app.py possui os endpoints expostos para a API dos mapas

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
