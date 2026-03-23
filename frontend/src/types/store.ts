export interface Store {
  id: string;
  name: string;
  shopify_domain: string;
  status: "creating" | "setup" | "active" | "paused" | "error";
  niche: string;
  monthly_revenue: number;
  created_at: string;
}

export interface Product {
  id: string;
  store_id: string;
  title: string;
  description: string;
  price: number;
  cost_price: number;
  supplier_url: string;
  image_urls: string[];
  status: "researched" | "listing" | "live" | "paused" | "archived";
  research_score: number;
  conversion_rate: number;
  created_at: string;
}

export interface Order {
  id: string;
  store_id: string;
  shopify_order_id: number;
  customer_email: string;
  total_price: number;
  profit: number;
  status: "new" | "processing" | "fulfilled" | "cancelled" | "refunded";
  created_at: string;
}

export interface AgentLog {
  id: string;
  store_id: string | null;
  agent_type: string;
  action: string;
  status: "started" | "running" | "completed" | "failed";
  tokens_used: number;
  cost_usd: number;
  duration_ms: number;
  created_at: string;
}

export interface AnalyticsOverview {
  total_revenue: number;
  total_orders: number;
  total_profit: number;
  active_stores: number;
  conversion_rate: number;
  ai_cost_today: number;
}
