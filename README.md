# DESAFIO DEV. BR MED - Backend

Sistema para o teste DESAFIO DEV. BR MED - Backend 


Segue a história de usuário:

Preciso de um sistema que guarde as cotações do dólar versus real, euro e iene(JPY) e que as exibe em um gráfico, respeitando as seguintes especificações:

* Deve ser possível informar uma data de início e de fim para consultar qualquer período de tempo, contanto que o período informado seja de no máximo 5 dias úteis.
* Deve ser possível variar as moedas (real, euro e iene).


Existem algumas restrições que devem ser seguidas:
* Os dados das cotações devem ser coletados utilizando a api do https://www.vatcomply.com/documentation (Você vai precisar usar Dólar como base).
* O código deve ser desenvolvido utilizando um repositório git no seu perfil do Github ou BitBucket;
* Backend: deve ser implementado em python utilizando o framework django.
* Frontend: o único requisito é usar o highcharts para apresentação dos dados.
* Não precisa de login, usuário, autenticação ou qualquer coisa. Só a página carregando o gráfico.


O que será avaliado?
* Clareza do código escrito.
* Uso de Orientação a Objetos.
* Entendimento de práticas de desenvolvimento como testes automatizados, utilização correta do controle de versão.
* Conhecimento do framework escolhido.


Bônus:
* Deploy no heroku ou em outro servidor de sua preferência.
* Criar uma api para realizar leitura das cotações persistidas no banco de dados.


### Deploy 

A aplicação esta no endpoint https://currency-rate-render-app2.onrender.com

Mais informações podem ser vistas em https://currency-rate-render-app2.onrender.com/openapi/
Mais informações podem ser vistas em https://currency-rate-render-app2.onrender.com/swagger/  



### Instalação e Execução

**Requisitos:** Docker e docker-compose

1. Copie o conteúdo de contrib/env-sample para um arquivo .env na raiz do projeto.

```bash
cp contrib/env-sample .env
```

2. Construa a imagem

```bash
docker-compose build
```

3. Instalar o pre-commit

```bash
pre-commit install
```

4. Instalar pre-push para rodar os testes automaticamente

```bash
pre-commit install --hook-type pre-push
```

5. Execute o sistema

```bash
docker-compose run --rm --service-ports api
```

6. Compilar dependências

```bash
docker-compose run --rm api bash -c "pip-compile --generate-hashes /opt/currency_rate/requirements/production.in && pip-compile --generate-hashes /opt/currency_rate/requirements/development.in"
```

7. Executar testes

```bash
docker-compose run --rm --service-ports api pytest --cov .
```

8. Executar o flake8 (linter)

```bash
docker-compose run --rm --service-ports api flake8 .
```

8. Executar o blue (formatador)

```bash
docker-compose run --rm --service-ports api blue .
```
