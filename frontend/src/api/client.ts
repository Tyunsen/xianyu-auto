/**
 * API 客户端
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface ApiResponse<T> {
  items: T[]
  total: number
}

interface Account {
  id: number
  nickname: string
  status: string
  last_login: string | null
  created_at: string
  updated_at: string | null
}

interface AccountCreate {
  nickname: string
}

interface AccountUpdate {
  nickname?: string
  status?: string
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `请求失败: ${response.status}`)
    }

    return response.json()
  }

  // 账号 API
  async getAccounts(params?: {
    skip?: number
    limit?: number
  }): Promise<ApiResponse<Account>> {
    const query = new URLSearchParams()
    if (params?.skip) query.set('skip', String(params.skip))
    if (params?.limit) query.set('limit', String(params.limit))
    return this.request(`/api/accounts?${query}`)
  }

  async getAccount(id: number): Promise<Account> {
    return this.request(`/api/accounts/${id}`)
  }

  async createAccount(data: AccountCreate): Promise<Account> {
    return this.request('/api/accounts', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateAccount(id: number, data: AccountUpdate): Promise<Account> {
    return this.request(`/api/accounts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteAccount(id: number): Promise<void> {
    await this.request(`/api/accounts/${id}`, {
      method: 'DELETE',
    })
  }

  async refreshCookies(id: number, cookies: string): Promise<void> {
    await this.request(`/api/accounts/${id}/refresh-cookies`, {
      method: 'POST',
      body: JSON.stringify(cookies),
    })
  }

  async checkAccountStatus(id: number): Promise<{ status: string }> {
    return this.request(`/api/accounts/${id}/status`)
  }
}

export const api = new ApiClient(API_BASE_URL)
export type { Account, AccountCreate, AccountUpdate, ApiResponse }
