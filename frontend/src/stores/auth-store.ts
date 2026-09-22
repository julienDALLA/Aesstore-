// Auth Store using Zustand

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { UserResponse } from "@/types";
import { AuthService } from "@/services/auth-service";

// Auth State Interface
interface AuthState {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (data: any) => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
  setUser: (user: UserResponse | null) => void;
}

// Initial State
const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

// Create Auth Store
export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      // Login action
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const userResponse = await AuthService.login({
            username: email,
            password,
          });
          
          const { access_token, refresh_token, ...userData } = userResponse;
          
          set({
            user: userData,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : "Login failed",
            user: null,
            isAuthenticated: false,
          });
          throw error;
        }
      },
      
      // Logout action
      logout: async () => {
        set({ isLoading: true });
        
        try {
          await AuthService.logout();
        } catch (error) {
          // Ignore error
        } finally {
          AuthService.clearAuthState();
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },
      
      // Register action
      register: async (data: any) => {
        set({ isLoading: true, error: null });
        
        try {
          const userResponse = await AuthService.register(data);
          const { access_token, refresh_token, ...userData } = userResponse;
          
          set({
            user: userData,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : "Registration failed",
          });
          throw error;
        }
      },
      
      // Check authentication state
      checkAuth: async () => {
        set({ isLoading: true });
        
        try {
          const user = AuthService.getStoredUser();
          
          if (user && AuthService.isAuthenticated()) {
            // Verify token by fetching current user
            try {
              const currentUser = await AuthService.getCurrentUser();
              const { access_token, refresh_token, ...userData } = currentUser;
              
              set({
                user: userData,
                isAuthenticated: true,
                isLoading: false,
              });
            } catch {
              // Token expired, clear auth
              AuthService.clearAuthState();
              set({
                user: null,
                isAuthenticated: false,
                isLoading: false,
              });
            }
          } else {
            set({
              user: null,
              isAuthenticated: false,
              isLoading: false,
            });
          }
        } catch (error) {
          AuthService.clearAuthState();
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },
      
      // Clear error
      clearError: () => {
        set({ error: null });
      },
      
      // Set user directly
      setUser: (user: UserResponse | null) => {
        set({
          user,
          isAuthenticated: !!user,
        });
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        // Only persist user data, not tokens (they're in localStorage separately)
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Selector hooks for better performance
export const useUser = () => useAuthStore((state) => state.user);
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated);
export const useIsAuthLoading = () => useAuthStore((state) => state.isLoading);
export const useAuthError = () => useAuthStore((state) => state.error);
