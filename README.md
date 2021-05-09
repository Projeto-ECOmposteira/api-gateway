<div>
    <p align="center">
    <img src='https://raw.githubusercontent.com/Projeto-ECOmposteira/documentacao/main/assets/img/logo/logo.png' alt="Projeto Kokama" width="25%"/>
    </p> 
    <h1 align="center">
    Projeto ECOmposteira
    </h1>
</div>

## API Gateway

A API Gateway é responsável por delegar as demandas vindas do front-end (interface) para os demais microsserviços disponíveis na aplicação.

## Rode o Backend com Docker

### Dependências

Inicialmente, instale localmente as seguintes dependências:

1. Instale o [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/);
2. Instale o [Docker Compose](https://docs.docker.com/compose/install/).

### Arquivo de Configuração

1. Crie um arquivo `.env` e preencha as variáveis de ambiente de acordo com os exemplos localizados nos arquivos `env-reference`.

### Inicialização do Projeto

1. Na pasta principal do projeto, construa e inicialize a aplicação com o comando:

```bash
sudo make
```

2. A API Gateway estará disponível em: `http://localhost:8000/`.
