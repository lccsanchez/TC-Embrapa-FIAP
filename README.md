# Embrapa FIAP Tech Challenge

API para extração, processamento e consulta aos dados públicos sobre vitivinicultura do [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php), com autenticação JWT, integração com banco de dados MySQL/Azure e interface web para cadastro e consulta.

---

## 🗂 Sumário

- [🔍 Visão Geral](#-visão-geral)
- [🚀 Funcionalidades](#-funcionalidades)
- [⚙️ Configuração do Ambiente](#️-configuração-do-ambiente)
- [🖥️ Como Executar Localmente](#️-como-executar-localmente)
- [🌐 Utilizando a Interface Web](#-utilizando-a-interface-web)
- [📡 Rotas Principais](#-rotas-principais)
- [✅ Testes](#-testes)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [📝 Licença](#-licença)

---

## 🔍 Visão Geral

Este projeto utiliza **FastAPI** para expor endpoints REST que permitem consultar, em tempo real, os dados de vitivinicultura da Embrapa: **produção, comercialização, processamento, importação e exportação**.

Funcionalidades principais incluem:

- Autenticação JWT
- Interface Web para cadastro/login
- Integração com banco de dados relacional
- Download e persistência de dados extraídos via scraping ou CSV

---

## 🚀 Funcionalidades

- 🔐 **Autenticação JWT**: Cadastro e login de usuários.
- 📊 **Consulta de Dados**: Produção, comercialização, processamento, importação e exportação.
- 📥 **Scraping & Download**: Coleta de dados do site da Embrapa ou via CSV (fallback, em que os dados são baixados via CSV, mas, a consulta dos dados, em caso de contingência, é via banco de dados).
- 💾 **Persistência**: Armazenamento dos dados em banco MySQL/Azure.
- 🖼️ **Interface Web**: Página estática para cadastro, login e consulta.
- 🛠️ **Administração**: Endpoints para salvar ou atualizar dados no banco.

---

## ⚙️ Configuração do Ambiente

### 1. Pré-requisitos

- Python 3.11+
- MySQL (local ou Azure)
- [Poetry](https://python-poetry.org/) ou `pip`

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar `.env`

1. Localize `env_example` na raiz do projeto.
2. Copie e renomeie para `.env`:

```bash
cp env_example .env
```

3. Edite com as variáveis reais do ambiente.

---

## 🖥️ Como Executar Localmente

### 1. Banco de Dados

- Configure as credenciais conforme o `.env`.
- Execute as migrações com Alembic:

```bash
alembic upgrade head
```

### 2. Inicie a API

```bash
uvicorn app.main:app --reload
```

### 3. Acesse a aplicação

Abra o navegador em: [http://localhost:8000](http://localhost:8000)

---

## 🌐 Utilizando a Interface Web

### 1. Acesse o sistema:

- [Interface Web](https://tc-embrapa-fiap.onrender.com)
- [Swagger (Documentação)](https://tc-embrapa-fiap.onrender.com/docs)

### 2. Crie um usuário:

Preencha os campos necessários:
- Usuário, Senha, E-mail
- Nome, Sobrenome, Telefone

Via Swagger:
- Vá até `/auth/create-user`
- Clique em "Try it out", preencha e envie

### 3. Faça login:

- Preencha usuário e senha para obter o token JWT
- No Swagger, clique em `Authorize`, insira o token e autentique

### 4. Consulte os dados:

- Acesse as rotas de sua escolha
- Preencha o ano e subopção, se necessário

---

## 📡 Rotas Principais

### 🔐 Autenticação
- `POST /auth/create-user` — Criação de usuário
- `POST /auth/token` — Login e obtenção do token

### 📊 Consultas
- `GET /producao?year=ANO`
- `GET /comercializacao?year=ANO`
- `GET /processamento?year=ANO&subopcao=SUB`
  - Subopções:
    - Viníferas: ProcessaViniferas
    - Americanas e híbridas: ProcessaAmericanas
    - Uvas de mesa: ProcessaMesa
    - Sem classificação: ProcessaSemclass
- `GET /importacao?year=ANO&subopcao=SUB`
  - Subopções:
    - Vinhos de mesa: ImpVinhos
    - Espumantes: ImpEspumantes
    - Uvas frescas: ImpFrescas
    - Uvas passas: ImpPassas
    - Suco de uva: ImpSuco
- `GET /exportacao?year=ANO&subopcao=SUB`
  - Subopções:
    - Vinhos de mesa: ExpVinho
    - Espumantes: ExpEspumantes
    - Uvas frescas: ExpUva
    - Suco de uva: ExpSuco

> **Obs:** Para todas as rotas é possível consultar os dados de 1970-2023.

### 🛠️ Administração
- Endpoints utilizados para salvar os dados no nosso banco de dados
- `POST /save_producao`
- `POST /save_comercializacao`
- `POST /save_processamento`
- `POST /save_importacao`
- `POST /save_exportacao`

> **Obs:** Todas as rotas (exceto `/`) exigem autenticação via **Bearer Token**.

---

## ✅ Testes

Para testar a conexão com o banco de dados:
- Acesse a raiz do projeto e execute:
```bash
pytest
```
- Ou:
```bash
pytest tests/test_auth_service.py
```

---

## 📁 Estrutura do Projeto

```
app/
│
├── main.py         # Ponto de entrada FastAPI
├── config.py       # Configurações globais e do .env
├── database.py     # Conexão com o banco de dados
├── model.py        # Modelos ORM
│
├── routes/         # Endpoints REST
├── service/        # Regras de negócio
├── repository/     # CRUD e acesso ao banco
├── util/           # Funções auxiliares
├── dto/            # Schemas de entrada/saída
├── static/         # HTML, CSS, JS da interface web
│
alembic/            # Migrações Alembic
certs/              # Certificados (banco de dados DigiCertGlobalRootCA.crt.pem.)
tests/              # Testes automatizados
.env                # Configurações sensíveis (não versionar)
env_example         # Exemplo de arquivo .env
requirements.txt    # Dependências do projeto
README.md           # Esta documentação
```

---

## 📝 Licença

Este projeto está licenciado sob a licença **MIT**.