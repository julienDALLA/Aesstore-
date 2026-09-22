// API Service Configuration

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from "axios";
import { APIResponse, ErrorResponse } from "@/types";

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_VERSION = "/api/v1";

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add authorization token if available
    const token = localStorage.getItem("access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ErrorResponse>) => {
    if (error.response) {
      const { status } = error.response;

      // Handle token expiration
      if (status === 401) {
        // Try to refresh token
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          try {
            const response = await axios.post(
              `${API_BASE_URL}${API_VERSION}/auth/refresh`,
              { refresh_token: refreshToken }
            );
            
            const { access_token, refresh_token } = response.data.data;
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("refresh_token", refresh_token);

            // Retry original request
            if (error.config) {
              error.config.headers.Authorization = `Bearer ${access_token}`;
              return axios.request(error.config);
            }
          } catch (refreshError) {
            // Refresh failed, logout user
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("user");
            window.location.href = "/auth/login";
          }
        } else {
          // No refresh token, logout user
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");
          window.location.href = "/auth/login";
        }
      }

      // Handle other errors
      return Promise.reject(error);
    }

    // Network error
    return Promise.reject(error);
  }
);

// Helper function to handle API responses
export const handleAPIResponse = <T>(
  response: APIResponse<T>
): T => {
  if (!response.success) {
    throw new Error(response.message || "Request failed");
  }
  return response.data as T;
};

// Helper function to handle API errors
export const handleAPIError = (error: AxiosError<ErrorResponse>): Error => {
  if (error.response) {
    const { data } = error.response;
    if (data) {
      return new Error(
        data.message || data.error || "An error occurred"
      );
    }
  }
  return new Error(error.message || "Network error");
};

// Export API instance
export default api;

// Export API endpoints
export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    REGISTER: "/auth/register",
    LOGIN: "/auth/login",
    LOGOUT: "/auth/logout",
    REFRESH: "/auth/refresh",
    FORGOT_PASSWORD: "/auth/forgot-password",
    RESET_PASSWORD: "/auth/reset-password",
    CHANGE_PASSWORD: "/auth/change-password",
    ME: "/auth/me",
  },
  // Users
  USERS: {
    LIST: "/users",
    DETAIL: (id: number | string) => `/users/${id}`,
    CREATE: "/users",
    UPDATE: (id: number | string) => `/users/${id}`,
    DELETE: (id: number | string) => `/users/${id}`,
  },
  // Products
  PRODUCTS: {
    LIST: "/products",
    DETAIL: (slug: string) => `/products/${slug}`,
    CREATE: "/products",
    UPDATE: (id: number | string) => `/products/${id}`,
    DELETE: (id: number | string) => `/products/${id}`,
    SEARCH: "/products/search",
    FEATURED: "/products/featured",
    CATEGORIES: (categorySlug: string) => `/products/category/${categorySlug}`,
  },
  // Categories
  CATEGORIES: {
    LIST: "/categories",
    DETAIL: (slug: string) => `/categories/${slug}`,
    CREATE: "/categories",
    UPDATE: (id: number | string) => `/categories/${id}`,
    DELETE: (id: number | string) => `/categories/${id}`,
    TREE: "/categories/tree",
  },
  // Orders
  ORDERS: {
    LIST: "/orders",
    DETAIL: (orderNumber: string) => `/orders/${orderNumber}`,
    CREATE: "/orders",
    UPDATE: (id: number | string) => `/orders/${id}`,
    MY_ORDERS: "/orders/my",
    VENDOR_ORDERS: "/orders/vendor",
  },
  // Cart
  CART: {
    GET: "/cart",
    ADD: "/cart/items",
    UPDATE: (id: number | string) => `/cart/items/${id}`,
    DELETE: (id: number | string) => `/cart/items/${id}`,
    CLEAR: "/cart/clear",
    CHECKOUT: "/cart/checkout",
  },
  // Reviews
  REVIEWS: {
    LIST: (productSlug: string) => `/reviews/product/${productSlug}`,
    CREATE: "/reviews",
    UPDATE: (id: number | string) => `/reviews/${id}`,
    DELETE: (id: number | string) => `/reviews/${id}`,
    MY_REVIEWS: "/reviews/my",
  },
  // Health
  HEALTH: {
    CHECK: "/health",
    READY: "/health/ready",
    LIVE: "/health/live",
  },
};
