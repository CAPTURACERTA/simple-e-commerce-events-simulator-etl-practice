# Simple E-commerce Events Simulator - ETL Practice

Projeto simples de simulação de eventos de e-commerce, criado como prática de engenharia de dados com uma API em FastAPI, persistência em PostgreSQL e um fluxo local de geração, carga e análise de dados.

Mais do que uma API CRUD, este projeto foi construído como um exercício prático para entender como dados transacionais podem ser gerados, armazenados, consultados e transformados em informações analíticas.

## Foco principal: aprendizado em engenharia de dados

O objetivo principal deste projeto foi praticar fundamentos de engenharia de dados em um ambiente pequeno, controlado e fácil de entender.

Durante o desenvolvimento, trabalhei conceitos como:

- modelagem de tabelas relacionais para clientes, produtos, pedidos e itens de pedido;
- criação automática de estrutura no PostgreSQL;
- uso de chaves primárias, chaves estrangeiras e restrições de unicidade;
- separação entre dados transacionais e consultas analíticas;
- geração de dados simulados para alimentar o banco;
- carga de eventos no banco por meio de um fluxo ETL local;
- consultas SQL com `JOIN`, `GROUP BY`, `COUNT`, `SUM` e ordenação por métricas;
- validação de entrada com Pydantic e FastAPI;
- tratamento de erros previsíveis em rotas da API;
- organização básica de uma aplicação Python com routers, schemas, scripts e camada de banco.
- visualização do fluxo do pipeline usando postman

A ideia foi criar um projeto pequeno o suficiente para ser compreendido de ponta a ponta, mas completo o bastante para representar um fluxo realista: cadastrar entidades base, gerar pedidos simulados, persistir esses eventos e extrair métricas de negócio.

## Uso de IA no desenvolvimento

Este projeto também marcou uma introdução saudável e útil ao uso de IA no código.

Usei IA como ferramenta de apoio analítico, revisão e aceleração, sempre buscando compreender o que estava sendo sugerido antes de aceitar qualquer mudança. O objetivo não foi terceirizar o raciocínio, mas melhorar meu desempenho combinando estudo, implementação manual, revisão crítica e auxílio automatizado.

Ferramentas utilizadas:

- GitHub Copilot para sugestões inline durante a escrita de trechos de código;
- Codex para verificações, revisão da estrutura, melhorias pontuais e montagem de algumas partes do código.

O uso da IA foi feito de forma consciente:

- analisei as sugestões antes de aplicar;
- comparei as respostas com o comportamento esperado da aplicação;
- revisei os efeitos no código e no fluxo do projeto;
- pedi verificações sobre pontos frágeis, como validação de entrada, tratamento de erro e organização geral;
- mantive o entendimento do funcionamento da aplicação como prioridade.

Esse processo aumentou muito minha produtividade em relação a fazer tudo sozinho, principalmente porque a IA ajudou a identificar pontos de melhoria, sugerir ajustes e acelerar partes repetitivas. Ainda assim, cada mudança relevante foi avaliada dentro do contexto do projeto.

## Sobre o projeto

A aplicação simula uma base de e-commerce com:

- clientes;
- produtos;
- pedidos;
- itens de pedido;
- geração automática de pedidos simulados;
- endpoints analíticos para consultar clientes e produtos com melhor desempenho.

O fluxo principal é:

1. cadastrar clientes;
2. cadastrar produtos;
3. executar o endpoint de extração para gerar pedidos simulados;
4. consultar métricas nos endpoints de analytics.

## Tecnologias

- Python 3.12+
- FastAPI
- PostgreSQL
- psycopg2
- Pydantic
- python-dotenv
- uv

## Estrutura

```text
src/
  main.py
  db.py
  schemas.py
  routers/
    analytics.py
    customers.py
    extract.py
    orders.py
    products.py
  scripts/
    etl.py
    fake_data.py
```

## Modelo de dados

O projeto cria quatro tabelas principais:

- `customers`: clientes cadastrados;
- `products`: produtos cadastrados;
- `orders`: pedidos realizados;
- `order_items`: itens associados a cada pedido.

As tabelas são criadas automaticamente quando a aplicação importa o módulo de banco, desde que a conexão com o PostgreSQL esteja configurada corretamente.

## Configuração local

Crie um arquivo `.env` na raiz do projeto com as variáveis de conexão:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=postgres
DB_POOL_MIN=1
DB_POOL_MAX=10
```

Instale as dependências:

```bash
uv sync
```

Execute a API:

```bash
uvicorn src.main:app --reload
```

A documentação interativa ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Endpoints principais

### Customers

- `POST /customers/`: cria um cliente;
- `GET /customers/`: lista clientes;
- `GET /customers/{customer_id}`: busca um cliente por ID.

### Products

- `POST /products/`: cria um produto;
- `GET /products/`: lista produtos;
- `GET /products/{product_id}`: busca um produto por ID.

### Orders

- `POST /orders/`: cria um pedido manualmente;
- `GET /orders/`: lista pedidos;
- `GET /orders/{order_id}`: busca um pedido por ID.

### Extract

- `POST /extract/`: gera pedidos simulados com base nos clientes e produtos existentes.

Exemplo de corpo:

```json
{
  "amount": 10
}
```

Antes de executar esse endpoint, é necessário ter pelo menos um cliente e um produto cadastrados.

### Analytics

- `GET /analytics/top-customers-count/{limit}`: clientes com maior número de pedidos;
- `GET /analytics/top-customers-value/{limit}`: clientes com maior valor total gasto;
- `GET /analytics/top-products/{limit}`: produtos mais vendidos.

O parâmetro `limit` aceita valores de `1` a `100`.

## Exemplos de uso

Criar um cliente:

```bash
curl -X POST http://127.0.0.1:8000/customers/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Silva", "email": "ana@example.com"}'
```

Criar um produto:

```bash
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyboard", "price": 199.90}'
```

Gerar pedidos simulados:

```bash
curl -X POST http://127.0.0.1:8000/extract/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 10}'
```

Consultar produtos mais vendidos:

```bash
curl http://127.0.0.1:8000/analytics/top-products/5
```

## O que este projeto demonstra

Este projeto demonstra minha capacidade de:

- construir uma API simples com FastAPI;
- conectar uma aplicação Python a um banco PostgreSQL;
- modelar dados relacionais básicos;
- gerar dados sintéticos para simulação;
- criar um fluxo local de ingestão de dados;
- escrever consultas analíticas em SQL;
- validar entradas e tratar erros previsíveis;
- usar IA como apoio produtivo sem abrir mão da compreensão técnica.

## Status

Projeto em estágio funcional para prática e portfólio.

Ele não busca ser uma aplicação de produção, mas sim um exercício completo e compreensível de engenharia de dados em escala local.
