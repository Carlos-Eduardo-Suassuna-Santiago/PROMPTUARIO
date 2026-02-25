/**
 * Charts Script
 * Gerencia gráficos com Chart.js para dashboards
 */

// Armazenar referências dos gráficos
const charts = {};

/**
 * Inicializar todos os gráficos na página
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

/**
 * Inicializar gráficos
 */
function initializeCharts() {
    const chartElements = document.querySelectorAll('[data-chart]');
    
    chartElements.forEach(element => {
        const chartType = element.dataset.chart;
        const chartId = element.id;
        
        if (!chartId) {
            console.warn('Elemento de gráfico sem ID encontrado');
            return;
        }

        // Obter dados do elemento
        const chartData = element.dataset.chartData ? JSON.parse(element.dataset.chartData) : null;
        
        if (!chartData) {
            console.warn(`Nenhum dado fornecido para o gráfico ${chartId}`);
            return;
        }

        // Criar gráfico apropriado
        switch(chartType) {
            case 'line':
                createLineChart(chartId, chartData);
                break;
            case 'bar':
                createBarChart(chartId, chartData);
                break;
            case 'pie':
                createPieChart(chartId, chartData);
                break;
            case 'doughnut':
                createDoughnutChart(chartId, chartData);
                break;
            default:
                console.warn(`Tipo de gráfico desconhecido: ${chartType}`);
        }
    });
}

/**
 * Criar gráfico de linha
 */
function createLineChart(chartId, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    charts[chartId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    cornerRadius: 6
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: { size: 11 }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: { size: 11 }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Criar gráfico de barras
 */
function createBarChart(chartId, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    charts[chartId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: data.indexAxis || 'x',
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    cornerRadius: 6
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: { size: 11 }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: { size: 11 }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Criar gráfico de pizza
 */
function createPieChart(chartId, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    charts[chartId] = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    cornerRadius: 6,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Criar gráfico de rosca
 */
function createDoughnutChart(chartId, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    charts[chartId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    cornerRadius: 6,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Atualizar dados de um gráfico
 */
function updateChart(chartId, newData) {
    const chart = charts[chartId];
    if (!chart) {
        console.warn(`Gráfico ${chartId} não encontrado`);
        return;
    }

    if (newData.labels) {
        chart.data.labels = newData.labels;
    }

    if (newData.datasets) {
        chart.data.datasets = newData.datasets;
    }

    chart.update();
}

/**
 * Destruir gráfico
 */
function destroyChart(chartId) {
    const chart = charts[chartId];
    if (chart) {
        chart.destroy();
        delete charts[chartId];
    }
}

/**
 * Exportar gráfico como imagem
 */
function exportChartAsImage(chartId, filename = 'chart.png') {
    const chart = charts[chartId];
    if (!chart) {
        console.warn(`Gráfico ${chartId} não encontrado`);
        return;
    }

    const link = document.createElement('a');
    link.href = chart.canvas.toDataURL('image/png');
    link.download = filename;
    link.click();
}

/**
 * Cores padrão para gráficos
 */
const chartColors = {
    primary: 'rgba(14, 165, 233, 0.8)',
    success: 'rgba(16, 185, 129, 0.8)',
    danger: 'rgba(239, 68, 68, 0.8)',
    warning: 'rgba(245, 158, 11, 0.8)',
    info: 'rgba(59, 130, 246, 0.8)',
    secondary: 'rgba(148, 163, 184, 0.8)',
    
    primaryLight: 'rgba(14, 165, 233, 0.1)',
    successLight: 'rgba(16, 185, 129, 0.1)',
    dangerLight: 'rgba(239, 68, 68, 0.1)',
    warningLight: 'rgba(245, 158, 11, 0.1)',
    infoLight: 'rgba(59, 130, 246, 0.1)',
    secondaryLight: 'rgba(148, 163, 184, 0.1)',

    primaryBorder: 'rgb(14, 165, 233)',
    successBorder: 'rgb(16, 185, 129)',
    dangerBorder: 'rgb(239, 68, 68)',
    warningBorder: 'rgb(245, 158, 11)',
    infoBorder: 'rgb(59, 130, 246)',
    secondaryBorder: 'rgb(148, 163, 184)'
};

/**
 * Paleta de cores para gráficos de pizza/rosca
 */
const chartPalette = [
    'rgba(14, 165, 233, 0.8)',
    'rgba(16, 185, 129, 0.8)',
    'rgba(239, 68, 68, 0.8)',
    'rgba(245, 158, 11, 0.8)',
    'rgba(59, 130, 246, 0.8)',
    'rgba(168, 85, 247, 0.8)',
    'rgba(236, 72, 153, 0.8)',
    'rgba(34, 197, 94, 0.8)'
];

/**
 * Paleta de cores para bordas
 */
const chartPaletteBorder = [
    'rgb(14, 165, 233)',
    'rgb(16, 185, 129)',
    'rgb(239, 68, 68)',
    'rgb(245, 158, 11)',
    'rgb(59, 130, 246)',
    'rgb(168, 85, 247)',
    'rgb(236, 72, 153)',
    'rgb(34, 197, 94)'
];
