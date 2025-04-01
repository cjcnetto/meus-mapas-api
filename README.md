# MEUS-MAPS-API

Este é o projeto que se encontra o MVP da disciplina  **Desenvolvimento Full Stack Básico** 

Tem como objetivo criar mapas e seus pontos de interesse georeferenciados.

Foi pensada a seguinte arquitetura:
- **[models](./models/)** -> Meus modelos com a configuração das entidadades de mapeamento para a base
- **[repositories](./repositories/)** -> Classes que realizam as operações com a base de dados.
- **[services](./services/)** -> Classes que controlam as regras de negócio da aplicação e interagem com os repositories
- **[exceptions](./exceptions/)** -> Erros pré definidos na aplicação para tratamento interno
- **[schemas](./schemas/)** -> schemas que serão entregues pelo endpoint.
- **[database](./database/)** -> Diretório onde será criada a base de dados do backend atualmente SQL Lite. 
- **[log](./log/)** -> Diretório onde serão criados os arquivos de log da aplicação. Com a chamada de métodos e os erros 
- **[app.py](app.py)** -> Arquivo com todos os endpoints exposto pela aplicação e a configuração do Swager.

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