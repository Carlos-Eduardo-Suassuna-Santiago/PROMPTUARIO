# Promptuario - Sistema de Prontuário Eletrônico

![Versão](https://img.shields.io/badge/version-1.0.0-blue)
![Licença](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-4.2-green?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker&logoColor=white)

O **Promptuario** é um sistema web de prontuário eletrônico projetado para otimizar a gestão de informações de pacientes em unidades de saúde. Ele centraliza o histórico médico, agendamentos, receitas e outros dados clínicos, facilitando o acesso seguro para médicos, atendentes e pacientes.

## 🧾 Informações Gerais

- **Área de Aplicação:** Saúde
- **Público-alvo:** Unidades de saúde públicas, médicos, atendentes e pacientes.
- **Tipo de Sistema:** Aplicação Web

## 🏗️ Diagrama de Arquitetura

O diagrama abaixo ilustra a arquitetura geral do sistema, desde a interação do usuário até a infraestrutura de backend.

![Diagrama de Arquitetura](https://private-us-east-1.manuscdn.com/sessionFile/9tqfYNNKSCtXPbgAUKakP7/sandbox/LHDQAcEVowrnMDgfogTMQJ-images_1763328004938_na1fn_L2hvbWUvdWJ1bnR1L3Byb21wdHVhcmlvL2FyY2hpdGVjdHVyZQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvOXRxZllOTktTQ3RYUGJnQVVLYWtQNy9zYW5kYm94L0xIRFFBY0VWb3dybk1EZ2ZvZ1RNUUotaW1hZ2VzXzE3NjMzMjgwMDQ5MzhfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQnliMjF3ZEhWaGNtbHZMMkZ5WTJocGRHVmpkSFZ5WlEucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Me7C3Bygz6c-t9bWgFRxaIk3OK~BlI41imSN3v9hwVMDoYia-um7DuTUBBr2teeH6SMw7nyqKfxHzGyCMcxoKjALZ73ngKAe4sXXj5bBFsVrrOujHXN6brYzz44Tx2LDegHKcwKLSkcydeTkSQITfLVh7L6QETpV~ted-z3mdZ8BI4RCR-3fOXQwv20jspgrRn0dbgZwclku4kog4R4edimy7~Cw5258ARyeoI5M-ffTumO~c2Xi~o-foi9zu8g3N5DH87Jg6WCsCDUMx1-~QH-E2zCyaqTdS-0zc9FYWHhJtJYolbfa0j-VN9vVR2ZdCo76I9pckR5X0dqmwoAMzg__)

## ✨ Funcionalidades Principais

O sistema é dividido nos seguintes módulos:

- **Gestão de Contas e Perfis:**
  - Autenticação segura com diferentes níveis de acesso (Admin, Médico, Atendente, Paciente).
  - Perfis detalhados para cada tipo de usuário.

- **Gestão de Pacientes:**
  - Cadastro completo de pacientes com informações pessoais e médicas.
  - Registro de alergias, vacinas e medicamentos de uso contínuo.

- **Agendamento de Consultas:**
  - Marcação de consultas e retornos.
  - Calendário de disponibilidade dos médicos.
  - Cancelamento de consultas com regras de negócio (24h de antecedência).

- **Prontuário Eletrônico:**
  - Histórico completo de todas as consultas e procedimentos.
  - Geração de receitas médicas em PDF.
  - Solicitação e registro de resultados de exames.

- **Administração do Sistema:**
  - Gerenciamento de usuários (médicos e atendentes).
  - Configuração de quadros de horários e plantões.

- **Relatórios:**
  - Geração de relatórios sobre consultas, pacientes e atividades médicas.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, Django 4.2
- **Frontend:** Django Templates, CSS3, JavaScript
- **Banco de Dados:** SQLite (desenvolvimento), PostgreSQL (produção)
- **Testes:** Pytest, Pytest-Django, Coverage
- **Qualidade de Código:** Black, Flake8, iSort
- **Infraestrutura:** Docker, Docker Compose, Nginx
- **CI/CD:** GitHub Actions

## 🚀 Começando

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (para execução com containers)

### 1. Instalação (sem Docker)

Clone o repositório e execute o script de setup, que irá configurar o ambiente virtual, instalar as dependências e preparar o banco de dados.

```bash
git clone https://github.com/seu-usuario/promptuario.git
cd promptuario

# Dê permissão de execução ao script
chmod +x setup.sh

# Execute o script de setup
./setup.sh
```

Após a conclusão, inicie o servidor de desenvolvimento:

```bash
source venv/bin/activate
python manage.py runserver
```

### 2. Instalação (com Docker)

Para uma configuração mais rápida e isolada, utilize o Docker Compose. Este método irá construir as imagens, iniciar os contêineres e executar as migrações automaticamente.

```bash
docker-compose up --build
```

A aplicação estará disponível em [http://localhost:8000](http://localhost:8000) (via `runserver`) ou [http://localhost](http://localhost) (via Docker).

## 🧪 Executando Testes

Para executar a suíte de testes e verificar a cobertura de código, utilize o Pytest:

```bash
source venv/bin/activate
pytest
```

## 👤 Usuários de Teste

O sistema é populado com os seguintes usuários para facilitar a demonstração:

| Usuário   | Senha        | Perfil        |
|-----------|--------------|---------------|
| `admin`     | `admin123`   | Administrador |
| `medico`    | `medico123`  | Médico        |
| `atendente` | `atendente123` | Atendente     |
| `paciente`  | `paciente123`| Paciente      |

## 🌐 Endpoints

- **/healthcheck**: Endpoint para verificação de status do sistema. Retorna `{"status": "ok"}` se a aplicação estiver no ar.

## 📂 Estrutura do Projeto

```
promptuario/
├── accounts/         # App de usuários, perfis e autenticação
├── appointments/     # App de agendamentos
├── medical_records/  # App de prontuários, receitas e exames
├── patients/         # App de pacientes, alergias e vacinas
├── reports/          # App de relatórios
├── config/           # Configurações centrais do Django
├── static/           # Arquivos estáticos (CSS, JS)
├── templates/        # Templates HTML
├── .github/          # Workflows de CI/CD
├── Dockerfile        # Configuração do container da aplicação
├── docker-compose.yml# Orquestração dos serviços
├── README.md         # Esta documentação
└── requirements.txt  # Dependências Python
```

## 🔄 CI/CD

O projeto utiliza GitHub Actions para integração e entrega contínua. O workflow (`.github/workflows/ci.yml`) automatiza:

1.  **Testes:** Executa a suíte de testes com Pytest em cada push ou pull request.
2.  **Linting:** Verifica a qualidade e o estilo do código com Black, Flake8 e iSort.
3.  **Build:** Gera a imagem Docker da aplicação quando há um push para a branch `main`.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1.  Faça um fork do projeto.
2.  Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3.  Faça suas alterações e commit (`git commit -m 'Adiciona nova funcionalidade'`).
4.  Envie para a sua branch (`git push origin feature/nova-funcionalidade`).
5.  Abra um Pull Request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
