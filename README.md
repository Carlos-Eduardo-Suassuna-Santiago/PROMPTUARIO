# 🩺 **Promptuário**
### Sistema Web para Gestão de Prontuários Médicos  

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![Django](https://img.shields.io/badge/Django-4.3-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)
![Docker](https://img.shields.io/badge/Docker-suportado-0db7ed?logo=docker)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-ativo-black?logo=githubactions)
![License](https://img.shields.io/badge/license-MIT-green)

---

# 📖 Sobre o Projeto

O **Promptuário** é um sistema web desenvolvido para otimizar o fluxo de atendimento em unidades de saúde, oferecendo:

✔ Cadastro de pacientes  
✔ Gerenciamento de consultas  
✔ Prontuário médico detalhado  
✔ Geração e anexação de relatórios e prescrições  
✔ Controle de vacinas, alergias e medicamentos  
✔ Agenda médica completa  
✔ Painel administrativo  

O sistema foi projetado seguindo boas práticas de **engenharia de software**, **segurança da informação** e **LGPD**.

---

# 🧱 Tecnologias Utilizadas

### **Backend**
- 🐍 Python 3.11  
- 🧩 Django 4.3 (MVT)  
- 🗄️ SQLite (dev) / PostgreSQL (prod)  

### **Frontend**
- 🎨 HTML5  
- 🧼 CSS3  
- 🖼️ Django Templates  

### **Infra / DevOps**
- 🐳 Docker / Docker Compose  
- 🎛 Gunicorn (produção)  
- ☁️ GitHub Actions (CI/CD)

### **Testes**
- 🧪 pytest  
- 📏 coverage  

---

# 🏗️ Arquitetura Geral

A aplicação segue a arquitetura **MVT – Model View Template** do Django.

```mermaid
graph LR
  U[Usuário] --> F[Frontend - Templates Django]
  F --> V[Views]
  V --> M[Models]
  M --> DB[(Banco de Dados)]
  V --> A[Arquivos (Relatórios/Prescrições)]
````

---

# 📂 Estrutura do Projeto

```
promptuario/
│
├── core/                  # App principal
│   ├── models.py          # Modelos
│   ├── views.py           # Lógica de negócio
│   ├── urls.py            # Rotas
│   ├── templates/core/    # Templates HTML
│   └── static/css/        # CSS / assets
│
├── promptuario/           # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── infra/
│   ├── docker/            # Dockerfiles e entrypoint
│   └── docker-compose.*   # Compose dev/prod
│
├── scripts/               # Instalação, backup, migração
├── tests/                 # Testes pytest
└── README.md
```

---

# 🚀 Como Rodar o Projeto

## ▶️ Rodando com Docker (recomendado)

### **1. Clone o repositório**

```bash
git clone https://github.com/seuusuario/promptuario.git
cd promptuario
```

### **2. Suba os containers**

```bash
docker-compose -f infra/docker-compose.dev.yml up --build
```

### **3. Acesse**

👉 [http://localhost:8000](http://localhost:8000)

---

## ▶️ Rodando sem Docker

### **1. Crie o ambiente virtual**

```bash
python -m venv .venv
source .venv/bin/activate
```

### **2. Instale as dependências**

```bash
pip install -r requirements.txt
```

### **3. Aplique as migrações**

```bash
python promptuario/manage.py migrate
```

### **4. Crie um superusuário**

```bash
python promptuario/manage.py createsuperuser
```

### **5. Execute o servidor**

```bash
python promptuario/manage.py runserver
```

---

# 🧪 Testes

## Executar testes

```bash
pytest
```

## Com relatório de cobertura

```bash
pytest --cov
```

📌 Cobertura mínima configurada: **90%**

---

# 🔐 Segurança, LGPD e Boas Práticas

O projeto segue boas práticas incluindo:

✔ Validação por papéis (RBAC: admin, médico, atendente, paciente)
✔ Proteção CSRF
✔ Validação e sanitização de dados
✔ Logs de auditoria
✔ Senhas com hashing seguro
✔ Separação entre dados sensíveis e não sensíveis
✔ Variáveis de ambiente para `SECRET_KEY` e credenciais
✔ Preparado para HTTPS em produção

---

# 📊 CI/CD

Pipeline GitHub Actions configurado para:

* Rodar testes automaticamente
* Validar cobertura
* Validar build
* Preparar imagem Docker
* Permitir deploy automatizado

Arquivo localizado em:

```
.github/workflows/ci.yml
```

---

# 📸 Screenshots (Figma)

> Substituir pelo design final quando disponível.

Protótipo:
🔗 [https://www.figma.com/design/RC0t8XgR1IyobtWTo0uBZg/Promptuario](https://www.figma.com/design/RC0t8XgR1IyobtWTo0uBZg/Promptuario)

Exemplo placeholder:

![Tela exemplo](https://via.placeholder.com/900x500.png?text=Tela+do+Sistema)

---

# 🗺️ Roadmap

### 🟢 Implementado

* Autenticação e controle de acesso
* CRUD de pacientes
* Dashboard
* Agendamento de consultas
* Relatórios e anexos
* Docker e Docker Compose
* Testes com pytest
* CI/CD

### 🟡 Em andamento

* Módulo de vacinas
* Módulo de alergias
* Módulo de medicamentos
* Agenda avançada

### 🔵 Futuro

* Notificações push
* Integração com WhatsApp/SMS
* API RESTful
* Multi–unidade de saúde

---

# 🤝 Contribuição

1. Faça um fork
2. Crie uma branch:

```bash
git checkout -b feature/minha-feature
```

3. Commit:

```bash
git commit -m "feat: adiciona nova funcionalidade"
```

4. Push:

```bash
git push origin feature/minha-feature
```

5. Abra um Pull Request 🚀

---

# 📜 Licença

Licença **MIT** – livre para uso pessoal e comercial.

---

Feito com ❤️ para ajudar na evolução tecnológica da área da saúde.

```

---