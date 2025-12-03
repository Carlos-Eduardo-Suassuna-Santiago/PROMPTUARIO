#!/bin/bash

echo "=== Setup do Promptuario ==="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detectar Python (3.10+)
PYTHON=$(command -v python3 || command -v python || command -v py)

if [ -z "$PYTHON" ]; then
    echo -e "${YELLOW}Python não encontrado. Instale Python 3.10+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python encontrado: $PYTHON${NC}"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    $PYTHON -m venv venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}Ambiente virtual já existe${NC}"
fi

# Ativar venv conforme SO
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Git Bash / Windows
    echo "Ativando venv (Windows)..."
    source venv/Scripts/activate
else
    # Linux/Mac
    echo "Ativando venv (Linux/Mac)..."
    source venv/bin/activate
fi

echo -e "${GREEN}✓ Ambiente virtual ativado${NC}"

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip atualizado${NC}"

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# Criar .env
if [ ! -f ".env" ]; then
    echo "Criando arquivo .env..."
    cp .env.example .env
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
else
    echo -e "${YELLOW}.env já existe${NC}"
fi

# Migrações
echo "Executando migrações..."
python manage.py migrate > /dev/null 2>&1
echo -e "${GREEN}✓ Migrações executadas${NC}"

# Usuários iniciais
echo "Criando usuários..."
python manage.py create_initial_users
echo -e "${GREEN}✓ Usuários criados${NC}"

# Static
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✓ Arquivos estáticos coletados${NC}"

echo ""
echo -e "${GREEN}=== Setup concluído com sucesso! ===${NC}"
