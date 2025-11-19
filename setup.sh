#!/bin/bash

# Script de setup do projeto Promptuario

echo "=== Setup do Promptuario ==="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
if ! command -v python3.11 &> /dev/null; then
    echo -e "${YELLOW}Python 3.11 não encontrado. Por favor, instale Python 3.11${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3.11 encontrado${NC}"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3.11 -m venv venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}Ambiente virtual já existe${NC}"
fi

# Ativar ambiente virtual

source venv/bin/activate #Linux/Mac
venv\Scripts\activate #Windows

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip atualizado${NC}"

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "Criando arquivo .env..."
    cp .env.example .env
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
else
    echo -e "${YELLOW}.env já existe${NC}"
fi

# Executar migrações
echo "Executando migrações..."
python manage.py migrate > /dev/null 2>&1
echo -e "${GREEN}✓ Migrações executadas${NC}"

# Criar usuários iniciais
echo "Criando usuários de teste..."
python manage.py create_initial_users
echo -e "${GREEN}✓ Usuários criados${NC}"

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✓ Arquivos estáticos coletados${NC}"

echo ""
echo -e "${GREEN}=== Setup concluído com sucesso! ===${NC}"
echo ""
echo "Para iniciar o servidor de desenvolvimento, execute:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Ou com Docker:"
echo "  docker-compose up"
echo ""
echo "Acesse: http://localhost:8000"
echo ""
echo "Usuários de teste:"
echo "  Admin:     admin / admin123"
echo "  Médico:    medico / medico123"
echo "  Atendente: atendente / atendente123"
echo "  Paciente:  paciente / paciente123"
