function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('visible');
    }, 50);

    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4200);
}

window.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.flash-message');
    alerts.forEach((element) => {
        showToast(element.textContent.trim(), element.dataset.category || 'info');
    });
});
