// API Response Types

export interface APIResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
}

export interface ErrorResponse {
  success: boolean;
  error: string;
  message?: string;
  field?: string;
  details?: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}

// User Types
export interface User {
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
}

export type UserRole = "admin" | "vendor" | "customer" | "guest";
export type UserStatus = "active" | "inactive" | "suspended" | "pending";

// Product Types
export interface Product {
  id: number;
  uuid: string;
  name: string;
  slug: string;
  description?: string;
  short_description?: string;
  base_price: number;
  sale_price?: number;
  cost_price?: number;
  sku?: string;
  quantity: number;
  low_stock_threshold: number;
  track_inventory: boolean;
  allow_backorders: boolean;
  status: ProductStatus;
  category_id?: number;
  vendor_id?: number;
  featured_image?: string;
  image_gallery: string[];
  weight?: number;
  dimensions: Record<string, unknown>;
  attributes: Record<string, unknown>;
  is_shippable: boolean;
  shipping_class?: string;
  tax_class: string;
  tax_rate: number;
  is_featured: boolean;
  is_visible: boolean;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

export type ProductStatus = "draft" | "published" | "archived" | "out_of_stock";

// Category Types
export interface Category {
  id: number;
  uuid: string;
  name: string;
  slug: string;
  description?: string;
  parent_id?: number;
  meta_title?: string;
  meta_description?: string;
  icon?: string;
  color?: string;
  image?: string;
  is_featured: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

// Order Types
export interface Order {
  id: number;
  uuid: string;
  order_number: string;
  status: OrderStatus;
  customer_id: number;
  vendor_id?: number;
  shipping_first_name: string;
  shipping_last_name: string;
  shipping_email: string;
  shipping_phone?: string;
  shipping_address_line_1: string;
  shipping_address_line_2?: string;
  shipping_city: string;
  shipping_state?: string;
  shipping_postal_code: string;
  shipping_country: string;
  billing_first_name?: string;
  billing_last_name?: string;
  billing_email?: string;
  billing_phone?: string;
  billing_address_line_1?: string;
  billing_address_line_2?: string;
  billing_city?: string;
  billing_state?: string;
  billing_postal_code?: string;
  billing_country?: string;
  payment_status: PaymentStatus;
  payment_method?: string;
  payment_gateway?: string;
  transaction_id?: string;
  subtotal: number;
  tax: number;
  shipping_cost: number;
  discount: number;
  total: number;
  currency: string;
  customer_notes?: string;
  admin_notes?: string;
  tracking_number?: string;
  tracking_url?: string;
  paid_at?: string;
  shipped_at?: string;
  delivered_at?: string;
  cancelled_at?: string;
  created_at: string;
  updated_at: string;
}

export type OrderStatus = "pending" | "confirmed" | "processing" | "shipped" | "delivered" | "cancelled" | "refunded";
export type PaymentStatus = "pending" | "paid" | "failed" | "refunded";

// Order Item Types
export interface OrderItem {
  id: number;
  uuid: string;
  order_id: number;
  product_id?: number;
  product_name: string;
  product_sku?: string;
  product_slug?: string;
  unit_price: number;
  quantity: number;
  tax: number;
  discount: number;
  subtotal: number;
  total: number;
  product_attributes: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// Review Types
export interface Review {
  id: number;
  uuid: string;
  user_id: number;
  product_id: number;
  rating: number;
  title?: string;
  comment?: string;
  is_approved: boolean;
  is_recommended: boolean;
  images: string[];
  videos: string[];
  helpful_count: number;
  unhelpful_count: number;
  created_at: string;
  updated_at: string;
}

// Cart Types
export interface Cart {
  id: number;
  uuid: string;
  user_id: number;
  currency: string;
  created_at: string;
  updated_at: string;
}

export interface CartItem {
  id: number;
  uuid: string;
  cart_id: number;
  product_id: number;
  quantity: number;
  attributes: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// Health Check Types
export interface HealthCheckResponse {
  status: string;
  version: string;
  debug: boolean;
}
