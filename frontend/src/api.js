const API_BASE_URL = 'http://127.0.0.1:8000' 

const apiClient = {
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const username = sessionStorage.getItem('username')
    const password = sessionStorage.getItem('password')
    const headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${username}:${password}`)
    })
    const response = await fetch(`${API_BASE_URL}${endpoint}?${queryString}`, {
      headers: headers,
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    return response.json()
  },

  async getAll() {
    return this.get('/all_properties/')
  }
}

export default apiClient