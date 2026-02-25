#!/bin/sh
set -e

echo "=== Docker Entrypoint: aplicando tarefas de setup ==="

cd /code

# Criar .env a partir de .env.example se ausente
if [ -f .env.example ] && [ ! -f .env ]; then
  echo "Criando .env a partir de .env.example"
  cp .env.example .env || true
fi

# Garantir que o mount /data exista e o arquivo do DB esteja acessível
if [ ! -d "/data" ]; then
  echo "Criando diretório /data (local)..."
  mkdir -p /data || true
fi
# Criar arquivo de DB SQLite se não existir para evitar erros em algumas situações
if [ ! -f "/data/db.sqlite3" ]; then
  echo "Criando arquivo /data/db.sqlite3"
  touch /data/db.sqlite3 || true
fi

# Executar migrações com retry para aguardar o DB
echo "Executando migrações (aguardando DB)..."
RETRIES=30
until python manage.py migrate --noinput; do
  RETRIES=$((RETRIES-1))
  if [ "$RETRIES" -le 0 ]; then
    echo "Migrações falharam após múltiplas tentativas" >&2
    break
  fi
  echo "Migração falhou, tentando novamente em 2s..."
  sleep 2
done

# Criar usuários iniciais (ignorar erro caso o comando não exista)
echo "Criando usuários iniciais (se o comando existir)..."
python manage.py create_initial_users || echo "create_initial_users não disponível ou falhou, continuando..."

# Coletar estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || echo "collectstatic falhou, continuando..."

echo "Tarefas de setup concluídas. Executando: $@"

exec "$@"
