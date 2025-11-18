# Visão Geral Técnica do Promptuario

Este documento fornece uma visão técnica detalhada do sistema Promptuario, incluindo arquitetura, decisões de design e padrões utilizados.

## Arquitetura do Sistema

O Promptuario segue o padrão **MVT (Model-View-Template)** do Django, com uma arquitetura modular baseada em apps.

### Componentes Principais

O sistema é composto pelos seguintes módulos principais:

**Accounts** - Gerencia autenticação, autorização e perfis de usuários. Implementa um modelo de usuário customizado que suporta quatro tipos distintos: Administrador, Médico, Atendente e Paciente. Cada tipo possui perfis estendidos com informações específicas.

**Patients** - Responsável pelo cadastro e gerenciamento de informações dos pacientes, incluindo dados pessoais, histórico de alergias, vacinas e medicamentos em uso contínuo.

**Appointments** - Controla o agendamento de consultas, incluindo validação de disponibilidade, regras de cancelamento e notificações automáticas.

**Medical Records** - Armazena prontuários médicos completos, receitas, solicitações de exames e histórico de alterações para auditoria.

**Reports** - Gera relatórios customizáveis sobre consultas, pacientes e atividades médicas em diversos formatos.

## Modelo de Dados

### Relacionamentos Principais

O modelo de dados foi projetado para garantir integridade referencial e facilitar consultas complexas. Os principais relacionamentos incluem:

- **User → DoctorProfile/AttendantProfile/Patient** (1:1) - Cada usuário possui um perfil específico baseado em seu tipo.
- **Patient → Appointment** (1:N) - Um paciente pode ter múltiplas consultas.
- **DoctorProfile → Appointment** (1:N) - Um médico atende múltiplos pacientes.
- **Appointment → MedicalRecord** (1:1) - Cada consulta gera um prontuário único.
- **MedicalRecord → Prescription/Exam** (1:N) - Um prontuário pode conter várias receitas e exames.

### Auditoria e Histórico

O sistema mantém um registro completo de todas as alterações realizadas nos prontuários médicos através do modelo `MedicalRecordHistory`, garantindo rastreabilidade e conformidade com a LGPD.

## Segurança

### Autenticação e Autorização

O sistema utiliza o sistema de autenticação nativo do Django, com as seguintes camadas de segurança:

- **Autenticação baseada em sessão** - Cookies seguros com proteção CSRF.
- **Controle de acesso baseado em perfis** - Mixins customizados (`AdminRequiredMixin`) garantem que apenas usuários autorizados acessem funcionalidades específicas.
- **Senhas criptografadas** - Utiliza o algoritmo PBKDF2 com salt aleatório.

### Proteção de Dados

Todas as informações sensíveis são protegidas seguindo as diretrizes da LGPD:

- Dados médicos são acessíveis apenas por médicos e pelo próprio paciente.
- Atendentes têm acesso limitado a informações não-sensíveis.
- Histórico de acesso e modificações é registrado para auditoria.

## Performance

### Otimizações de Banco de Dados

O sistema utiliza diversas técnicas para otimizar o desempenho:

- **Select Related e Prefetch Related** - Reduz o número de queries em relacionamentos.
- **Índices** - Campos frequentemente consultados (CPF, CRM) possuem índices únicos.
- **Paginação** - Listas longas são paginadas (20 itens por página).

### Cache e Arquivos Estáticos

- **WhiteNoise** - Serve arquivos estáticos comprimidos diretamente pelo Django.
- **Compressão** - CSS e JavaScript são minificados em produção.

## Testes

O projeto adota uma abordagem de testes em múltiplas camadas:

### Testes Unitários

Testam a lógica de negócio dos modelos e funções isoladamente. Exemplos incluem:

- Criação e validação de usuários
- Cálculo de idade de pacientes
- Regras de cancelamento de consultas

### Testes de Integração

Verificam a interação entre diferentes componentes do sistema, como a criação de um prontuário após uma consulta.

### Cobertura de Código

O projeto visa manter uma cobertura de testes acima de **95%**, garantindo que a maior parte do código seja testada.

## Infraestrutura

### Docker e Containerização

O sistema é totalmente containerizado, facilitando o deploy e a escalabilidade. A arquitetura Docker inclui:

- **Web Container** - Executa a aplicação Django com Gunicorn.
- **Database Container** - PostgreSQL 15 para persistência de dados.
- **Nginx Container** - Serve como proxy reverso e servidor de arquivos estáticos.

### CI/CD

O pipeline de CI/CD automatiza:

1. **Testes** - Execução automática de testes em cada push.
2. **Linting** - Verificação de qualidade de código.
3. **Build** - Construção da imagem Docker.
4. **Deploy** - (Configurável) Deploy automático em produção.

## Padrões de Código

### Estilo

O projeto segue rigorosamente o **PEP 8**, com formatação automática via **Black** e validação via **Flake8**.

### Organização

- **Apps modulares** - Cada funcionalidade é isolada em um app Django.
- **Separação de responsabilidades** - Models, Views e Templates são claramente separados.
- **Reutilização** - Mixins e classes base promovem DRY (Don't Repeat Yourself).

### Documentação

Todo código é documentado com docstrings descritivas, facilitando a manutenção e onboarding de novos desenvolvedores.

## Escalabilidade

O sistema foi projetado para escalar horizontalmente:

- **Stateless** - A aplicação não mantém estado local, permitindo múltiplas instâncias.
- **Banco de Dados Separado** - PostgreSQL pode ser escalado independentemente.
- **Arquivos Estáticos** - Podem ser servidos por CDN em produção.

## Próximas Melhorias

Possíveis evoluções futuras do sistema incluem:

- **API REST** - Exposição de endpoints para integração com outros sistemas.
- **Notificações em Tempo Real** - WebSockets para alertas instantâneos.
- **Integração com HL7/FHIR** - Padrões de interoperabilidade em saúde.
- **Machine Learning** - Análise preditiva de dados médicos.

## Conclusão

O Promptuario é um sistema robusto, seguro e escalável, projetado seguindo as melhores práticas de desenvolvimento de software. Sua arquitetura modular facilita a manutenção e evolução contínua.
