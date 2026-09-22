"use client";

import { Inter } from "next/font/google";
import { ThemeProvider } from "next-themes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "sonner";
import { MotionConfig } from "framer-motion";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Metadata
export const metadata = {
  title: {
    default: "Aesstore | B2B E-commerce Platform",
    template: "%s | Aesstore",
  },
  description: "Modern B2B e-commerce platform for businesses",
  keywords: ["B2B", "e-commerce", "wholesale", "business", "platform"],
  authors: [{ name: "Aesstore Team" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://aesstore.com",
    siteName: "Aesstore",
    title: "Aesstore | B2B E-commerce Platform",
    description: "Modern B2B e-commerce platform for businesses",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aesstore | B2B E-commerce Platform",
    description: "Modern B2B e-commerce platform for businesses",
  },
  robots: {
    index: true,
    follow: true,
  },
};

// Root Layout
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <QueryClientProvider client={queryClient}>
            <MotionConfig reducedMotion="user">
              <Toaster
                position="top-right"
                richColors
                closeButton
                toastOptions={{
                  unstyled: false,
                  classNames: {
                    toast: "group toast group-[.toast]",
                    success: "border-green-500",
                    error: "border-red-500",
                    warning: "border-yellow-500",
                    info: "border-blue-500",
                  },
                }}
              />
              {children}
              <ReactQueryDevtools initialIsOpen={false} />
            </MotionConfig>
          </QueryClientProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
