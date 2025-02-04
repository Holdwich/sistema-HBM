# Simulador HBM+

O Simulador HBM+ é um projeto de demonstração de um sistema de monitoramento de medições de um dispositivo médico.

O projeto consiste em uma aplicação web dividida em dois componentes principais:

1. **Frontend**: Uma interface de usuário para simular medições e exibir o histórico de medições e irregularidades detectadas. O frontend é escrito em Next.js.
2. **Backend**: Uma API que fornece os dados de medição e irregularidades detectadas. A API é escrita em FastAPI e utiliza o banco de dados especificado na variável de ambiente `DATABASE_URL` (pode ser trocado por via da variável desta, deve ser compatível com SQLAlchemy).

## Instalação

Para instalar o projeto, é necessário que tenha o Docker instalado, após isso, navegue até a pasta onde se encontra o docker-compose, e execute os seguintes comandos no cmd:

```
    docker compose build
    docker compose up
```

Após alguns instantes, a aplicação estará rodando.

Caso prefira executar cada aplicação separadamente, navegue para as pastas das respectivas aplicações, e execute os comandos apropriados para cada aplicação em um cmd diferente:

Para o front:
```
    npm install && npm run start
```
Para o back:
```
    pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000
```

## Atenção

Se a execução for local, lembre-se de configurar o arquivo `.env` com a variável de ambiente `DATABASE_URL` com a connection string para o SQLAlchemy, com o banco de dados desejado.

Exemplo:
    DATABASE_URL=mysql+mysqlconnector://user:password@mysql/dbhbm

## Utilização

Para utilizar o simulador, abra o browser e navegue para `http://localhost:3000`. Lá você encontrará uma interface para simular medições e exibir o histórico de medições e irregularidades detectadas.

Caso prefira interagir diretamente com a API, que já está documentada com Swagger, vá para `http://localhost:8000/docs`


## Finalização da aplicação

Para finalizar a aplicação, execute o comando:

```
    docker compose down
```

ou aperte `CTRL-C` nos CMDs abertos, caso a execução seja feita manualmente sem o Docker.