import { ProductStats } from "@/app/types/stats";

export async function getStats(): Promise<ProductStats> {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const res = await fetch(`${API_URL}/stats`, {
    next: { revalidate: 300 },
  });
  
  if (!res.ok) {
    throw new Error("Failed to fetch stats");
  }
  return res.json();
}