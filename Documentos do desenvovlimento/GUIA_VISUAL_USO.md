# 🎬 GUIA VISUAL: Como Usar o Cadastro Inline

## Cenário Real: Atendente Agendando Consulta para Novo Paciente

---

## 📍 PASSO 1: Acesse a Página de Agendamento

**URL**: `http://seu-sistema.com/agendamentos/criar/`

```
┌──────────────────────────────────────────────────────────────┐
│  Sistema de Agendamento Medical                          🏠   │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Agendar Consulta para Paciente                              │
│  Preencha os dados para agendar a consulta.                  │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Paciente: [▼ Selecione um paciente    ] [✚ Novo]    │    │
│  │                                           ↑ NOVO      │    │
│  │                                       CLIQUE AQUI    │    │
│  │                                                      │    │
│  │ Médico: [▼ Selecione um médico       ]             │    │
│  │                                                      │    │
│  │ Data: [2026-01-25                   ]              │    │
│  │                                                      │    │
│  │ Horário: [10:30                     ]              │    │
│  │                                                      │    │
│  │ Motivo: [Consulta de rotina        ]               │    │
│  │                                                      │    │
│  │  [Agendar Consulta]  [Cancelar]                     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔔 PASSO 2: Clique em "✚ Novo"

Quando você clica no botão verde "✚ Novo", um modal se abre:

```
┌──────────────────────────────────────────────────────────────┐
│  Sistema de Agendamento Medical                          🏠   │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Agendar Consulta para Paciente                              │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Paciente: [▼ Selecione um paciente] [✚ Novo]       │    │
│  │                                                      │    │
│  │  ╔═══════════════════════════════════════════════╗  │    │
│  │  ║  📋 Registrar Novo Paciente                  ║  │    │
│  │  ╠═══════════════════════════════════════════════╣  │    │
│  │  ║                                               ║  │    │
│  │  ║ Nome:          [João          ]               ║  │    │
│  │  ║ Sobrenome:     [Silva         ]               ║  │    │
│  │  ║                                               ║  │    │
│  │  ║ CPF:           [123.456.789-10]               ║  │    │
│  │  ║ Email:         [joao@gmail.com]               ║  │    │
│  │  ║                                               ║  │    │
│  │  ║ Telefone:      [(11) 98765-4321]             ║  │    │
│  │  ║ Tipo de Sangue:[O+ ▼          ]              ║  │    │
│  │  ║                                               ║  │    │
│  │  ║ Contato Emergência:                          ║  │    │
│  │  ║  Nome: [Maria Silva       ]                   ║  │    │
│  │  ║  Tel:  [(11) 99999-8888   ]                  ║  │    │
│  │  ║                                               ║  │    │
│  │  ║ ℹ️ Nota: O paciente poderá completar seu     ║  │    │
│  │  ║ cadastro (altura, peso, etc) na primeira vez  ║  │    │
│  │  ║ que acessar a plataforma.                      ║  │    │
│  │  ║                                               ║  │    │
│  │  ║            [Cancelar]  [✓ Registrar Paciente]║  │    │
│  │  ╚═══════════════════════════════════════════════╝  │    │
│  │                                                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## ✏️ PASSO 3: Preencha os Dados

### Campos Obrigatórios (com *)
- **Nome**: `João`
- **Sobrenome**: `Silva`
- **CPF**: `123.456.789-10` (com máscara automática)
- **Email**: `joao@gmail.com`

### Campos Opcionais
- **Telefone**: `(11) 98765-4321` (máscara automática)
- **Tipo de Sangue**: `O+`
- **Contato de Emergência**: `Maria Silva` e telefone

```
✨ MÁSCARAS AUTOMÁTICAS:
───────────────────────────
• CPF: Digita "12345678910" → Mostra "123.456.789-10"
• Telefone: Digita "11987654321" → Mostra "(11) 98765-4321"
```

---

## ✅ PASSO 4: Clique em "Registrar Paciente"

Após clicar, o sistema:

### 1️⃣ Valida os dados no cliente:
```
✓ Nome preenchido?
✓ Sobrenome preenchido?
✓ CPF em formato correto?
✓ Email em formato correto?
```

