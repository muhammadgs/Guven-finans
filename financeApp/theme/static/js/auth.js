const API_BASE_URL = 'http://94.20.153.157:8011';
const API_VERSION = '/api/v1';

const AUTH_ENDPOINTS = {
    login: `${API_BASE_URL}${API_VERSION}/auth/login`,
    refresh: `${API_BASE_URL}${API_VERSION}/auth/refresh`,
    logout: `${API_BASE_URL}${API_VERSION}/auth/logout`,
    me: `${API_BASE_URL}${API_VERSION}/auth/me`,
};

const STORAGE_KEYS = {
    access: 'gf_access_token',
    refresh: 'gf_refresh_token',
};

const getTokens = () => ({
    access: localStorage.getItem(STORAGE_KEYS.access),
    refresh: localStorage.getItem(STORAGE_KEYS.refresh),
});

const storeTokens = (access, refresh) => {
    if (access) {
        localStorage.setItem(STORAGE_KEYS.access, access);
    }
    if (refresh) {
        localStorage.setItem(STORAGE_KEYS.refresh, refresh);
    }
};

const clearTokens = () => {
    localStorage.removeItem(STORAGE_KEYS.access);
    localStorage.removeItem(STORAGE_KEYS.refresh);
};

const parseErrorMessage = (data, fallback = 'Xəta baş verdi.') => {
    if (!data) return fallback;
    if (typeof data === 'string') return data;
    if (Array.isArray(data) && data.length) return data[0];
    if (data.detail) return data.detail;
    if (data.message) return data.message;
    return fallback;
};

const updateStatus = (message, status = 'info') => {
    const statusBox = document.querySelector('[data-api-status]');
    if (!statusBox) return;

    const statusClasses = {
        success: 'bg-green-100 text-green-800 border border-green-200',
        error: 'bg-red-100 text-red-800 border border-red-200',
        info: 'bg-blue-50 text-blue-700 border border-blue-200',
    };

    statusBox.className = `mt-6 rounded-lg px-4 py-3 text-sm font-medium ${statusClasses[status] || statusClasses.info}`;
    statusBox.textContent = message;
    statusBox.classList.remove('hidden');
};

const apiRequest = async (url, options = {}) => {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        const message = parseErrorMessage(data);
        throw new Error(message);
    }

    return data;
};

const handleLogin = (form) => {
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const payload = {
            username: formData.get('username'),
            password: formData.get('password'),
        };

        updateStatus('Giriş sorğusu göndərilir...', 'info');

        try {
            const data = await apiRequest(AUTH_ENDPOINTS.login, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const accessToken = data.access || data.access_token || data.token;
            const refreshToken = data.refresh || data.refresh_token;
            storeTokens(accessToken, refreshToken);

            updateStatus('Giriş uğurla tamamlandı.', 'success');
        } catch (error) {
            updateStatus(error.message || 'Giriş zamanı xəta baş verdi.', 'error');
        }
    });
};

const handleLogout = (button) => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const { access, refresh } = getTokens();

        updateStatus('Çıxış sorğusu göndərilir...', 'info');

        try {
            await apiRequest(AUTH_ENDPOINTS.logout, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(access ? { Authorization: `Bearer ${access}` } : {}),
                },
                body: refresh ? JSON.stringify({ refresh }) : undefined,
            });

            updateStatus('Çıxış uğurla tamamlandı.', 'success');
        } catch (error) {
            updateStatus(error.message || 'Çıxış zamanı xəta baş verdi.', 'error');
        } finally {
            clearTokens();
        }
    });
};

const handleRefresh = (button) => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const { refresh } = getTokens();

        if (!refresh) {
            updateStatus('Yenilənəcək token tapılmadı.', 'error');
            return;
        }

        updateStatus('Token yenilənir...', 'info');

        try {
            const data = await apiRequest(AUTH_ENDPOINTS.refresh, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh }),
            });

            const accessToken = data.access || data.access_token || data.token;
            if (accessToken) {
                storeTokens(accessToken, refresh);
                updateStatus('Token uğurla yeniləndi.', 'success');
            } else {
                updateStatus('Yeni token əldə edilə bilmədi.', 'error');
            }
        } catch (error) {
            updateStatus(error.message || 'Token yenilənərkən xəta baş verdi.', 'error');
        }
    });
};

const handleMe = (button) => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const { access } = getTokens();

        if (!access) {
            updateStatus('İstifadəçi məlumatı üçün giriş tələb olunur.', 'error');
            return;
        }

        updateStatus('İstifadəçi məlumatı gətirilir...', 'info');

        try {
            const data = await apiRequest(AUTH_ENDPOINTS.me, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${access}`,
                },
            });

            const message = `Aktiv istifadəçi: ${data.username || data.email || 'məlumat əldə edildi'}.`;
            updateStatus(message, 'success');
        } catch (error) {
            updateStatus(error.message || 'İstifadəçi məlumatı alınmadı.', 'error');
        }
    });
};

const initAuthHandlers = () => {
    const loginForm = document.querySelector('[data-api-login-form]');
    const logoutButton = document.querySelector('[data-api-logout-btn]');
    const refreshButton = document.querySelector('[data-api-refresh-btn]');
    const meButton = document.querySelector('[data-api-me-btn]');

    if (loginForm) handleLogin(loginForm);
    if (logoutButton) handleLogout(logoutButton);
    if (refreshButton) handleRefresh(refreshButton);
    if (meButton) handleMe(meButton);
};

document.addEventListener('DOMContentLoaded', initAuthHandlers);
