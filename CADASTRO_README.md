# Funcionalidade de Cadastro de Usuários - Promptuario

Esta documentação descreve a funcionalidade completa de cadastro de usuários implementada no sistema Promptuario.

## 📋 Visão Geral

O sistema possui um sistema robusto de cadastro de usuários com diferentes níveis de acesso e validações específicas para cada tipo de usuário.

## 🎯 Tipos de Cadastro

### 1. Cadastro de Paciente (Público)

O cadastro de paciente é **público** e pode ser acessado por qualquer pessoa através da página de login.

**URL:** `/accounts/register/` ou `/accounts/register/patient/`

**Campos obrigatórios:**
- Nome de usuário (username)
- Email
- Senha e confirmação de senha
- Nome completo (primeiro nome e sobrenome)
- CPF

**Campos opcionais:**
- Telefone
- Data de nascimento
- Endereço completo (rua, cidade, estado, CEP)
- Tipo sanguíneo
- Altura e peso
- Contato de emergência (nome e telefone)
- Observações médicas

**Validações:**
- CPF único no sistema
- Email único no sistema
- Senhas devem corresponder
- Formato de CPF, telefone e CEP são validados automaticamente

### 2. Cadastro de Médico (Apenas Admin)

O cadastro de médicos é **restrito** e só pode ser realizado por administradores do sistema.

**URL:** `/accounts/register/doctor/`

**Campos obrigatórios:**
- Todos os campos do cadastro básico
- **CRM** (único no sistema)
- **Especialidade**

**Campos opcionais:**
- Biografia profissional
- Valor da consulta

**Validações:**
- CRM único no sistema
- Apenas usuários admin podem acessar

### 3. Cadastro de Atendente (Apenas Admin)

O cadastro de atendentes é **restrito** e só pode ser realizado por administradores do sistema.

**URL:** `/accounts/register/attendant/`

**Campos obrigatórios:**
- Todos os campos do cadastro básico

**Campos opcionais:**
- Departamento
- Turno (Manhã, Tarde, Noite, Integral)

**Validações:**
- Apenas usuários admin podem acessar

## 🔐 Segurança

### Validações Implementadas

O sistema implementa as seguintes validações de segurança:

**Unicidade de Dados:**
- CPF não pode ser duplicado
- Email não pode ser duplicado
- CRM (para médicos) não pode ser duplicado

**Validação de Senhas:**
- Senha deve ter no mínimo 8 caracteres
- Senha não pode ser muito comum
- Senha não pode ser totalmente numérica
- As duas senhas devem corresponder

**Formatação Automática:**
- CPF: `000.000.000-00`
- Telefone: `(00) 00000-0000`
- CEP: `00000-000`

## 🎨 Interface

### Página de Cadastro de Paciente

A página de cadastro de paciente possui um design moderno e responsivo com:

- Formulário dividido em seções lógicas:
  - Dados de Acesso
  - Dados Pessoais
  - Endereço
  - Informações Médicas

- Validação em tempo real com mensagens de erro claras
- Formatação automática de campos (CPF, telefone, CEP)
- Link para login caso o usuário já possua conta

### Páginas de Cadastro Admin

As páginas de cadastro de médico e atendente seguem o layout padrão do sistema com:

- Integração com o menu de navegação
- Botões de ação (Cadastrar e Cancelar)
- Validações e mensagens de erro
- Redirecionamento para lista de usuários após sucesso

### Página de Escolha de Tipo

Administradores têm acesso a uma página de escolha de tipo de cadastro:

**URL:** `/accounts/register/choice/`

Esta página apresenta cards visuais para escolher entre:
- Cadastrar Médico
- Cadastrar Atendente
- Cadastrar Paciente

## 🔗 Fluxo de Cadastro

### Fluxo do Paciente

1. Usuário acessa a página de login
2. Clica em "Cadastre-se"
3. Preenche o formulário de cadastro
4. Sistema valida os dados
5. Conta é criada automaticamente
6. Usuário é redirecionado para o login
7. Mensagem de sucesso é exibida

