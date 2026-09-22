"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Package, ShoppingCart, Users, DollarSign, TrendingUp, Clock, CheckCircle, XCircle } from "lucide-react";
import { motion } from "framer-motion";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/stores/auth-store";
import { formatPrice } from "@/lib/utils";

// Stats card component
const StatsCard = ({
  title,
  value,
  change,
  icon: Icon,
  color = "text-primary",
}: {
  title: string;
  value: string | number;
  change: string;
  icon: React.ElementType;
  color?: string;
}) => (
  <Card className="hover:shadow-md transition-shadow">
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      <Icon className={`h-4 w-4 ${color}`} />
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      <p className={`text-xs ${change.startsWith("+") ? "text-green-500" : "text-red-500"}`}>
        {change}
      </p>
    </CardContent>
  </Card>
);

// Dashboard page component
export default function DashboardPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [stats, setStats] = useState({
    totalSales: 0,
    totalOrders: 0,
    totalCustomers: 0,
    totalProducts: 0,
    pendingOrders: 0,
    completedOrders: 0,
    cancelledOrders: 0,
  });
  const [recentOrders, setRecentOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch dashboard stats (mock data for now)
    const fetchStats = async () => {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      
      setStats({
        totalSales: 125000,
        totalOrders: 245,
        totalCustomers: 89,
        totalProducts: 156,
        pendingOrders: 12,
        completedOrders: 210,
        cancelledOrders: 23,
      });
      
      setRecentOrders([
        { id: "#ORD-001", customer: "Acme Corp", amount: 1250.0, status: "completed", date: "2024-01-15" },
        { id: "#ORD-002", customer: "Tech Solutions", amount: 890.5, status: "pending", date: "2024-01-14" },
        { id: "#ORD-003", customer: "Global Inc", amount: 2100.0, status: "completed", date: "2024-01-13" },
        { id: "#ORD-004", customer: "Local Shop", amount: 450.75, status: "cancelled", date: "2024-01-12" },
        { id: "#ORD-005", customer: "Enterprise Ltd", amount: 3200.0, status: "pending", date: "2024-01-11" },
      ]);
      
      setIsLoading(false);
    };
    
    fetchStats();
  }, []);

  // Get status badge color
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "pending":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "cancelled":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return <CheckCircle className="h-3 w-3" />;
      case "pending":
        return <Clock className="h-3 w-3" />;
      case "cancelled":
        return <XCircle className="h-3 w-3" />;
      default:
        return null;
    }
  };

  // Redirect if no user
  if (!user) {
    router.replace("/auth/login");
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Welcome back, {user.first_name || "User"}!
            </h1>
            <p className="text-muted-foreground">
              Here&apos;s what&apos;s happening with your store today.
            </p>
          </div>
          <Button onClick={() => router.push("/dashboard/products")}>
            View Products
          </Button>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4"
      >
        <StatsCard
          title="Total Sales"
          value={formatPrice(stats.totalSales)}
          change="+12% from last month"
          icon={DollarSign}
          color="text-green-500"
        />
        <StatsCard
          title="Total Orders"
          value={stats.totalOrders}
          change="+8% from last month"
          icon={ShoppingCart}
          color="text-blue-500"
        />
        <StatsCard
          title="Total Customers"
          value={stats.totalCustomers}
          change="+5% from last month"
          icon={Users}
          color="text-purple-500"
        />
        <StatsCard
          title="Total Products"
          value={stats.totalProducts}
          change="+15% from last month"
          icon={Package}
          color="text-orange-500"
        />
      </motion.div>

      {/* Order Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-1 gap-4 md:grid-cols-3"
      >
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Pending Orders</CardTitle>
            <Clock className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pendingOrders}</div>
            <p className="text-xs text-muted-foreground">
              Awaiting processing
            </p>
          </CardContent>
        </Card>
        
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Completed Orders</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedOrders}</div>
            <p className="text-xs text-muted-foreground">
              Successfully delivered
            </p>
          </CardContent>
        </Card>
        
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Cancelled Orders</CardTitle>
            <XCircle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.cancelledOrders}</div>
            <p className="text-xs text-muted-foreground">
              Orders cancelled
            </p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Recent Orders */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="space-y-4"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Recent Orders</h2>
          <Button variant="outline" size="sm" onClick={() => router.push("/dashboard/orders")}>
            View All
          </Button>
        </div>
        
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Order ID
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {recentOrders.map((order: any, index) => (
                    <tr
                      key={order.id}
                      className="border-b border-muted/20 hover:bg-muted/50 transition-colors"
                    >
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {order.id}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {order.customer}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {formatPrice(order.amount)}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}
                        >
                          {getStatusIcon(order.status)}
                          <span className="ml-1">{order.status}</span>
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-muted-foreground">
                        {order.date}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => router.push(`/dashboard/orders/${order.id.replace("#", "")}`)}
                        >
                          View
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
