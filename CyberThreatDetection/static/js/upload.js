/**
 * CyberShield AI - File Upload Handler
 * Handles drag-and-drop CSV upload with progress tracking.
 */

let selectedFile = null;
let resultFileName = null;

// ─── Drag & Drop Setup ─────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    if (!dropZone || !fileInput) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight on drag
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        }, false);
    });

    // Handle drop
    dropZone.addEventListener('drop', function(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }, false);

    // Handle file input change
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFile(this.files[0]);
        }
    });
});

// ─── File Handling ──────────────────────────────────
function handleFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showToast('Please upload a CSV file only.', 'error');
        return;
    }

    // Validate file size (16 MB)
    if (file.size > 16 * 1024 * 1024) {
        showToast('File size exceeds 16 MB limit.', 'error');
        return;
    }

    selectedFile = file;

    // Show file info
    const selectedDiv = document.getElementById('selectedFile');
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    selectedDiv.classList.remove('d-none');

    // Enable upload button
    document.getElementById('uploadBtn').disabled = false;

    showToast(`File "${file.name}" selected.`, 'info');
}

function clearFile() {
    selectedFile = null;
    document.getElementById('selectedFile').classList.add('d-none');
    document.getElementById('uploadBtn').disabled = true;
    document.getElementById('fileInput').value = '';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ─── Upload File ────────────────────────────────────
async function uploadFile() {
    if (!selectedFile) {
        showToast('Please select a file first.', 'error');
        return;
    }

    const uploadBtn = document.getElementById('uploadBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const resultsArea = document.getElementById('resultsArea');

    // Show progress
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Analyzing...';
    progressContainer.classList.remove('d-none');
    progressBar.style.width = '10%';
    progressText.textContent = 'Uploading file...';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Simulate progress steps
        progressBar.style.width = '30%';
        progressText.textContent = 'Processing data...';

        const response = await fetch('/api/predict-batch', {
            method: 'POST',
            body: formData
        });

        progressBar.style.width = '70%';
        progressText.textContent = 'Running predictions...';

        const data = await response.json();

        progressBar.style.width = '100%';
        progressText.textContent = 'Complete!';

        if (response.ok) {
            resultFileName = data.result_file;
            renderBatchResults(data, resultsArea);
            showToast('Analysis complete! Results are ready.', 'success');

            // Show download button
            document.getElementById('downloadBtn').classList.remove('d-none');
        } else {
            resultsArea.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-circle-fill me-2"></i>
                    <strong>Error:</strong> ${data.error || 'Failed to process file.'}
                </div>
            `;
            showToast('Error processing file.', 'error');
        }

    } catch (err) {
        progressBar.style.width = '0%';
        resultsArea.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-circle-fill me-2"></i>
                <strong>Network Error:</strong> ${err.message}
            </div>
        `;
        showToast('Network error occurred.', 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="bi bi-shield-fill-check"></i> Analyze Network Traffic';
        setTimeout(() => { progressContainer.classList.add('d-none'); }, 2000);
    }
}

// ─── Render Batch Results ───────────────────────────
function renderBatchResults(data, container) {
    const summary = data.summary;
    const results = data.results || [];

    const attackPct = summary.attack_percentage || 0;
    const threatLevel = attackPct > 50 ? 'Critical' : attackPct > 20 ? 'High' : attackPct > 5 ? 'Medium' : 'Low';
    const threatColor = attackPct > 50 ? '#ff1744' : attackPct > 20 ? '#ff9100' : attackPct > 5 ? '#ffea00' : '#00e676';

    container.innerHTML = `
        <!-- Summary Cards -->
        <div class="row g-3 mb-4">
            <div class="col-6">
                <div class="text-center p-3" style="background: rgba(0,0,0,0.2); border-radius: 12px;">
                    <h2 class="mb-0" style="color: #00e5ff;">${summary.total}</h2>
                    <small class="text-muted">Total Records</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center p-3" style="background: rgba(0,0,0,0.2); border-radius: 12px;">
                    <h2 class="mb-0" style="color: ${threatColor};">${threatLevel}</h2>
                    <small class="text-muted">Threat Level</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center p-3" style="background: rgba(0, 230, 118, 0.08); border-radius: 12px; border: 1px solid rgba(0,230,118,0.2);">
                    <h2 class="mb-0 text-success">${summary.normal}</h2>
                    <small class="text-muted">Normal (${summary.normal_percentage}%)</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center p-3" style="background: rgba(255, 23, 68, 0.08); border-radius: 12px; border: 1px solid rgba(255,23,68,0.2);">
                    <h2 class="mb-0 text-danger">${summary.attacks}</h2>
                    <small class="text-muted">Attacks (${summary.attack_percentage}%)</small>
                </div>
            </div>
        </div>

        <!-- Distribution Bar -->
        <div class="mb-4">
            <div class="d-flex justify-content-between mb-2">
                <small class="text-success">Normal: ${summary.normal_percentage}%</small>
                <small class="text-danger">Attack: ${summary.attack_percentage}%</small>
            </div>
            <div class="progress cyber-progress" style="height: 12px;">
                <div class="progress-bar bg-success" style="width: ${summary.normal_percentage}%"></div>
                <div class="progress-bar bg-danger" style="width: ${summary.attack_percentage}%"></div>
            </div>
        </div>

        <!-- Results Table (first 50) -->
        <h6 class="mb-3"><i class="bi bi-table text-info"></i> Prediction Details (showing ${Math.min(results.length, 50)} of ${data.total_results})</h6>
        <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
            <table class="table cyber-table table-sm">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Prediction</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.slice(0, 50).map(r => `
                        <tr>
                            <td>${r.index + 1}</td>
                            <td>
                                ${r.prediction === 1
                                    ? '<span class="badge bg-danger"><i class="bi bi-exclamation-triangle-fill"></i> Attack</span>'
                                    : '<span class="badge bg-success"><i class="bi bi-check-circle-fill"></i> Normal</span>'
                                }
                            </td>
                            <td>${r.confidence ? r.confidence + '%' : '--'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>

        ${data.total_results > 50 ? `<p class="text-muted text-center mt-2"><small>Showing first 50 results. Download CSV for complete results.</small></p>` : ''}
    `;

    // Add chart
    const chartContainer = document.createElement('div');
    chartContainer.className = 'mt-4';
    chartContainer.innerHTML = '<canvas id="batchResultChart" height="200"></canvas>';
    container.appendChild(chartContainer);

    new Chart(document.getElementById('batchResultChart'), {
        type: 'doughnut',
        data: {
            labels: ['Normal', 'Attack'],
            datasets: [{
                data: [summary.normal, summary.attacks],
                backgroundColor: ['rgba(0, 230, 118, 0.8)', 'rgba(255, 23, 68, 0.8)'],
                borderColor: ['#00e676', '#ff1744'],
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 16, usePointStyle: true }
                }
            }
        }
    });
}

// ─── Download Results ───────────────────────────────
function downloadResults() {
    if (!resultFileName) {
        showToast('No results to download.', 'error');
        return;
    }
    window.location.href = `/api/download/${resultFileName}`;
}
