"use client";

import { ProductStats } from "@/app/types/stats";
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8"];

interface Props {
  data: ProductStats["top_brands"];
  totalProducts: ProductStats["total_products"];
}

export function TopBrandsChart({ data, totalProducts }: Props) {
  const filteredData = data
    .filter((brand) => brand.name !== "Unknown")
    .slice(0, 5)
    .map((brand) => ({
      ...brand,
      percentage: ((brand.count / totalProducts) * 100).toFixed(1),
    }));

  return (
    <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
      <h3 className="text-lg font-semibold mb-4 text-slate-300">Top 5 Brands</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={filteredData}
              dataKey="count"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={80}
              label={({ name, payload }) => `${name} (${payload.percentage}%)`}>
              {filteredData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: "#1e293b", border: "none", borderRadius: "0.5rem" }}
              labelStyle={{ color: "#e2e8f0" }}
              itemStyle={{ color: "#e2e8f0" }}
              formatter={(value, name, entry) => [`${entry.payload.percentage}%`, name]}
            />
            <Legend wrapperStyle={{ color: "#e2e8f0" }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
