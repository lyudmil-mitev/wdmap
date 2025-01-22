const API_BASE_URL = 'http://127.0.0.1:8000' 

const apiClient = {
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_BASE_URL}${endpoint}?${queryString}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    return response.json()
  },

  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    return response.json()
  },

}

export default apiClient