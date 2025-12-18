/**
 * Edu2Job Shared Utilities
 */

const Utils = {
    /**
     * Show a toast notification
     */
    showToast: function (message, type = 'info', title = '') {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.style.cssText = 'position: fixed; top: 1.5rem; right: 1.5rem; z-index: 2000;';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        const colors = {
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6'
        };

        const icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };

        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'polite');
        toast.style.cssText = `
            background: white;
            border-left: 4px solid ${colors[type] || colors.info};
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            min-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;

        const displayTitle = title || type.charAt(0).toUpperCase() + type.slice(1);

        toast.innerHTML = `
            <div style="font-size: 1.25rem;">${icons[type] || icons.info}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1e293b;">${displayTitle}</div>
                <div style="color: #64748b; font-size: 0.875rem;">${message}</div>
            </div>
        `;

        container.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    },

    /**
     * Check if user is authenticated
     */
    checkAuth: async function (redirectToLogin = true) {
        const token = localStorage.getItem('authToken');
        if (!token) {
            if (redirectToLogin) window.location.href = 'login.html';
            return false;
        }

        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/verify-token`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (!data.valid) {
                localStorage.removeItem('authToken');
                localStorage.removeItem('userInfo');
                if (redirectToLogin) window.location.href = 'login.html';
                return false;
            }
            return true;
        } catch (error) {
            console.error('Auth verification failed:', error);
            return false;
        }
    },

    /**
     * Logout user
     */
    logout: function () {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        window.location.href = 'login.html';
    },

    /**
     * Initialize shared styles (like toast animations)
     */
    init: function () {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
};

// Initialize on load
Utils.init();
window.Utils = Utils;
