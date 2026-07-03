/**
 * CyberShield AI - Main JavaScript
 * Core functionality: sidebar, time, status checks
 */

// ─── Sidebar Toggle ─────────────────────────────────
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('show');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggleBtns = document.querySelectorAll('.sidebar-toggle, .sidebar-toggle-btn');

    if (!sidebar || !sidebar.classList.contains('show')) return;

    let clickedToggle = false;
    toggleBtns.forEach(btn => {
        if (btn.contains(e.target)) clickedToggle = true;
    });

    if (!sidebar.contains(e.target) && !clickedToggle) {
        sidebar.classList.remove('show');
    }
});

// ─── Live Time ──────────────────────────────────────
function updateLiveTime() {
    const el = document.getElementById('liveTime');
    if (!el) return;

    const now = new Date();
    const options = {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: true
    };
    el.textContent = now.toLocaleString('en-US', options);
}

setInterval(updateLiveTime, 1000);
updateLiveTime();

// ─── System Status Check ────────────────────────────
async function checkSystemStatus() {
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    if (!dot || !text) return;

    try {
        const res = await fetch('/api/health');
        const data = await res.json();

        if (data.model_loaded) {
            dot.style.background = '#00e676';
            text.textContent = 'System Active';
        } else {
            dot.style.background = '#ff9100';
            text.textContent = 'Model Not Trained';
        }
    } catch (e) {
        dot.style.background = '#ff1744';
        text.textContent = 'System Error';
    }
}

// Check status on page load and every 30 seconds
document.addEventListener('DOMContentLoaded', function() {
    checkSystemStatus();
    setInterval(checkSystemStatus, 30000);
});

// ─── Utility Functions ──────────────────────────────
function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle-fill' : type === 'error' ? 'exclamation-circle-fill' : 'info-circle-fill'}"></i>
        <span>${message}</span>
    `;
    toast.style.cssText = `
        position: fixed; bottom: 24px; right: 24px; z-index: 9999;
        padding: 14px 24px; border-radius: 10px;
        display: flex; align-items: center; gap: 10px;
        font-size: 0.9rem; font-weight: 500;
        animation: slideInRight 0.3s ease;
        background: ${type === 'success' ? 'rgba(0,230,118,0.15)' : type === 'error' ? 'rgba(255,23,68,0.15)' : 'rgba(0,229,255,0.15)'};
        border: 1px solid ${type === 'success' ? 'rgba(0,230,118,0.3)' : type === 'error' ? 'rgba(255,23,68,0.3)' : 'rgba(0,229,255,0.3)'};
        color: ${type === 'success' ? '#00e676' : type === 'error' ? '#ff1744' : '#00e5ff'};
        backdrop-filter: blur(12px);
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS for toast animation
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100px); }
        to { opacity: 1; transform: translateX(0); }
    }
`;
document.head.appendChild(toastStyle);
