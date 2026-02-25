# Configuração de Email para Recuperação de Senha

## Pré-requisitos

O sistema Promptuario está configurado para enviar emails de recuperação de senha. Para ativar essa funcionalidade, siga as instruções abaixo.

---

## Opção 1: Gmail (Recomendado)

### Passo 1: Habilitar Autenticação de Dois Fatores
1. Acesse https://myaccount.google.com
2. Navegue até "Segurança" no menu lateral
3. Ative "Autenticação de 2 etapas"

### Passo 2: Gerar Senha de Aplicativo
1. Retorne à página de Segurança
2. Em "Senhas de aplicativos", clique nessa opção
3. Selecione "Correio" e "Windows"
4. Clique em "Gerar"
5. Copie a senha de 16 caracteres gerada

### Passo 3: Configurar Variáveis de Ambiente
Edite o arquivo `.env` ou `.env.local` com:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app-google
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

---

## Opção 2: SendGrid

### Passo 1: Criar Conta SendGrid
1. Acesse https://sendgrid.com
2. Crie uma conta gratuita (até 100 emails/dia)
3. Confirme seu email

### Passo 2: Gerar Chave de API
1. No painel, vá para "Settings" > "API Keys"
2. Clique em "Create API Key"
3. Copie a chave gerada

### Passo 3: Configurar Variáveis de Ambiente
Edite o arquivo `.env` com:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.sua-chave-api-aqui
DEFAULT_FROM_EMAIL=seu-email@seudominio.com
```

---

## Opção 3: Outro Provedor SMTP

Se usar outro provedor (ex: Mailgun, Amazon SES, etc):

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.seuprovedorer.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-usuario
EMAIL_HOST_PASSWORD=sua-senha
DEFAULT_FROM_EMAIL=seu-email@seudominio.com
```

---

## Teste da Configuração

Para testar se o email está funcionando:

1. Acesse a página de login: `http://localhost:8000/accounts/login/`
2. Clique em "Esqueceu sua senha?"
3. Digite um email válido
4. Você deve receber um email com o link de recuperação

Se não receber o email:
- Verifique a pasta de Spam
- Verifique os logs do Django: `python manage.py shell`
- Teste a configuração:

```python
from django.core.mail import send_mail

send_mail(
    'Teste',
    'Este é um email de teste',
    'seu-email@gmail.com',
    ['seu-email@gmail.com'],
    fail_silently=False,
)
```

---

## Modo Desenvolvimento (Testes Locais)

Se quiser testar sem enviar emails reais, use:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Os emails aparecerão no console/terminal em vez de serem enviados.

---

## Dicas de Segurança

⚠️ **IMPORTANTE:**

1. **Nunca commite credenciais de email no Git**
   - Use variáveis de ambiente (arquivo `.env`)
   - Adicione `.env` ao `.gitignore`

2. **Use senhas de aplicativo, não senhas principais**
   - Gmail: Use senhas de aplicativo, não a senha da conta
   - SendGrid: Use API Keys, não a senha principal

3. **Em Produção:**
   - Use um servidor de email profissional (SendGrid, Amazon SES, etc)
   - Configure SSL/TLS corretamente
   - Monitore taxa de envio

4. **Domínio Próprio:**
   - Para credibilidade, configure um domínio próprio como sender
   - Exemplo: `noreply@meudominio.com` em vez de Gmail

---

## Troubleshooting

### "SMTPAuthenticationError: 535 Authentication failed"
- Verifique se a senha está correta
- Confirme que a autenticação de 2 fatores está ativa (Gmail)
- Verifique se gerou a senha de aplicativo corretamente

### "SMTPException: SMTP AUTH extension not supported"
- Verifique se `EMAIL_USE_TLS=True`
- Confirme a porta está correta (587 para TLS, 465 para SSL)

### Email não chega
- Verifique spam/filtros
- Confirme o email no `DEFAULT_FROM_EMAIL`
- Teste direto no shell Django

---

## Mais Informações

- [Documentação Django Email](https://docs.djangoproject.com/en/4.2/topics/email/)
- [Google App Passwords](https://support.google.com/accounts/answer/185833)
- [SendGrid Documentation](https://docs.sendgrid.com/)
