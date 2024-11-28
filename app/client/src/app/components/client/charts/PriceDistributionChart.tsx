"use client";

import { ProductStats } from "@/app/types/stats";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface Props {
  data: ProductStats["price_ranges"];
}

export function PriceDistributionChart({ data }: Props) {
  const chartData = Object.entries(data).map(([range, count]) => ({
    range,
    count,
  }));
  return (
    <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
      <h3 className="text-lg font-semibold mb-4 text-slate-300">Price Distribution</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="range" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{ backgroundColor: "#1e293b", border: "none", borderRadius: "0.5rem" }}
              labelStyle={{ color: "#e2e8f0" }}
              itemStyle={{ color: "#e2e8f0" }}
            />
            <Legend wrapperStyle={{ color: "#e2e8f0" }} />
            <Bar dataKey="count" fill="#60a5fa" name="Number of Products" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
