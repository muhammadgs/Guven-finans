(function (global) {
  const TOKEN_KEY = 'access_token';

  function saveToken(token) {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    }
  }

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  }

  async function login(credentials) {
    const response = await API.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    if (response?.access_token) {
      saveToken(response.access_token);
    }
    return response;
  }

  async function logout() {
    const token = getToken();
    if (!token) return;
    try {
      await API.request('/auth/logout', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
    } catch (error) {
      console.warn('Logout error ignored', error);
    }
    clearToken();
  }

  async function getMe() {
    const token = getToken();
    if (!token) {
      throw new Error('Token yoxdur');
    }
    return API.request('/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  global.Auth = { login, logout, getMe, getToken, saveToken, clearToken };
})(window);
