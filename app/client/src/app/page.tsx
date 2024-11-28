'use client'

import Dashboard from './components/Dashboard';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-8">Product Analytics Dashboard</h1>
        <Dashboard />
      </div>
    </main>
  );
}