### 2️⃣ Se tudo OK, envia para o servidor:
```
POST /pacientes/api/quick-register/
Content-Type: application/json

{
  "first_name": "João",
  "last_name": "Silva",
  "cpf": "123.456.789-10",
  "email": "joao@gmail.com",
  "phone": "(11) 98765-4321",
  "blood_type": "O+",
  "emergency_contact_name": "Maria Silva",
  "emergency_contact_phone": "(11) 99999-8888"
}
```

### 3️⃣ Servidor valida novamente:
```
✓ Usuário está logado?
✓ Usuário é atendente ou admin?
✓ CPF não existe na base?
✓ Email não existe na base?
```

### 4️⃣ Se passou, cria o paciente:
```
✓ Cria usuário (User)
✓ Cria perfil de paciente (Patient)
✓ Retorna dados do paciente criado
```

---

## ⚡ PASSO 5: Resultado - Paciente Aparece Automaticamente

```
┌──────────────────────────────────────────────────────────────┐
│  Sistema de Agendamento Medical                          🏠   │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Agendar Consulta para Paciente                              │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Paciente: [▼ João Silva (123.456.789-10) ✓] [+ Nov] │    │
│  │                    ↑ JÁ SELECIONADO AUTOMATICAMENTE   │    │
│  │                                                      │    │
│  │ ✅ Paciente Registrado com Sucesso!                 │    │
│  │                                                      │    │
│  │ Médico: [▼ Selecione um médico       ]             │    │
│  │                                                      │    │
│  │ Data: [2026-01-25                   ]              │    │
│  │                                                      │    │
│  │ Horário: [10:30                     ]              │    │
│  │                                                      │    │
│  │ Motivo: [Consulta de rotina        ]               │    │
│  │                                                      │    │
│  │  [Agendar Consulta]  [Cancelar]                     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
│  Modal se fecha automaticamente! 🎉                           │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ PASSO 6: Continue Agendando Normalmente

Agora é só completar os dados da consulta:

```
┌──────────────────────────────────────────────────────────────┐
│  Sistema de Agendamento Medical                          🏠   │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Agendar Consulta para Paciente                              │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Paciente: [▼ João Silva (123.456.789-10)]  [+ Novo] │    │
│  │           ✅ JÁ PREENCHIDO                           │    │
│  │                                                      │    │
│  │ Médico: [▼ Dr. Carlos Silva        ]               │    │
│  │           ← PREENCHE AQUI                           │    │
│  │                                                      │    │
│  │ Data: [2026-02-15                 ]               │    │
│  │        ← PREENCHE AQUI                             │    │
│  │                                                      │    │
│  │ Horário: [14:00                   ]               │    │
│  │          ← PREENCHE AQUI                           │    │
│  │                                                      │    │
│  │ Motivo: [Consulta de rotina anual]                 │    │
│  │         ← PREENCHE AQUI                            │    │
│  │                                                      │    │
│  │  [✅ Agendar Consulta]  [Cancelar]                  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 COMPARAÇÃO DE TEMPO

### ❌ Forma Antiga (Redirecionamento)

```
Etapa                              Tempo
─────────────────────────────────────────
1. Abre formulário agendamento     5s
2. Vai para página de registro     3s
3. Preenche formulário             30s
4. Submete e aguarda              5s
5. Volta para agendamento          3s
6. Reabre formulário               3s
7. Busca novo paciente            5s
8. Continua agendamento            20s
─────────────────────────────────────────
TOTAL:                             ~74 segundos
```

### ✅ Forma Nova (Modal Inline)

```
Etapa                              Tempo
─────────────────────────────────────────
1. Abre formulário agendamento     5s
2. Clica "Novo +" (abre modal)     1s
3. Preenche formulário rápido     15s
4. Clica registrar e aguarda       3s
5. Continua agendamento            20s
─────────────────────────────────────────
TOTAL:                             ~44 segundos
```

**ECONOMIA: 30 segundos por novo paciente! ⏱️✨**

---

## ⚠️ Cenários de Erro

### Cenário 1: CPF Duplicado

