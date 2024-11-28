import { Suspense } from "react";
import { Dashboard } from "./components/Dashboard";
import { getStats } from "@/app/utils/api";
import Loading from "./loading";

async function DashboardContent() {
  const stats = await getStats();
  return <Dashboard stats={stats} />;
}

export default async function Home() {
  return (
    <main className="min-h-screen bg-slate-900">
      <div className="container mx-auto p-4 sm:p-8">
        <h1 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-white">Product Analytics Dashboard</h1>
        <Suspense fallback={<Loading />}>
          <DashboardContent />
        </Suspense>
      </div>
    </main>
  );
}
