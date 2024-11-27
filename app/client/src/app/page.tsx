'use client';

import { useEffect, useState } from 'react';
import { ApiResponse } from './types';

export default function Home() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/dummy');
        const result = await response.json();
        setData(result as ApiResponse);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Test Data Display</h1>
      <div className="bg-gray-100 p-4 rounded">
        <p>Data Source: {data?.source}</p>
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Products</h2>
          {data?.data.products.map(product => (
            <div key={product.id} className="bg-white p-2 rounded mb-2">
              <p>Name: {product.name}</p>
              <p>Price: ${product.price}</p>
            </div>
          ))}
        </div>
        <p className="mt-4 text-sm text-gray-600">
          Last updated: {data?.data.timestamp}
        </p>
      </div>
    </div>
  );
}