```
┌──────────────────────────────────────────┐
│  Registrar Novo Paciente                 │
├──────────────────────────────────────────┤
│                                          │
│ ❌ Erro!                                 │
│ Este CPF já está cadastrado no sistema.  │
│                                          │
│ Nome: [João            ]                 │
│ Sobrenome: [Silva      ]                 │
│ CPF: [123.456.789-10   ]  ← PROBLEMA    │
│ Email: [joao@gmail.com ]                 │
│                                          │
│ [Cancelar]  [Registrar Paciente]         │
│                                          │
└──────────────────────────────────────────┘
```

### Cenário 2: Email Duplicado

```
┌──────────────────────────────────────────┐
│  Registrar Novo Paciente                 │
├──────────────────────────────────────────┤
│                                          │
│ ❌ Erro!                                 │
│ Este email já está cadastrado no sistema │
│                                          │
│ Nome: [João            ]                 │
│ Sobrenome: [Silva      ]                 │
│ CPF: [123.456.789-10   ]                 │
│ Email: [joao@gmail.com ]  ← PROBLEMA    │
│                                          │
│ [Cancelar]  [Registrar Paciente]         │
│                                          │
└──────────────────────────────────────────┘
```

### Cenário 3: Campo Obrigatório Vazio

```
┌──────────────────────────────────────────┐
│  Registrar Novo Paciente                 │
├──────────────────────────────────────────┤
│                                          │
│ ❌ Erro!                                 │
│ Preencha todos os campos obrigatórios!  │
│                                          │
│ Nome: [              ]  ← FALTA PREENCHER│
│ Sobrenome: [Silva      ]                 │
│ CPF: [123.456.789-10   ]                 │
│ Email: [joao@gmail.com ]                 │
│                                          │
│ [Cancelar]  [Registrar Paciente]         │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🔒 Verificações de Segurança

### Se você NÃO é Atendente/Admin:

```javascript
❌ Botão "Novo +" não aparece
❌ Modal não é carregado
❌ Script JavaScript não é incluído

Apenas usuários com permissão veem a funcionalidade!
```

### Se tentar enviar requisição diretamente:

```javascript
POST /pacientes/api/quick-register/

❌ Erro 403: Permissão Negada!

Apenas usuários logados e com permissão podem usar!
```

---

## 📱 Em Dispositivos Móveis

```
┌─────────────────────────────┐
│ Agendar Consulta            │
├─────────────────────────────┤
│                             │
│ Paciente:                   │
│ [Sel... ] [✚ Novo]         │
│                             │
│  ┌─────────────────────┐   │
│  │ 📋 Novo Paciente   │   │
│  ├─────────────────────┤   │
│  │ Nome:               │   │
│  │ [________        ]  │   │
│  │                     │   │
│  │ Email:              │   │
│  │ [__________     ]   │   │
│  │                     │   │
│  │ CPF:                │   │
│  │ [___.___.___-__]    │   │
│  │                     │   │
│  │  [Cancel][Register] │   │
│  └─────────────────────┘   │
│                             │
│ Médico:                     │
│ [Selecione...       ]       │
│                             │
└─────────────────────────────┘

✅ Modal responsivo e adaptado!
```

---

## 💾 Dados Salvos

Quando o paciente é registrado, o sistema salva:

```json
{
  "usuario": {
    "username": "123.456.789-10",
    "email": "joao@gmail.com",
    "first_name": "João",
    "last_name": "Silva",
    "cpf": "123.456.789-10",
    "phone": "(11) 98765-4321",
    "user_type": "patient",
    "is_active": true
  },
  "paciente": {
    "blood_type": "O+",
    "emergency_contact_name": "Maria Silva",
    "emergency_contact_phone": "(11) 99999-8888"
  }
}
```

---

## 🎯 Próximos Passos do Paciente

Após ser registrado pelo atendente:

1. **Paciente recebe email com login**
   - ✉️ Email: `joao@gmail.com`
   - 🔑 Username: `123.456.789-10`
   - 🔐 Senha temporária: gerada automaticamente

2. **Primeiro acesso**
   - Entra no sistema com seus dados
   - Completa cadastro (altura, peso, etc)
   - Vê sua consulta já agendada

3. **Acesso futuro**
   - Pode usar CPF ou Email para login
   - Pode recuperar senha se esquecer
   - Gerencia suas próprias consultas

---

**🎉 Tudo pronto! O cadastro inline está funcionando!**

Para dúvidas, veja: `CADASTRO_INLINE_ATENDENTE.md`
