const API_BASE_URL = 'http://94.20.153.157:8011';
const API_VERSION = '/api/v1';

const AUTH_ENDPOINTS = {
    login: `${API_BASE_URL}${API_VERSION}/auth/login`,
    refresh: `${API_BASE_URL}${API_VERSION}/auth/refresh`,
    logout: `${API_BASE_URL}${API_VERSION}/auth/logout`,
    me: `${API_BASE_URL}${API_VERSION}/auth/me`,
};

const WORKER_ENDPOINTS = {
    verifyCompany: `${API_BASE_URL}${API_VERSION}/companies/verify`,
    register: `${API_BASE_URL}${API_VERSION}/workers/register`,
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

const initWorkerRegistration = () => {
    const form = document.querySelector('[data-worker-registration]');
    if (!form) return;

    const companyInput = form.querySelector('[data-company-code-input]');
    const verifyButton = form.querySelector('[data-company-verify-btn]');
    const fieldsWrapper = form.querySelector('[data-company-fields]');
    const companyStatus = form.querySelector('[data-company-status]');
    const submitButton = form.querySelector('[data-worker-submit]');
    const successRedirect = form.dataset.successRedirect;

    let companyVerified = false;

    const toggleFieldsVisibility = (visible) => {
        if (!fieldsWrapper) return;
        fieldsWrapper.classList.toggle('hidden', !visible);
        if (visible) {
            fieldsWrapper.classList.remove('opacity-0');
            fieldsWrapper.classList.add('opacity-100');
        } else {
            fieldsWrapper.classList.remove('opacity-100');
            fieldsWrapper.classList.add('opacity-0');
        }
    };

    const setCompanyStatus = (message, status = 'info') => {
        if (!companyStatus) return;
        const statusClasses = {
            success: 'border-green-200 bg-green-50 text-green-800',
            error: 'border-red-200 bg-red-50 text-red-800',
            info: 'border-blue-200 bg-blue-50 text-blue-800',
        };
        companyStatus.className = `rounded-xl border px-4 py-3 text-sm ${statusClasses[status] || statusClasses.info}`;
        companyStatus.textContent = message;
        companyStatus.classList.remove('hidden');
    };

    const resetFormState = () => {
        companyVerified = false;
        toggleFieldsVisibility(false);
        submitButton?.setAttribute('disabled', 'true');
    };

    const verifyCompanyCode = async () => {
        const code = companyInput?.value?.trim();
        if (!code) {
            setCompanyStatus('Zəhmət olmasa şirkət kodunu daxil edin.', 'error');
            resetFormState();
            return;
        }

        setCompanyStatus('Şirkət kodu yoxlanılır...', 'info');
        try {
            await apiRequest(`${WORKER_ENDPOINTS.verifyCompany}?code=${encodeURIComponent(code)}`, {
                method: 'GET',
            });
            companyVerified = true;
            toggleFieldsVisibility(true);
            submitButton?.removeAttribute('disabled');
            setCompanyStatus('Şirkət kodu təsdiqləndi. Qeydiyyat məlumatlarını doldurun.', 'success');
        } catch (error) {
            setCompanyStatus(error.message || 'Şirkət kodu tapılmadı.', 'error');
            resetFormState();
        }
    };

    verifyButton?.addEventListener('click', verifyCompanyCode);
    companyInput?.addEventListener('input', () => {
        companyStatus?.classList.add('hidden');
        resetFormState();
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!companyVerified) {
            setCompanyStatus('Zəhmət olmasa əvvəl şirkət kodunu təsdiqləyin.', 'error');
            return;
        }

        const formData = new FormData(form);
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');

        if (password !== confirmPassword) {
            updateStatus('Şifrələr uyğun gəlmir.', 'error');
            return;
        }

        const payload = {
            company_code: formData.get('company_code'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            father_name: formData.get('father_name'),
            fin_code: formData.get('fin_code'),
            phone_number: formData.get('phone_number'),
            email: formData.get('email'),
            password,
        };

        submitButton?.setAttribute('disabled', 'true');
        updateStatus('Qeydiyyat göndərilir...', 'info');

        try {
            await apiRequest(WORKER_ENDPOINTS.register, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            updateStatus('Qeydiyyat uğurla tamamlandı. Yönləndirilirsiniz...', 'success');
            const redirectUrl = successRedirect || '/accounts/login/';
            setTimeout(() => {
                window.location.href = redirectUrl;
            }, 800);
        } catch (error) {
            updateStatus(error.message || 'Qeydiyyat zamanı xəta baş verdi.', 'error');
            submitButton?.removeAttribute('disabled');
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
    initWorkerRegistration();
};

document.addEventListener('DOMContentLoaded', initAuthHandlers);
