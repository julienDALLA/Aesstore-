// Authentication Service

import api, { API_ENDPOINTS, handleAPIResponse, handleAPIError } from "./api";
import {
  UserRegister,
  UserLogin,
  UserResponse,
  Token,
  TokenRefresh,
  ForgotPassword,
  ResetPassword,
  ChangePassword,
} from "@/types";
import { APIResponse } from "@/types/api";

// Auth Service Class
export class AuthService {
  // Register a new user
  static async register(data: UserRegister): Promise<UserResponse> {
    try {
      const response = await api.post<APIResponse<UserResponse>>(
        API_ENDPOINTS.AUTH.REGISTER,
        data
      );
      return handleAPIResponse<UserResponse>(response.data);
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Login user
  static async login(data: UserLogin): Promise<UserResponse> {
    try {
      const response = await api.post<APIResponse<UserResponse>>(
        API_ENDPOINTS.AUTH.LOGIN,
        data
      );
      const userResponse = handleAPIResponse<UserResponse>(response.data);
      
      // Store tokens and user data
      if (userResponse.access_token) {
        localStorage.setItem("access_token", userResponse.access_token);
      }
      if (userResponse.refresh_token) {
        localStorage.setItem("refresh_token", userResponse.refresh_token);
      }
      
      // Remove tokens from response before returning
      const { access_token, refresh_token, ...userData } = userResponse;
      localStorage.setItem("user", JSON.stringify(userData));
      
      return userResponse;
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Logout user
  static async logout(): Promise<void> {
    try {
      await api.post(API_ENDPOINTS.AUTH.LOGOUT);
    } catch (error) {
      // Ignore error, still clear local storage
    } finally {
      // Clear local storage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    }
  }

  // Refresh token
  static async refreshToken(data: TokenRefresh): Promise<Token> {
    try {
      const response = await api.post<APIResponse<Token>>(
        API_ENDPOINTS.AUTH.REFRESH,
        data
      );
      const token = handleAPIResponse<Token>(response.data);
      
      // Store new tokens
      localStorage.setItem("access_token", token.access_token);
      localStorage.setItem("refresh_token", token.refresh_token);
      
      return token;
    } catch (error) {
      // Clear local storage on refresh failure
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      throw handleAPIError(error as any);
    }
  }

  // Get current user
  static async getCurrentUser(): Promise<UserResponse> {
    try {
      const response = await api.get<APIResponse<UserResponse>>(
        API_ENDPOINTS.AUTH.ME
      );
      const userResponse = handleAPIResponse<UserResponse>(response.data);
      
      // Store user data
      const { access_token, refresh_token, ...userData } = userResponse;
      localStorage.setItem("user", JSON.stringify(userData));
      
      return userResponse;
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Forgot password
  static async forgotPassword(data: ForgotPassword): Promise<void> {
    try {
      await api.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, data);
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Reset password
  static async resetPassword(data: ResetPassword): Promise<void> {
    try {
      await api.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, data);
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Change password
  static async changePassword(data: ChangePassword): Promise<void> {
    try {
      await api.post(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, data);
    } catch (error) {
      throw handleAPIError(error as any);
    }
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    const token = localStorage.getItem("access_token");
    return !!token;
  }

  // Get stored user
  static getStoredUser(): UserResponse | null {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        return JSON.parse(user) as UserResponse;
      } catch {
        return null;
      }
    }
    return null;
  }

  // Get access token
  static getAccessToken(): string | null {
    return localStorage.getItem("access_token");
  }

  // Get refresh token
  static getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token");
  }

  // Clear auth state
  static clearAuthState(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  }
}

// Export singleton instance
export const authService = new AuthService();

export default AuthService;
