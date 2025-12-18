(function (global) {
  const BASE_URL = 'https://api.example.com';

  async function request(path, options = {}) {
    const url = `${BASE_URL}${path}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const contentType = response.headers.get('content-type') || '';
      const data = contentType.includes('application/json') ? await response.json() : await response.text();

      if (!response.ok) {
        const error = new Error(data?.message || 'İstək zamanı xəta baş verdi');
        error.status = response.status;
        error.payload = data;
        throw error;
      }

      return data;
    } catch (error) {
      console.error('API error', error);
      throw error;
    }
  }

  global.API = { BASE_URL, request };
})(window);
