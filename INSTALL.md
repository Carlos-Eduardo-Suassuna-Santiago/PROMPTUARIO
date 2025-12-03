# Guia de Instalação do Promptuario

Este guia fornece instruções detalhadas para instalar e configurar o sistema Promptuario em diferentes ambientes.

## Requisitos do Sistema

### Requisitos Mínimos

- **Sistema Operacional:** Linux, macOS ou Windows (com WSL2)
- **Python:** 3.11 ou superior
- **Memória RAM:** 2GB mínimo (4GB recomendado)
- **Espaço em Disco:** 500MB para a aplicação + dependências

### Requisitos para Docker

- **Docker:** 20.10 ou superior
- **Docker Compose:** 2.0 ou superior

## Instalação Local (Desenvolvimento)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/promptuario.git
cd promptuario
```

### Passo 2: Criar Ambiente Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e edite conforme necessário:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Passo 5: Executar Migrações

```bash
python manage.py migrate
```

### Passo 6: Criar Usuários de Teste

```bash
python manage.py create_initial_users
```

### Passo 7: Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### Passo 8: Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

## Instalação com Docker

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/promptuario.git
cd promptuario
```

### Passo 2: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Para produção com Docker, configure:

```env
SECRET_KEY=sua-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
DATABASE_URL=postgresql://promptuario:promptuario123@db:5432/promptuario
```

### Passo 3: Construir e Iniciar os Containers

```bash
docker-compose up --build
```

O sistema estará disponível em:
- **Aplicação:** [http://localhost](http://localhost)
- **Admin Django:** [http://localhost/admin](http://localhost/admin)

### Passo 4: Parar os Containers

```bash
docker-compose down
```

## Instalação em Produção

### Usando Docker (Recomendado)

1. Configure as variáveis de ambiente em `.env` com valores de produção
2. Gere uma SECRET_KEY forte:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

3. Configure `DEBUG=False`
4. Adicione seu domínio em `ALLOWED_HOSTS`
5. Configure um banco PostgreSQL
6. Execute:

```bash
docker-compose -f docker-compose.yml up -d
```

### Sem Docker

1. Instale PostgreSQL
2. Crie um banco de dados:

```sql
CREATE DATABASE promptuario;
CREATE USER promptuario WITH PASSWORD 'senha-forte';
GRANT ALL PRIVILEGES ON DATABASE promptuario TO promptuario;
```

3. Configure o `.env`:

```env
DATABASE_URL=postgresql://promptuario:senha-forte@localhost:5432/promptuario
```

4. Execute as migrações e colete os estáticos
5. Configure um servidor web (Nginx + Gunicorn)

## Verificação da Instalação

### Testar o Sistema

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar testes
pytest

# Verificar cobertura
pytest --cov
```

### Acessar o Admin

1. Acesse [http://localhost:8000/admin](http://localhost:8000/admin)
2. Use as credenciais: `admin` / `admin123`

### Verificar o Healthcheck

```bash
curl http://localhost:8000/healthcheck/
```

Deve retornar: `{"status": "ok"}`

## Solução de Problemas

### Erro: "No module named 'django'"

**Solução:** Ative o ambiente virtual e instale as dependências:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "CSRF verification failed"

**Solução:** Verifique se `ALLOWED_HOSTS` está configurado corretamente no `.env`.

### Erro de Conexão com o Banco de Dados

**Solução:** Verifique se o PostgreSQL está rodando e se as credenciais em `DATABASE_URL` estão corretas.

### Arquivos Estáticos não Carregam

**Solução:** Execute:

```bash
python manage.py collectstatic --noinput
```

## Próximos Passos

Após a instalação bem-sucedida:

1. Leia o [README.md](README.md) para entender a estrutura do projeto
2. Consulte o [CONTRIBUTING.md](CONTRIBUTING.md) se quiser contribuir
3. Explore a documentação da API (se disponível)
4. Configure backups regulares do banco de dados

## Suporte

Se encontrar problemas durante a instalação, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento.
