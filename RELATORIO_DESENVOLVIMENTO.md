# Relatório de Desenvolvimento do Sistema Promptuario (Prontuário Eletrônico)

## Introdução

Este relatório detalha o processo de desenvolvimento e as funcionalidades implementadas no sistema **Promptuario**, um Prontuário Eletrônico (EHR) construído com o framework **Django** e focado em atender às necessidades de **Médicos**, **Atendentes** e **Administradores** em uma unidade de saúde. O projeto seguiu uma abordagem modular, garantindo escalabilidade e manutenção.

## Funcionalidades Implementadas por Perfil

O sistema utiliza um modelo de usuário customizado com perfis (`User`, `DoctorProfile`, `AttendantProfile`, `Patient`) para gerenciar o acesso e as funcionalidades de forma granular.

### 1. Médico (Doctor)

O foco principal foi fornecer um fluxo de trabalho completo para o atendimento clínico.

| Funcionalidade | Descrição | Implementação |
| :--- | :--- | :--- |
| **Prontuário Eletrônico** | Criação, visualização e edição de prontuários médicos por consulta. | Views baseadas em `CreateView` e `UpdateView` (`MedicalRecordCreateView`, `MedicalRecordUpdateView`) com Mixins de permissão (`DoctorRequiredMixin`). |
| **Geração de Receita** | Criação de receitas médicas com geração automática de PDF. | `PrescriptionCreateView` integrada com a biblioteca `reportlab` para saída em PDF. |
| **Solicitação de Exame** | Registro de solicitações de exames. | `ExamCreateView` para registro e associação ao prontuário. |
| **Detalhe do Paciente** | Acesso ao histórico completo do paciente (alergias, vacinas, medicamentos, prontuários). | `PatientDetailView` com lógica de permissão para médicos. |
| **Relatórios** | Visualização de dados de produtividade (consultas, pacientes). | `DoctorReportView` para agregação e exibição de dados. |

### 2. Atendente (Attendant)

O Atendente é responsável pela gestão da recepção e do fluxo de pacientes.

| Funcionalidade | Descrição | Implementação |
| :--- | :--- | :--- |
| **Dashboard** | Visão geral dos agendamentos do dia e pendentes. | `DashboardView` com template específico (`dashboard_attendant.html`) e filtros de consulta. |
| **Agendamento** | Criação de novas consultas para pacientes. | `AppointmentCreateView` utilizando `AttendantAppointmentForm`. |
| **Check-in/Check-out** | Gerenciamento do status da consulta (entrada e saída do paciente). | Views baseadas em `View` (`AppointmentCheckInView`, `AppointmentCheckOutView`) com Mixins de permissão. |

### 3. Administrador (Admin)

O Administrador possui controle total sobre o sistema e a gestão de usuários.

| Funcionalidade | Descrição | Implementação |
| :--- | :--- | :--- |
| **Dashboard** | Métricas gerais do sistema (total de usuários, médicos, pacientes). | `DashboardView` com template específico (`dashboard_admin.html`). |
| **Gerenciamento de Usuários** | CRUD completo de todos os tipos de usuários. | Views baseadas em `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` com `AdminRequiredMixin`. |
| **Logs de Acesso (LGPD)** | Rastreamento de acessos a dados sensíveis. | Modelo `AccessLog`, `AccessLogMiddleware` e `AccessLogListView` para visualização e filtragem. |

## Conformidade com a LGPD (Lei Geral de Proteção de Dados)

A conformidade com a LGPD foi abordada com a implementação de um robusto sistema de **Logs de Acesso**.

- **Modelo `AccessLog`:** Registra o usuário, a ação (e.g., `view_patient`, `view_record`, `generate_pdf`), o timestamp, o endereço IP e detalhes da operação.
- **`AccessLogMiddleware`:** Garante o registro automático de eventos de `login` e `logout`.
- **Integração nas Views:** As views de detalhe de paciente (`PatientDetailView`) e de prontuário (`MedicalRecordDetailView`), bem como as de geração de documentos (`PrescriptionCreateView`, `ExamCreateView`), foram instrumentadas com a função `log_access` para registrar o acesso a dados sensíveis.

## Estrutura do Projeto e Tecnologias

- **Framework:** Django (Python)
- **Banco de Dados:** SQLite (padrão, configurável via `DATABASE_URL`)
- **Geração de PDF:** `reportlab`
- **Frontend:** Templates Django com Bootstrap (via `crispy-forms` e `crispy-bootstrap5`)

## Próximos Passos Sugeridos

1.  **Testes de Integração:** Implementar testes automatizados para as novas funcionalidades.
2.  **Agendamento Online:** Permitir que pacientes agendem consultas diretamente, verificando a disponibilidade do médico.
3.  **Módulo de Faturamento:** Adicionar um módulo para gerenciar faturas e pagamentos.

---
*Este relatório marca a conclusão da fase de implementação principal do sistema Promptuario.*
