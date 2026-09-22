// Application constants

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  VERSION: "/api/v1",
  TIMEOUT: 30000,
} as const;

// App Configuration
export const APP_CONFIG = {
  NAME: process.env.NEXT_PUBLIC_APP_NAME || "Aesstore",
  VERSION: process.env.NEXT_PUBLIC_APP_VERSION || "1.0.0",
  DESCRIPTION: "Modern B2B e-commerce platform",
} as const;

// Theme Configuration
export const THEME_CONFIG = {
  PRIMARY_COLOR: "#3b82f6",
  SECONDARY_COLOR: "#6b7280",
  SUCCESS_COLOR: "#10b981",
  WARNING_COLOR: "#f59e0b",
  ERROR_COLOR: "#ef4444",
} as const;

// Pagination Configuration
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100,
} as const;

// Table Configuration
export const TABLE_CONFIG = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 20, 50, 100],
} as const;

// Form Configuration
export const FORM_CONFIG = {
  DEBOUNCE_TIME: 300,
  VALIDATION_DELAY: 500,
} as const;

// Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
  USER: "user",
  THEME: "theme",
  LANGUAGE: "language",
  CURRENCY: "currency",
} as const;

// Local Storage Keys
export const LOCAL_STORAGE = {
  ...STORAGE_KEYS,
  CART: "cart",
  RECENT_PRODUCTS: "recent_products",
  FAVORITES: "favorites",
} as const;

// Session Storage Keys
export const SESSION_STORAGE = {
  LAST_PATH: "last_path",
  REDIRECT_URL: "redirect_url",
} as const;

// Date Formats
export const DATE_FORMATS = {
  SHORT: "MMM d, yyyy",
  LONG: "MMMM d, yyyy",
  FULL: "EEEE, MMMM d, yyyy",
  TIME: "h:mm a",
  DATETIME: "MMM d, yyyy h:mm a",
  ISO: "yyyy-MM-dd",
} as const;

// Number Formats
export const NUMBER_FORMATS = {
  CURRENCY: {
    USD: { style: "currency", currency: "USD" },
    EUR: { style: "currency", currency: "EUR" },
    GBP: { style: "currency", currency: "GBP" },
  },
  PERCENT: { style: "percent", minimumFractionDigits: 1, maximumFractionDigits: 2 },
  DECIMAL: { minimumFractionDigits: 2, maximumFractionDigits: 2 },
} as const;

// Validation Rules
export const VALIDATION_RULES = {
  EMAIL: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
  PHONE: /^\+?[1-9]\d{1,14}$/,
  USERNAME: /^[a-zA-Z0-9_-]{3,20}$/,
  VAT: /^[A-Z]{2,3}\d{4,12}$/,
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  REQUIRED: "This field is required",
  INVALID_EMAIL: "Please enter a valid email address",
  INVALID_PASSWORD: "Password must be at least 8 characters with uppercase, lowercase, number and special character",
  INVALID_PHONE: "Please enter a valid phone number",
  PASSWORDS_DONT_MATCH: "Passwords do not match",
  USER_NOT_FOUND: "User not found",
  INVALID_CREDENTIALS: "Invalid credentials",
  UNAUTHORIZED: "Unauthorized access",
  FORBIDDEN: "You do not have permission to perform this action",
  NOT_FOUND: "Resource not found",
  SERVER_ERROR: "An unexpected error occurred",
  NETWORK_ERROR: "Network error. Please check your connection.",
  VALIDATION_ERROR: "Please check the form for errors",
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: "Login successful",
  LOGOUT_SUCCESS: "Logout successful",
  REGISTER_SUCCESS: "Registration successful",
  UPDATE_SUCCESS: "Update successful",
  CREATE_SUCCESS: "Created successfully",
  DELETE_SUCCESS: "Deleted successfully",
  PASSWORD_CHANGED: "Password changed successfully",
  PASSWORD_RESET: "Password reset successfully",
  ORDER_PLACED: "Order placed successfully",
} as const;

// Regex Patterns
export const REGEX_PATTERNS = {
  EMAIL: VALIDATION_RULES.EMAIL,
  PASSWORD: VALIDATION_RULES.PASSWORD,
  PHONE: VALIDATION_RULES.PHONE,
  USERNAME: VALIDATION_RULES.USERNAME,
  VAT: VALIDATION_RULES.VAT,
  URL: /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/,
  UUID: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
} as const;

// File Types
export const FILE_TYPES = {
  IMAGE: ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"],
  DOCUMENT: ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
  VIDEO: ["video/mp4", "video/webm", "video/quicktime"],
  AUDIO: ["audio/mpeg", "audio/wav", "audio/ogg"],
} as const;

// File Size Limits
export const FILE_SIZE_LIMITS = {
  AVATAR: 5 * 1024 * 1024, // 5MB
  IMAGE: 10 * 1024 * 1024, // 10MB
  DOCUMENT: 25 * 1024 * 1024, // 25MB
  VIDEO: 100 * 1024 * 1024, // 100MB
} as const;

// Export all constants
export {
  API_CONFIG as API,
  APP_CONFIG as APP,
  THEME_CONFIG as THEME,
  PAGINATION_CONFIG as PAGINATION,
  TABLE_CONFIG as TABLE,
  FORM_CONFIG as FORM,
  STORAGE_KEYS as STORAGE,
  LOCAL_STORAGE,
  SESSION_STORAGE,
  DATE_FORMATS as DATE,
  NUMBER_FORMATS as NUMBER,
  VALIDATION_RULES as VALIDATION,
  ERROR_MESSAGES as ERRORS,
  SUCCESS_MESSAGES as SUCCESS,
  REGEX_PATTERNS as REGEX,
  FILE_TYPES,
  FILE_SIZE_LIMITS as FILE_SIZE,
};
