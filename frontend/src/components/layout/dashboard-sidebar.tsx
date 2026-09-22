"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Home, Package, ShoppingCart, Users, BarChart3, Settings, LogOut, Store, FileText, Bell, HelpCircle } from "lucide-react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { useAuthStore } from "@/stores/auth-store";
import { cn, getInitials } from "@/lib/utils";

// Sidebar navigation items
const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: Home },
  { label: "Products", href: "/dashboard/products", icon: Package },
  { label: "Categories", href: "/dashboard/categories", icon: Store },
  { label: "Orders", href: "/dashboard/orders", icon: ShoppingCart },
  { label: "Customers", href: "/dashboard/customers", icon: Users },
  { label: "Invoices", href: "/dashboard/invoices", icon: FileText },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
];

const bottomNavItems = [
  { label: "Notifications", href: "/dashboard/notifications", icon: Bell },
  { label: "Help & Support", href: "/dashboard/support", icon: HelpCircle },
];

// Sidebar item component
const SidebarItem = ({
  item,
  isActive,
  onClick,
}: {
  item: { label: string; href: string; icon: React.ElementType };
  isActive: boolean;
  onClick?: () => void;
}) => (
  <Link
    href={item.href}
    onClick={onClick}
    className={cn(
      "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors hover:bg-muted/50",
      isActive && "bg-primary/10 text-primary font-medium"
    )}
  >
    <item.icon className={cn("h-5 w-5", isActive ? "text-primary" : "text-muted-foreground")} />
    <span className="truncate">{item.label}</span>
  </Link>
);

// Dashboard sidebar component
export function DashboardSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Handle logout
  const handleLogout = async () => {
    await logout();
    router.replace("/auth/login");
  };

  return (
    <motion.aside
      className={cn(
        "fixed left-0 top-0 z-40 h-screen w-64 border-r bg-background flex flex-col",
        isCollapsed && "w-20"
      )}
      initial={{ width: 256 }}
      animate={{ width: isCollapsed ? 80 : 256 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
    >
      {/* Logo */}
      <div className="flex items-center justify-between h-16 px-4 border-b">
        {!isCollapsed ? (
          <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: isCollapsed ? 0 : 1 }}
            transition={{ duration: 0.2 }}
            className="flex items-center gap-2"
          >
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Store className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-lg">Aesstore</span>
          </motion.div>
        ) : (
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center mx-auto">
            <Store className="h-5 w-5 text-primary-foreground" />
          </div>
        )}
        
        <Button
          variant="ghost"
          size="icon"
          className={cn("h-8 w-8", isCollapsed && "mx-auto")}
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? (
            <motion.div
              initial={{ rotate: 0 }}
              animate={{ rotate: 180 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronRight className="h-4 w-4" />
            </motion.div>
          ) : (
            <motion.div
              initial={{ rotate: 180 }}
              animate={{ rotate: 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronLeft className="h-4 w-4" />
            </motion.div>
          )}
        </Button>
      </div>

      {/* Navigation */}
      <div className="flex-1 p-4 space-y-1">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="space-y-1"
        >
          {navItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <SidebarItem
                key={item.href}
                item={item}
                isActive={isActive}
              />
            );
          })}
        </motion.div>
      </div>

      {/* Bottom Section */}
      <div className="p-4 border-t space-y-4">
        {/* Notifications and Help */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="space-y-1"
        >
          {bottomNavItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <SidebarItem
                key={item.href}
                item={item}
                isActive={isActive}
              />
            );
          })}
        </motion.div>

        {/* User Profile */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex items-center gap-3 p-3 rounded-lg bg-muted/50"
        >
          <Avatar className="h-10 w-10">
            {user?.first_name && user?.last_name ? (
              <AvatarFallback className="bg-primary text-primary-foreground">
                {getInitials(`${user.first_name} ${user.last_name}`)}
              </AvatarFallback>
            ) : null}
            {user?.email && (
              <AvatarImage src={`https://avatar.vercel.sh/${user.email}`} />
            )}
          </Avatar>
          
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-sm text-muted-foreground truncate">
                {user?.email}
              </p>
            </div>
          )}
          
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={handleLogout}
            title="Logout"
          >
            <LogOut className="h-4 w-4" />
          </Button>
        </motion.div>
      </div>
    </motion.aside>
  );
}

// Import Chevron icons
import { ChevronLeft, ChevronRight } from "lucide-react";
