# Promptuario - Histórico de Mudanças

## Versão 1.0.0 - Implementação Completa (Foco em Médico, Atendente e Admin)

### Novas Funcionalidades

- **Funcionalidades do Médico:**
    - Implementação completa do fluxo de Prontuário Eletrônico (CRUD).
    - Geração de Receitas Médicas em PDF (usando `reportlab`).
    - Solicitação de Exames.
    - Visualização detalhada de Pacientes com histórico médico completo.
    - Relatórios de Produtividade (Consultas, Pacientes).

- **Funcionalidades do Atendente:**
    - Dashboard com visualização de agendamentos do dia e pendentes.
    - Gerenciamento de Check-in e Check-out de consultas.

- **Funcionalidades do Administrador:**
    - Gerenciamento completo de Usuários (CRUD) com filtros por tipo.
    - **Conformidade LGPD:** Implementação de Logs de Acesso para rastreabilidade de visualização de dados sensíveis (pacientes e prontuários).

- **Estrutura e Segurança:**
    - Criação de Mixins de permissão (`DoctorRequiredMixin`, `AdminRequiredMixin`).
    - Templates de Dashboard específicos por tipo de usuário (`dashboard_doctor.html`, `dashboard_attendant.html`, etc.).
    - Ajustes finos em formulários e templates para melhor usabilidade.

### Correções e Melhorias

- Refatoração de views para usar Mixins de permissão.
- Ajuste na lógica de filtragem de agendamentos para médicos.
- Correção de bugs menores em templates e URLs.
- Melhoria na estrutura de arquivos do projeto.
