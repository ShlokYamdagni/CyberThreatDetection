/**
 * CyberShield AI - Chart.js Dashboard Charts
 * Initializes all dashboard charts with cybersecurity theme colors.
 */

// ─── Chart.js Global Defaults ───────────────────────
Chart.defaults.color = '#8892b0';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";

// ─── Model Comparison Chart ─────────────────────────
function initModelComparisonChart(trainingData) {
    const canvas = document.getElementById('modelComparisonChart');
    if (!canvas || !trainingData || !trainingData.results) return;

    const results = trainingData.results;
    const labels = Object.keys(results);
    const bestModel = trainingData.best_model;

    const datasets = [
        {
            label: 'Accuracy',
            data: labels.map(l => (results[l].accuracy * 100).toFixed(2)),
            backgroundColor: 'rgba(0, 229, 255, 0.7)',
            borderColor: '#00e5ff',
            borderWidth: 1,
            borderRadius: 6,
        },
        {
            label: 'Precision',
            data: labels.map(l => (results[l].precision * 100).toFixed(2)),
            backgroundColor: 'rgba(0, 230, 118, 0.7)',
            borderColor: '#00e676',
            borderWidth: 1,
            borderRadius: 6,
        },
        {
            label: 'Recall',
            data: labels.map(l => (results[l].recall * 100).toFixed(2)),
            backgroundColor: 'rgba(41, 121, 255, 0.7)',
            borderColor: '#2979ff',
            borderWidth: 1,
            borderRadius: 6,
        },
        {
            label: 'F1 Score',
            data: labels.map(l => (results[l].f1_score * 100).toFixed(2)),
            backgroundColor: 'rgba(124, 77, 255, 0.7)',
            borderColor: '#7c4dff',
            borderWidth: 1,
            borderRadius: 6,
        }
    ];

    new Chart(canvas, {
        type: 'bar',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'roundRect',
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 22, 35, 0.95)',
                    titleColor: '#00e5ff',
                    bodyColor: '#e8eaf6',
                    borderColor: 'rgba(0, 229, 255, 0.2)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    callbacks: {
                        label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: Math.max(0, Math.min(...Object.values(results).map(r => r.accuracy * 100)) - 10),
                    grid: { color: 'rgba(255, 255, 255, 0.04)' },
                    ticks: { callback: v => v + '%' }
                },
                x: {
                    grid: { display: false },
                    ticks: { maxRotation: 45 }
                }
            }
        }
    });
}

// ─── Threat Distribution Pie Chart ──────────────────
function initThreatDistChart(stats) {
    const canvas = document.getElementById('threatDistChart');
    if (!canvas) return;

    const normal = stats.normal_detected || 0;
    const threats = stats.threats_detected || 0;

    if (normal === 0 && threats === 0) {
        // No data yet
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: ['No Data'],
                datasets: [{
                    data: [1],
                    backgroundColor: ['rgba(255,255,255,0.05)'],
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '70%',
            }
        });
        return;
    }

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Normal Traffic', 'Threats Detected'],
            datasets: [{
                data: [normal, threats],
                backgroundColor: [
                    'rgba(0, 230, 118, 0.8)',
                    'rgba(255, 23, 68, 0.8)',
                ],
                borderColor: [
                    '#00e676',
                    '#ff1744',
                ],
                borderWidth: 2,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle',
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 22, 35, 0.95)',
                    titleColor: '#00e5ff',
                    bodyColor: '#e8eaf6',
                    borderColor: 'rgba(0, 229, 255, 0.2)',
                    borderWidth: 1,
                    cornerRadius: 8,
                }
            }
        }
    });
}

// ─── Metrics Radar Chart ────────────────────────────
function initMetricsRadarChart(trainingData) {
    const canvas = document.getElementById('metricsRadarChart');
    if (!canvas || !trainingData || !trainingData.results) return;

    const results = trainingData.results;
    const bestModel = trainingData.best_model;
    const m = results[bestModel];
    if (!m) return;

    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC'],
            datasets: [{
                label: bestModel,
                data: [m.accuracy, m.precision, m.recall, m.f1_score, m.roc_auc || 0],
                backgroundColor: 'rgba(0, 229, 255, 0.12)',
                borderColor: '#00e5ff',
                borderWidth: 2,
                pointBackgroundColor: '#00e5ff',
                pointBorderColor: '#fff',
                pointRadius: 5,
                pointHoverRadius: 7,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 20 }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    grid: { color: 'rgba(255, 255, 255, 0.06)' },
                    pointLabels: {
                        color: '#8892b0',
                        font: { size: 11 }
                    },
                    ticks: { display: false },
                    angleLines: { color: 'rgba(255, 255, 255, 0.06)' },
                }
            }
        }
    });
}

// ─── Confusion Matrix ───────────────────────────────
function initConfusionMatrix(trainingData) {
    const container = document.getElementById('confusionMatrix');
    if (!container || !trainingData || !trainingData.results) return;

    const bestModel = trainingData.best_model;
    const m = trainingData.results[bestModel];
    if (!m || !m.confusion_matrix) return;

    const cm = m.confusion_matrix;
    const total = cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1];

    container.innerHTML = `
        <div class="cm-grid">
            <div class="cm-corner"></div>
            <div class="cm-header">Pred Normal</div>
            <div class="cm-header">Pred Attack</div>
            <div class="cm-label">Actual Normal</div>
            <div class="cm-cell cm-tn">
                ${cm[0][0]}<br><small>${((cm[0][0]/total)*100).toFixed(1)}%</small>
            </div>
            <div class="cm-cell cm-fp">
                ${cm[0][1]}<br><small>${((cm[0][1]/total)*100).toFixed(1)}%</small>
            </div>
            <div class="cm-label">Actual Attack</div>
            <div class="cm-cell cm-fn">
                ${cm[1][0]}<br><small>${((cm[1][0]/total)*100).toFixed(1)}%</small>
            </div>
            <div class="cm-cell cm-tp">
                ${cm[1][1]}<br><small>${((cm[1][1]/total)*100).toFixed(1)}%</small>
            </div>
        </div>
    `;
}
