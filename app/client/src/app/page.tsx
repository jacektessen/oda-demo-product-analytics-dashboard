import { Dashboard } from "./components/Dashboard";
import { ProductStats } from "@/app/types/stats";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function getStats(): Promise<ProductStats> {
  const res = await fetch(`${API_URL}/stats`, {
    next: { revalidate: 300 }, // 5 minutes
  });

  if (!res.ok) {
    throw new Error("Failed to fetch stats");
  }

  return res.json();
}

export default async function Home() {
  const stats = await getStats();

  return (
    <main className="min-h-screen bg-slate-900">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-8 text-white">Product Analytics Dashboard</h1>
        <Dashboard stats={stats} />
      </div>
    </main>
  );
}
