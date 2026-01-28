/**
 * Calendar Management Script
 * Gerencia a visualização do calendário de agendamentos
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeCalendarView();
});

/**
 * Inicializar visualização do calendário
 */
function initializeCalendarView() {
    // Verificar se FullCalendar está disponível
    if (typeof FullCalendar === 'undefined') {
        console.warn('FullCalendar não está carregado. Usando visualização de fallback.');
        return;
    }

    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: ''
        },
        locale: 'pt-br',
        height: 'auto',
        contentHeight: 'auto',
        events: loadCalendarEvents,
        eventClick: handleEventClick,
        datesSet: function(info) {
            calendar.refetchEvents();
        },
        editable: false,
        selectable: true,
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            meridiem: false,
            hour12: false
        },
        eventDisplay: 'block',
        dayMaxEventRows: 3,
        moreLinkClick: 'popover'
    });

    calendar.render();

    // Alternar visualizações
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            viewButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            calendar.changeView(this.dataset.view);
        });
    });

    // Armazenar referência global
    window.appointmentCalendar = calendar;
}

/**
 * Carregar eventos do servidor
 */
function loadCalendarEvents(info, successCallback, failureCallback) {
    // Tentar buscar a URL da API
    const apiUrl = document.querySelector('[data-calendar-api]')?.getAttribute('data-calendar-api') 
        || '/appointments/api/list/';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar eventos');
            }
            return response.json();
        })
        .then(data => {
            const events = data.map(appointment => {
                const startDateTime = new Date(appointment.scheduled_date + 'T' + appointment.scheduled_time);
                
                return {
                    id: appointment.id,
                    title: appointment.patient_name || 'Consulta',
                    start: startDateTime.toISOString(),
                    extendedProps: {
                        patient: appointment.patient_name,
                        doctor: appointment.doctor_name,
                        status: appointment.status,
                        reason: appointment.reason,
                        appointmentId: appointment.id
                    },
                    classNames: ['status-' + (appointment.status || 'scheduled')]
                };
            });
            successCallback(events);
        })
        .catch(error => {
            console.error('Erro ao carregar eventos do calendário:', error);
            failureCallback(error);
        });
}

/**
 * Manipular clique em evento
 */
function handleEventClick(info) {
    const event = info.event;
    const props = event.extendedProps;

    const statusBadgeClass = {
        'scheduled': 'bg-warning',
        'confirmed': 'bg-success',
        'completed': 'bg-secondary',
        'cancelled': 'bg-danger'
    };

    const statusDisplay = {
        'scheduled': 'Agendado',
        'confirmed': 'Confirmado',
        'completed': 'Concluído',
        'cancelled': 'Cancelado'
    };

    // Criar conteúdo do modal
    const startDate = event.start.toLocaleDateString('pt-BR');
    const startTime = event.start.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    let detailsHTML = `
        <div class="event-popup">
            <h4>${props.patient || 'Consulta'}</h4>
            <p><strong>Médico:</strong> ${props.doctor || 'N/A'}</p>
            <p><strong>Data/Hora:</strong> ${startDate} às ${startTime}</p>
    `;

    if (props.reason) {
        detailsHTML += `<p><strong>Motivo:</strong> ${props.reason}</p>`;
    }

    detailsHTML += `
            <span class="badge ${statusBadgeClass[props.status] || 'bg-secondary'}">
                ${statusDisplay[props.status] || 'Desconhecido'}
            </span>
            <div class="actions">
                <a href="/appointments/${props.appointmentId}/" class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-eye"></i> Ver Detalhes
                </a>
                <a href="/appointments/${props.appointmentId}/edit/" class="btn btn-outline-secondary btn-sm">
                    <i class="fas fa-edit"></i> Editar
                </a>
            </div>
        </div>
    `;

    // Atualizar modal
    const eventDetails = document.getElementById('eventDetails');
    if (eventDetails) {
        eventDetails.innerHTML = detailsHTML;
        
        // Mostrar modal
        const eventModal = document.getElementById('eventModal');
        if (eventModal) {
            const modal = new bootstrap.Modal(eventModal);
            modal.show();
        }
    }
}

/**
 * Atualizar calendário
 */
function refreshCalendar() {
    if (window.appointmentCalendar) {
        window.appointmentCalendar.refetchEvents();
    }
}

/**
 * Navegar para data específica
 */
function goToDate(dateString) {
    if (window.appointmentCalendar) {
        window.appointmentCalendar.gotoDate(dateString);
    }
}

/**
 * Mudar visualização
 */
function changeCalendarView(viewName) {
    if (window.appointmentCalendar) {
        window.appointmentCalendar.changeView(viewName);
    }
}