### Fluxo do Admin (Médico/Atendente)

1. Admin faz login no sistema
2. Acessa "Usuários" no menu
3. Clica em "Novo Usuário" ou acessa diretamente a URL de registro
4. Escolhe o tipo de usuário
5. Preenche o formulário específico
6. Sistema valida os dados
7. Conta é criada
8. Admin é redirecionado para lista de usuários
9. Mensagem de sucesso é exibida

## 📝 Exemplos de Uso

### Cadastro via Interface Web

**Paciente:**
```
1. Acesse: http://localhost:8000/accounts/login/
2. Clique em "Cadastre-se"
3. Preencha os dados
4. Clique em "Cadastrar"
```

**Médico (como Admin):**
```
1. Faça login como admin
2. Acesse: http://localhost:8000/accounts/register/doctor/
3. Preencha os dados incluindo CRM e especialidade
4. Clique em "Cadastrar Médico"
```

### Cadastro Programático

```python
from accounts.forms import PatientRegistrationForm

# Criar paciente
form = PatientRegistrationForm(data={
    'username': 'novopaciente',
    'email': 'paciente@exemplo.com',
    'password1': 'senhaforte123',
    'password2': 'senhaforte123',
    'first_name': 'João',
    'last_name': 'Silva',
    'cpf': '123.456.789-00',
    'blood_type': 'O+',
})

if form.is_valid():
    user = form.save()
    print(f"Paciente {user.get_full_name()} criado com sucesso!")
```

## 🧪 Testes

O sistema inclui uma suíte completa de testes para a funcionalidade de cadastro:

```bash
# Executar todos os testes de registro
pytest accounts/test_registration.py -v

# Executar testes específicos
pytest accounts/test_registration.py::TestPatientRegistration -v
pytest accounts/test_registration.py::TestDoctorRegistration -v
pytest accounts/test_registration.py::TestAttendantRegistration -v
```

**Testes implementados:**
- ✅ Acesso à página de registro
- ✅ Cadastro bem-sucedido
- ✅ Validação de CPF duplicado
- ✅ Validação de email duplicado
- ✅ Validação de CRM duplicado (médicos)
- ✅ Validação de senhas diferentes
- ✅ Restrição de acesso (apenas admin para médicos/atendentes)

## 📂 Arquivos Relacionados

```
accounts/
├── forms.py                          # Formulários de cadastro
├── views.py                          # Views de registro
├── urls.py                           # URLs de registro
├── test_registration.py              # Testes de registro
└── templates/accounts/
    ├── register_patient.html         # Template de cadastro de paciente
    ├── register_doctor.html          # Template de cadastro de médico
    ├── register_attendant.html       # Template de cadastro de atendente
    └── register_choice.html          # Template de escolha de tipo
```

## 🚀 Próximas Melhorias

Possíveis melhorias futuras para a funcionalidade de cadastro:

- [ ] Verificação de email com link de ativação
- [ ] Integração com reCAPTCHA para evitar bots
- [ ] Upload de foto de perfil durante o cadastro
- [ ] Validação de CPF com algoritmo verificador
- [ ] Busca automática de endereço por CEP (API ViaCEP)
- [ ] Cadastro em múltiplas etapas (wizard)
- [ ] Recuperação de senha
- [ ] Login social (Google, Facebook)

## 💡 Dicas de Uso

**Para Desenvolvedores:**
- Os formulários herdam de `UserRegistrationForm` para reutilização de código
- Cada tipo de usuário tem um método `save()` customizado que cria o perfil correspondente
- As validações são feitas tanto no frontend (JavaScript) quanto no backend (Django)

**Para Administradores:**
- Use a página de escolha de tipo para facilitar o cadastro
- Sempre verifique os dados antes de cadastrar médicos (CRM válido)
- Pacientes podem se auto-cadastrar, mas médicos e atendentes devem ser cadastrados por admins

**Para Usuários:**
- Guarde bem suas credenciais de acesso
- Preencha todos os campos obrigatórios marcados com *
- Campos opcionais podem ser preenchidos posteriormente no perfil