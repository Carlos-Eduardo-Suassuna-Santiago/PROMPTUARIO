# Análise de Requisitos - Sistema Promptuario

## 1. Visão Geral do Projeto

**Nome:** Promptuario  
**Descrição:** Sistema de prontuário eletrônico para unidades de saúde pública  
**Tecnologia:** Django (Python) + SQLite  
**Arquitetura:** MVT (Model-View-Template)  
**Área:** Saúde Pública

## 2. Atores do Sistema

### 2.1 Administrador
- Cadastrar e gerenciar médicos e atendentes
- Configurar quadros de horários
- Gerenciar usuários do sistema

### 2.2 Médico
- Visualizar histórico completo de pacientes
- Gerar relatórios de consultas
- Disponibilizar receitas virtuais (PDF)
- Marcar retornos
- Cadastrar avisos de ausência
- Acessar dados sensíveis (diagnóstico, sintomas, medicamentos)

### 2.3 Atendente
- Cadastrar pacientes
- Gerenciar consultas (agendar, cancelar)
- Marcar retornos
- Visualizar dados básicos de pacientes

### 2.4 Paciente
- Solicitar consultas
- Visualizar histórico médico próprio
- Consultar receitas e vacinas
- Cancelar consultas (com 24h de antecedência)

## 3. Requisitos Funcionais Principais

### RF001 - Gestão de Usuários
- Cadastro de médicos (nome, CPF, CRM, data nascimento, endereço, salário)
- Cadastro de atendentes (nome, CPF, data nascimento, endereço)
- Cadastro de pacientes (nome, CPF, endereço, data nascimento, telefone, email opcional, informações médicas)

### RF002 - Quadro de Horários
- Configuração personalizada de dias e horários por médico
- Suporte a plantões
- Detecção de conflitos de agendamento

### RF003 - Agendamento de Consultas
- Solicitação por paciente ou atendente
- Escolha de médico, dia e horário
- Marcação de retornos
- Cancelamento com 24h de antecedência

### RF004 - Prontuário Eletrônico
- Histórico de consultas
- Diagnósticos e sintomas
- Medicamentos receitados
- Receitas virtuais (PDF)
- Histórico de vacinas
- Alergias e restrições

### RF005 - Relatórios Médicos
- Geração de relatórios por consulta
- Filtros por médico, período, tipo de consulta
- Registro de diagnóstico, medicamentos, sintomas e observações

### RF006 - Notificações
- Lembretes de vacinação
- Avisos de ausência de médicos
- Alertas de cancelamento de consultas

### RF007 - Autenticação e Autorização
- Login com usuário e senha
- Controle de acesso por perfil (Admin, Médico, Atendente, Paciente)
- Autenticação segura

## 4. Requisitos Não Funcionais

### RNF001 - Segurança e Privacidade
- Conformidade com LGPD
- Criptografia de dados sensíveis
- Controle de acesso baseado em perfis
- Histórico de alterações (auditoria)

### RNF002 - Disponibilidade
- Sistema disponível 24/7
- Backup automático a cada 7 dias

### RNF003 - Escalabilidade
- Suporte a aumento gradual de usuários
- Performance mantida com crescimento de dados

### RNF004 - Usabilidade
- Interface responsiva
- Design moderno e intuitivo
- Notificações assíncronas (AJAX)

### RNF005 - Regras de Negócio
- Cancelamento de consultas: mínimo 24h antes
- Médicos podem editar consultas até fechamento
- Apenas médicos e pacientes veem dados de consultas
- Atendentes não acessam dados sensíveis

## 5. Módulos do Sistema

### 5.1 Módulo de Autenticação
- Login/Logout
- Recuperação de senha
- Controle de sessão

### 5.2 Módulo de Administração
- CRUD de médicos e atendentes
- Configuração de quadros de horários
- Gestão de usuários

### 5.3 Módulo de Pacientes
- CRUD de pacientes
- Visualização de histórico
- Gestão de informações médicas

### 5.4 Módulo de Consultas
- Agendamento
- Cancelamento
- Marcação de retornos
- Visualização de agenda

### 5.5 Módulo de Prontuário
- Histórico de consultas
- Receitas virtuais
- Vacinas
- Alergias
- Medicamentos

### 5.6 Módulo de Relatórios
- Relatórios de consultas
- Relatórios por médico
- Relatórios por período
- Exportação de dados

### 5.7 Módulo de Notificações
- Lembretes de vacinas
- Avisos de ausência
- Confirmações de agendamento

## 6. Estrutura de Páginas

1. **Login** - Autenticação de usuários
2. **Dashboard** - Visão geral por perfil
3. **Cadastro** - Formulários de registro
4. **Perfil** - Dados do usuário logado
5. **Administração** - Gestão de usuários e horários
6. **Pacientes** - Listagem e detalhes
7. **Agenda** - Calendário de consultas
8. **Prontuário** - Histórico médico completo
9. **Relatórios** - Geração de relatórios
10. **Exames** - Registro de exames
11. **Vacinas** - Cartão de vacinação
12. **Medicamentos** - Prescrições e receitas
13. **Alergias** - Registro de alergias

## 7. Tecnologias e Ferramentas

### Backend
- Python 3.11
- Django 4.x
- SQLite
- Django REST Framework (se necessário API)

### Frontend
- Django Templates
- CSS puro (design moderno)
- JavaScript vanilla
- AJAX para notificações assíncronas

### DevOps
- Docker e Docker Compose
- GitHub Actions (CI/CD)
- Vercel (deploy)

### Testes
- pytest
- pytest-django
- coverage (95% mínimo)

### Qualidade de Código
- black (formatação)
- flake8 (linting)
- prettier (CSS/JS)

## 8. Observações Importantes

- O Figma requer login, então o design será baseado nas especificações dos documentos
- Design moderno com foco em usabilidade
- Responsividade total (mobile-first)
- Acessibilidade (WCAG 2.1)
- Documentação completa em português
- Estrutura modular e escalável
- Código limpo e bem documentado
