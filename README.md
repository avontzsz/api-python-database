# Task Manager API

Esta é uma API Flask para uma aplicação de gerenciamento de tarefas. A API permite que os usuários se registrem, façam login, criem tarefas e obtenham uma lista de suas tarefas.

## Funcionalidades

- Registro de usuário
- Login de usuário
- Criação de tarefas para usuários autenticados
- Obtenção de tarefas de um usuário autenticado

## Pré-requisitos

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- PyJWT

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/avontzsz/api-python-database.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

- Configure a variável de ambiente `SECRET_KEY` para garantir a segurança dos tokens JWT.

## Uso

1. Execute a aplicação:

```bash
python app.py
```

2. Use os endpoints fornecidos para interagir com a API.

## Endpoints

- `POST /register`: Registra um novo usuário.
- `POST /login`: Autentica um usuário e retorna um token JWT.
- `POST /task`: Cria uma nova tarefa para o usuário autenticado.
- `GET /tasks`: Retorna todas as tarefas do usuário autenticado.

## Exemplo de Requisição

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "user", "password": "password"}' http://localhost:5000/register
```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.

## Autor

Arthur Miguel - [Seu GitHub](https://github.com/avontzsz)
