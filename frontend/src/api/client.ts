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

interface Product {
  id: number
  title: string
  price: string
  description: string | null
  images: string | null
  status: string
  xianyu_id: string | null
  account_id: number | null
  created_at: string
  updated_at: string | null
}

interface ProductCreate {
  title: string
  price: string
  description?: string
  images?: string
  account_id?: number
}

interface ProductUpdate {
  title?: string
  price?: string
  description?: string
  images?: string
  status?: string
  account_id?: number
}

interface CardKey {
  id: number
  key: string
  product_id: number
  status: string
  used_at: string | null
  used_order_id: number | null
  created_at: string
}

interface CardKeyCreate {
  key: string
  product_id: number
}

interface CardKeyStats {
  total: number
  available: number
  used: number
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

  // 商品 API
  async getProducts(params?: {
    skip?: number
    limit?: number
    status?: string
    search?: string
  }): Promise<ApiResponse<Product>> {
    const query = new URLSearchParams()
    if (params?.skip) query.set('skip', String(params.skip))
    if (params?.limit) query.set('limit', String(params.limit))
    if (params?.status) query.set('status', params.status)
    if (params?.search) query.set('search', params.search)
    return this.request(`/api/products?${query}`)
  }

  async getProduct(id: number): Promise<Product> {
    return this.request(`/api/products/${id}`)
  }

  async createProduct(data: ProductCreate): Promise<Product> {
    return this.request('/api/products', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateProduct(id: number, data: ProductUpdate): Promise<Product> {
    return this.request(`/api/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteProduct(id: number): Promise<void> {
    await this.request(`/api/products/${id}`, {
      method: 'DELETE',
    })
  }

  async publishProduct(id: number): Promise<void> {
    await this.request(`/api/products/${id}/publish`, {
      method: 'POST',
    })
  }

  async unpublishProduct(id: number): Promise<void> {
    await this.request(`/api/products/${id}/unpublish`, {
      method: 'POST',
    })
  }

  // 卡密 API
  async getCardKeys(params?: {
    skip?: number
    limit?: number
    product_id?: number
    status?: string
  }): Promise<ApiResponse<CardKey>> {
    const query = new URLSearchParams()
    if (params?.skip) query.set('skip', String(params.skip))
    if (params?.limit) query.set('limit', String(params.limit))
    if (params?.product_id) query.set('product_id', String(params.product_id))
    if (params?.status) query.set('status', params.status)
    return this.request(`/api/card-keys?${query}`)
  }

  async createCardKey(data: CardKeyCreate): Promise<CardKey> {
    return this.request('/api/card-keys', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async deleteCardKey(id: number): Promise<void> {
    await this.request(`/api/card-keys/${id}`, {
      method: 'DELETE',
    })
  }

  async getCardKeyStats(productId?: number): Promise<CardKeyStats> {
    const query = productId ? `?product_id=${productId}` : ''
    return this.request(`/api/card-keys/stats${query}`)
  }

  async importCardKeys(file: File, productId: number): Promise<{ imported: number; failed: number }> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('product_id', String(productId))

    const response = await fetch(`${this.baseUrl}/api/card-keys/import?product_id=${productId}`, {
      method: 'POST',
      body: file,
    })

    if (!response.ok) {
      throw new Error('导入失败')
    }

    return response.json()
  }
}

export const api = new ApiClient(API_BASE_URL)
export type {
  Account, AccountCreate, AccountUpdate,
  Product, ProductCreate, ProductUpdate,
  CardKey, CardKeyCreate, CardKeyStats,
  ApiResponse
}
