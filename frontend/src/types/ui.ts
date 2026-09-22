// UI Component Types

import { ReactNode } from "react";

// Table Types
export interface ColumnDef<T> {
  accessorKey: string;
  header: string;
  cell?: (info: CellContext<T, unknown>) => ReactNode;
  enableSorting?: boolean;
  enableHiding?: boolean;
  meta?: Record<string, unknown>;
}

export interface CellContext<T, TValue> {
  getValue: () => TValue;
  row: Row<T>;
  column: Column<T, TValue>;
  table: Table<T>;
}

export interface Row<T> {
  original: T;
  id: string;
  index: number;
  getValue: (accessorKey: string) => unknown;
}

export interface Column<T, TValue> {
  id: string;
  accessorKey: string;
  header: string;
}

export interface Table<T> {
  getCoreRowModel: () => RowModel<T>;
  getSortedRowModel: () => RowModel<T>;
  getFilteredRowModel: () => RowModel<T>;
  getPaginationRowModel: () => RowModel<T>;
  getRowCanExpand: (row: Row<T>) => boolean;
  getExpandedRowModel: () => RowModel<T>;
  toggleAllRowsExpanded: (expanded: boolean) => void;
  getRowId: (row: Row<T>) => string;
  getState: () => TableState<T>;
  setState: (state: Partial<TableState<T>>) => void;
  previousPage: () => void;
  nextPage: () => void;
  setPageSize: (size: number) => void;
  setPageIndex: (index: number) => void;
  getCanPreviousPage: () => boolean;
  getCanNextPage: () => boolean;
  getPageCount: () => number;
}

export interface RowModel<T> {
  rows: Row<T>[];
  flatRows: Row<T>[];
}

export interface TableState<T> {
  sorting: SortingState;
  columnFilters: ColumnFiltersState;
  pagination: PaginationState;
  expanded: Record<string, boolean>;
  rowSelection: Record<string, boolean>;
  columnVisibility: Record<string, boolean>;
}

export interface SortingState {
  id: string;
  desc: boolean;
}

export interface ColumnFiltersState {
  id: string;
  value: unknown;
}

export interface PaginationState {
  pageIndex: number;
  pageSize: number;
}

// Form Types
export interface FormField {
  name: string;
  label: string;
  type: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  options?: Option[];
  validation?: Record<string, unknown>;
}

export interface Option {
  value: string;
  label: string;
}

// Select Types
export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

// Toast Types
export interface ToastProps {
  id?: string;
  title?: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  promise?: Promise<unknown>;
  dismissible?: boolean;
  duration?: number;
}

// Dialog Types
export interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title?: string;
  description?: string;
  children: ReactNode;
}

// Button Types
export interface ButtonProps {
  variant?: "primary" | "secondary" | "destructive" | "outline" | "ghost" | "link";
  size?: "sm" | "md" | "lg";
  asChild?: boolean;
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
}

// Input Types
export interface InputProps {
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  readOnly?: boolean;
  required?: boolean;
  error?: string;
  label?: string;
  helperText?: string;
  className?: string;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

// Card Types
export interface CardProps {
  title?: string;
  description?: string;
  actions?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
  className?: string;
}

// Badge Types
export interface BadgeProps {
  variant?: "primary" | "secondary" | "destructive" | "outline";
  children: ReactNode;
  className?: string;
}

// Table Types
export interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  pageSize?: number;
  onRowClick?: (row: T) => void;
  selectedRows?: T[];
  onSelectionChange?: (rows: T[]) => void;
}

// Chart Types
export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
}

// Sidebar Types
export interface SidebarItem {
  title: string;
  url: string;
  icon: ReactNode;
  badge?: string | number;
  children?: SidebarItem[];
}

// Breadcrumb Types
export interface BreadcrumbItem {
  label: string;
  href?: string;
}

// Pagination Types
export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  showPageNumbers?: boolean;
  showPageSizeSelector?: boolean;
  pageSize?: number;
  onPageSizeChange?: (size: number) => void;
}

// Filter Types
export interface FilterItem {
  key: string;
  label: string;
  type: "select" | "date" | "range" | "search";
  options?: SelectOption[];
  placeholder?: string;
}

// Export Types
export type {
  ColumnDef,
  CellContext,
  Row,
  Column,
  Table,
  RowModel,
  TableState,
  SortingState,
  ColumnFiltersState,
  PaginationState,
  FormField,
  Option,
  SelectOption,
  ToastProps,
  DialogProps,
  ButtonProps,
  InputProps,
  CardProps,
  BadgeProps,
  DataTableProps,
  ChartData,
  ChartDataset,
  SidebarItem,
  BreadcrumbItem,
  PaginationProps,
  FilterItem,
};
