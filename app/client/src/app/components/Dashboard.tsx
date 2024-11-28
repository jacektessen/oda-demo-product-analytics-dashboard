"use client";

import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import type { ProductStats } from "../types/stats";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8"];

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Dashboard() {
  const [stats, setStats] = useState<ProductStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${API_URL}/stats`);
        if (!response.ok) {
          throw new Error("Failed to fetch stats");
        }
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (error) {
    return <div className="text-red-500 p-4 border border-red-300 rounded bg-red-50">Error: {error}</div>;
  }

  if (!stats) {
    return <div>No data available</div>;
  }

  const priceRangeData = Object.entries(stats.price_ranges).map(([range, count]) => ({
    range,
    count,
  }));

  const topBrandsData = stats.top_brands.filter((brand) => brand.name !== "Unknown").slice(0, 5);

  const categoriesData = Object.entries(stats.categories)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  return (
    <div className="p-6 space-y-6">
      {/* Summary Cards */}
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
            <p>Last Updated: {new Date(stats.last_updated).toLocaleString()}</p>
            <p>Next Update: {Math.floor(stats.cache_info.next_update_in / 60)} minutes</p>
          </div>
        </div>
      </div>

      {/* Price Range Chart */}
      <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-4 text-slate-300">Price Distribution</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={priceRangeData}>
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Charts with same styling pattern */}
        <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4 text-slate-300">Top 5 Brands</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={topBrandsData}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}>
                  {topBrandsData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: "#1e293b", border: "none", borderRadius: "0.5rem" }}
                  labelStyle={{ color: "#e2e8f0" }}
                  itemStyle={{ color: "#e2e8f0" }}
                />
                <Legend wrapperStyle={{ color: "#e2e8f0" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4 text-slate-300">Top 10 Categories</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoriesData} layout="vertical" margin={{ left: 150 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                <XAxis type="number" stroke="#94a3b8" />
                <YAxis dataKey="name" type="category" width={150} stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#1e293b", border: "none", borderRadius: "0.5rem" }}
                  labelStyle={{ color: "#e2e8f0" }}
                  itemStyle={{ color: "#e2e8f0" }}
                />
                <Legend wrapperStyle={{ color: "#e2e8f0" }} />
                <Bar dataKey="count" fill="#4ade80" name="Number of Products" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
