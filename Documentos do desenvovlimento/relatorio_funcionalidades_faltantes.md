# Relatório de Análise de Funcionalidades Faltantes no Front-end (Promptuario)

**Autor:** Manus AI
**Data:** 18 de Janeiro de 2026
**Projeto:** Promptuario (Baseado em Django)

## Introdução

O projeto "Promptuario" apresenta uma estrutura de back-end robusta, baseada no framework Django, com modelos e *views* bem definidos para as principais funcionalidades de um sistema de prontuário eletrônico (agendamentos, pacientes, prontuários, relatórios e contas de usuário).

No entanto, a análise do *front-end* (templates HTML e arquivos estáticos) indica que a usabilidade e a experiência do usuário (UX) estão comprometidas pela falta de implementação de componentes dinâmicos e interativos, essenciais para um sistema moderno de gestão clínica.

A lista a seguir detalha as funcionalidades que **faltam ser implementadas no front-end** para que o sistema seja considerado 100% utilizável, agrupadas por módulo.

## 1. Módulo de Agendamentos (`appointments`)

O módulo de agendamentos é o que apresenta a maior lacuna em termos de interatividade e usabilidade.

| Funcionalidade Faltante | Descrição e Impacto na Usabilidade |
| :--- | :--- |
| **Visualização de Calendário Interativo** | O template `appointment_calendar.html` é um *placeholder* que exibe apenas uma lista de agendamentos. Falta a integração com uma biblioteca JavaScript (como FullCalendar) para exibir os agendamentos em um **calendário visual e interativo** (dia, semana, mês), permitindo arrastar, redimensionar e clicar em eventos. |
| **API de Dados para Calendário** | O back-end não possui um *endpoint* JSON dedicado para fornecer os dados de agendamento no formato esperado por bibliotecas de calendário (e.g., `/api/appointments/events/`). Isso é crucial para carregar os dados de forma assíncrona. |
| **Fluxo de Agendamento Dinâmico (Paciente)** | O fluxo de agendamento do paciente (`patient_booking_*`) provavelmente utiliza formulários estáticos. Falta a implementação de uma interface **dinâmica e responsiva** para: 1. Seleção de médico com filtros. 2. Visualização de horários disponíveis em tempo real (via AJAX). 3. Confirmação de agendamento sem recarregar a página. |
| **Ações de Check-in/Check-out na Lista** | Embora as *views* de `AppointmentCheckInView` e `AppointmentCheckOutView` existam, a lista de agendamentos precisa de botões de ação visíveis e dinâmicos para que o atendente possa alterar o status da consulta rapidamente. |

## 2. Módulo de Prontuários Médicos (`medical_records`)

O módulo de prontuários possui a estrutura de dados completa, mas carece de ferramentas de visualização e edição ricas.

| Funcionalidade Faltante | Descrição e Impacto na Usabilidade |
| :--- | :--- |
| **Geração e Visualização de Receitas/Exames** | O template `medical_record_detail.html` possui botões para "Gerar PDF" e "Visualizar Receita/Exame" que estão desabilitados ou apontam para `#`. Falta a implementação do *front-end* para: 1. Acionar a geração do PDF (que o back-end já suporta via ReportLab). 2. Exibir o PDF gerado em um *modal* ou nova aba. 3. Criar as páginas de detalhe (`prescription_detail.html`, `exam_detail.html`). |
| **Editor de Texto Rico (Rich Text Editor)** | Campos como `chief_complaint`, `physical_examination`, `diagnosis` e `treatment_plan` em `MedicalRecord` se beneficiariam enormemente de um **editor de texto rico** (e.g., TinyMCE, CKEditor) para formatação de texto, listas e tabelas, melhorando a qualidade da documentação clínica. |
| **Interface de Busca e Filtro de Prontuários** | A listagem de prontuários (`medical_record_list.html`) precisa de uma interface de busca e filtro avançada (por paciente, médico, data, diagnóstico) para facilitar a localização de registros. |

