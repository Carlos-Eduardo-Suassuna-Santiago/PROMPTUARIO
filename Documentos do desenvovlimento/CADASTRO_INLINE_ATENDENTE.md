# Implementação: Cadastro de Paciente Inline para Atendentes

## 📋 Resumo da Implementação

O atendente (e admin) agora pode **registrar um novo paciente SEM SAIR DA PÁGINA DE AGENDAMENTO**, através de um modal (janela pop-up) interativo com validações em tempo real.

## ✨ Funcionalidades Implementadas

### 1. **Formulário Simplificado de Registro Rápido** (`QuickPatientRegistrationForm`)
   - **Localização**: `patients/forms.py`
   - **Campos**:
     - Nome (obrigatório)
     - Sobrenome (obrigatório)
     - CPF (obrigatório, validação de duplicação)
     - Email (obrigatório, validação de duplicação)
     - Telefone (opcional)
     - Tipo de Sangue (opcional)
     - Contato de Emergência (opcional)
   - **Validações**:
     - Verifica CPF duplicado
     - Verifica email duplicado
     - Cria usuário e perfil de paciente automaticamente

### 2. **View AJAX para Registro** (`QuickPatientRegistrationView`)
   - **Localização**: `patients/views.py`
   - **Endpoint**: `/pacientes/api/quick-register/`
   - **Método**: POST (JSON)
   - **Permissões**: Apenas atendentes e admins
   - **Resposta**:
     - Sucesso: Retorna dados do paciente criado (id, name, cpf, email)
     - Erro: Retorna mensagens de validação para cada campo

### 3. **Modal Bootstrap** no Template de Agendamento
   - **Localização**: `templates/appointments/appointment_form.html`
   - **Visibilidade**: Apenas para atendentes e admins
   - **Botão de Acesso**: "Novo +" ao lado do campo de seleção de paciente
   - **Campos do Modal**:
     - Formulário com todos os campos do registro rápido
     - Máscaras de entrada (CPF e Telefone)
     - Validação em tempo real
     - Alerta informativo sobre o fluxo
     - Botões: Cancelar | Registrar Paciente

### 4. **Script JavaScript** para Interatividade
   - **Localização**: `static/js/quick_patient_register.js` (NOVO)
   - **Funcionalidades**:
     - Máscaras de CPF: `000.000.000-00`
     - Máscaras de Telefone: `(11) 99999-9999`
     - Validação de formulário no cliente
     - Envio AJAX com CSRF token
     - Tratamento de sucesso/erro
     - Auto-adicionar paciente ao dropdown após criação
     - Fechar modal automaticamente após sucesso
     - Exibição de alertas responsivos

## 🔄 Fluxo de Funcionamento

```
1. Atendente está na página de agendamento
2. Clica no botão "Novo +" ao lado do campo de paciente
3. Modal se abre com formulário de registro
4. Preenche os dados do paciente
5. Clica em "Registrar Paciente"
6. JavaScript valida dados no cliente
7. Envia requisição AJAX para /pacientes/api/quick-register/
8. Backend valida, cria usuário e perfil de paciente
9. Retorna sucesso com dados do paciente
10. JavaScript:
    - Adiciona novo paciente ao dropdown (já selecionado)
    - Fecha o modal
    - Mostra mensagem de sucesso
    - Limpa o formulário do modal
11. Atendente continua preenchendo os dados da consulta
12. Submete o agendamento normalmente
```

## 📁 Arquivos Modificados/Criados

### Criados:
- ✅ `static/js/quick_patient_register.js` - Script de interatividade

### Modificados:
- ✅ `patients/forms.py` - Adicionado `QuickPatientRegistrationForm`
- ✅ `patients/views.py` - Adicionado `QuickPatientRegistrationView` e ajustes de import
- ✅ `patients/urls.py` - Adicionado route `/pacientes/api/quick-register/`
- ✅ `templates/appointments/appointment_form.html` - Adicionado modal e botão de registro

## 🛡️ Validações e Segurança

### No Cliente (JavaScript):
- ✅ Campos obrigatórios
- ✅ Formato de CPF
- ✅ Formato de Email

### No Servidor (Django):
- ✅ Autenticação (LoginRequiredMixin)
- ✅ Autorização (apenas atendente/admin)
- ✅ Validação de CPF único
- ✅ Validação de Email único
- ✅ CSRF Protection

## 📱 Responsividade

- ✅ Modal responsive (tamanho adapta a tela)
- ✅ Formulário em grid responsivo (col-md-6)
- ✅ Botões adaptáveis
- ✅ Alerta responsivo

## 🚀 Como Usar

### Para Atendentes:

1. Acesse `/agendamentos/criar/` (criar agendamento)
2. Clique em "Novo +" ao lado do campo "Paciente"
3. Preencha o formulário modal
4. Clique em "Registrar Paciente"
5. O paciente aparecerá automaticamente selecionado
6. Continua preenchendo o agendamento normalmente

### Campos Mínimos Obrigatórios:
- Nome
- Sobrenome
- CPF (formato: 000.000.000-00)
- Email

### Campos Opcionais:
- Telefone
- Tipo de Sangue
- Contato de Emergência

## 💡 Nota Importante

O paciente registrado via formulário rápido:
- ✅ Pode fazer login imediatamente
- ✅ Precisa completar seu cadastro na primeira vez (altura, peso, etc)
- ⚠️ Uma senha será gerada aleatoriamente (pode ser resetada via "Esqueci a Senha")
- ✅ Será vinculado ao agendamento criado pelo atendente

## 🔗 URLs e Endpoints

| Rota | Método | Descrição |
|------|--------|-----------|
| `/pacientes/api/quick-register/` | POST | Registro rápido de paciente via AJAX |
| `/agendamentos/criar/` | GET/POST | Formulário de agendamento (com modal integrado) |

## ✅ Testes Recomendados

- [ ] Atendente clica "Novo +" → Modal abre
- [ ] Preenche todos os campos → Validação passa
- [ ] Deixa campo obrigatório vazio → Validação falha
- [ ] CPF duplicado → Erro no servidor
- [ ] Email duplicado → Erro no servidor
- [ ] Registro com sucesso → Paciente aparece no dropdown
- [ ] Modal fecha após sucesso
- [ ] Agendamento completa normalmente

## 🔮 Melhorias Futuras (Opcionais)

1. **Validação de CPF com algoritmo mod-11**
   - Já temos JavaScript para isso em profile_form.js
   - Pode ser integrado ao quick_patient_register.js

2. **Geração automática de senha**
   - Atualmente gera automaticamente
   - Pode ser customizado

3. **Envio de email com credenciais**
   - Opcional: enviar email ao paciente com usuario/senha
   - Usar sinal (signal) post_save

4. **Preview de dados do paciente após criação**
   - Mostrar resumo antes de fechar modal

5. **Busca com autocomplete antes de criar**
   - Verificar se paciente já existe antes do modal

