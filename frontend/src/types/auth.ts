// Authentication Types

export interface UserRegister {
  email: string;
  username?: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  company_name?: string;
  company_vat?: string;
  address_line_1?: string;
  address_line_2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  language?: string;
  currency?: string;
  role?: UserRole;
}

export interface UserLogin {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  refresh_expires_in: number;
}

export interface TokenRefresh {
  refresh_token: string;
}

export interface ForgotPassword {
  email: string;
}

export interface ResetPassword {
  email: string;
  token: string;
  password: string;
  password_confirmation: string;
}

export interface ChangePassword {
  current_password: string;
  new_password: string;
  new_password_confirmation: string;
}

export interface UserResponse {
  id: number;
  uuid: string;
  email: string;
  username?: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  role: UserRole;
  status: UserStatus;
  company_name?: string;
  company_vat?: string;
  address_line_1?: string;
  address_line_2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  language?: string;
  currency?: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
  email_verified_at?: string;
  access_token?: string;
  refresh_token?: string;
}

// Re-export UserRole and UserStatus from api types
type UserRole = "admin" | "vendor" | "customer" | "guest";
type UserStatus = "active" | "inactive" | "suspended" | "pending";

export type { UserRole, UserStatus };