## 3. Módulo de Gerenciamento de Usuários e Perfis (`accounts`, `patients`)

O gerenciamento de dados mestres e perfis é funcional, mas a experiência de administração é básica.

| Funcionalidade Faltante | Descrição e Impacto na Usabilidade |
| :--- | :--- |
| **Gerenciamento Visual de Horários do Médico** | A página `doctor_schedule.html` para gerenciar `DoctorSchedule` e `DoctorAbsence` requer uma interface visual (e.g., um **calendário de agendamento de disponibilidade**) para criar, editar e excluir horários de trabalho e ausências de forma intuitiva, em vez de apenas formulários simples. |
| **Busca e Filtragem Dinâmica (AJAX)** | As listas de usuários (`user_list.html`), médicos (`doctor_list.html`) e pacientes (`patient_list.html`) utilizam submissão de formulário para busca. A implementação de **busca e filtragem assíncrona (AJAX)** melhoraria a performance e a UX ao evitar o recarregamento completo da página. |
| **Upload e Visualização de Foto de Perfil** | O *front-end* precisa de um componente de *upload* de imagem mais amigável e uma pré-visualização da foto de perfil (`profile_form.html`), que o back-end já suporta. |

## 4. Módulo de Relatórios (`reports`) e Dashboard

O back-end fornece os dados de relatórios, mas o *front-end* não os apresenta de forma visual.

| Funcionalidade Faltante | Descrição e Impacto na Usabilidade |
| :--- | :--- |
| **Visualização de Dados (Gráficos e Dashboards)** | O `dashboard_doctor.html` e o `doctor_report.html` exibem apenas números e listas. Falta a integração com uma biblioteca de gráficos (e.g., **Chart.js**) para transformar dados como `top_diagnoses`, `recent_appointments_count` e `total_appointments` em **gráficos e *dashboards* visuais** (barras, pizza, linhas), tornando a análise de dados mais rápida e eficaz. |
| **Interface de Geração de Relatórios** | A página `report_generate.html` precisa de uma interface para seleção de filtros (período, médico, tipo de relatório) antes de acionar a geração do relatório, que atualmente parece ser acionada por um `POST` simples. |

## 5. Experiência Geral do Usuário (UX)

Melhorias gerais que impactam a usabilidade de todo o sistema.

| Funcionalidade Faltante | Descrição e Impacto na Usabilidade |
| :--- | :--- |
| **Notificações em Tempo Real** | O modelo `AppointmentNotification` existe, mas não há um mecanismo de *front-end* (e.g., WebSockets, *polling*) para exibir **notificações em tempo real** (e.g., novo agendamento, cancelamento) para atendentes e médicos. |
| **Componentes de Data/Hora Interativos** | A maioria dos campos de data e hora em formulários provavelmente usa campos de texto simples. A implementação de **seletores de data e hora (Date/Time Pickers)** melhora a precisão e a usabilidade. |
| **Validação de Formulários Client-Side** | O `main.js` possui apenas formatadores básicos. É necessário implementar uma **validação de formulário abrangente no lado do cliente** para fornecer *feedback* imediato ao usuário antes da submissão ao servidor. |
| **Componentes de Confirmação e Alerta** | Implementação de *modals* e *toasts* padronizados para confirmações de ações (exclusão, cancelamento) e exibição de mensagens do sistema (sucesso, erro), substituindo os alertas nativos do navegador. |

## Conclusão

Para que o sistema "Promptuario" atinja 100% de usabilidade, o foco principal deve ser na **interatividade e visualização de dados** no *front-end*. A maior parte da lógica de back-end está estabelecida; o próximo passo é transformar os dados e formulários estáticos em uma experiência de usuário moderna e dinâmica, utilizando bibliotecas JavaScript para calendário, gráficos e componentes de formulário avançados.
