"use client";

import { ProductStats } from "@/app/types/stats";
import dynamic from "next/dynamic";

interface Props {
  stats: Pick<ProductStats, "total_products" | "average_price" | "last_updated" | "cache_info">;
}

// Dynamically import the DateTimeDisplay component with no SSR
const DateTimeDisplay = dynamic(() => import("../../DateTimeDisplay"), {
  ssr: false,
});

export function SummaryCards({ stats }: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-2 text-slate-300">Total Products</h3>
        <p className="text-3xl font-bold text-blue-400">{stats.total_products.toLocaleString()}</p>
      </div>
      <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-2 text-slate-300">Average Price</h3>
        <p className="text-3xl font-bold text-emerald-400">{stats.average_price.toFixed(2)} kr</p>
      </div>
      <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-2 text-slate-300">Cache Status</h3>
        <div className="space-y-2 text-slate-400">
          <DateTimeDisplay datetime={stats.last_updated} label="Last Updated" />
          <DateTimeDisplay datetime={stats.cache_info.next_update_at} label="Next Update" />
        </div>
      </div>
    </div>
  );
}
