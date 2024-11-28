import { NextResponse } from 'next/server';
import type { ProductStats } from '@/app/types/stats';

const API_SERVICE = process.env.FASTAPI_INTERNAL_URL;

export async function GET() {
  if (!API_SERVICE) {
    return NextResponse.json(
      { error: 'API service URL not configured' },
      { status: 500 }
    );
  }

  try {
    const response = await fetch(`${API_SERVICE}/api/stats`, {
      cache: 'no-store',
      next: { revalidate: 0 }
    });
    
    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`);
    }

    const data: ProductStats = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('Error fetching stats:', error);
    const message = error instanceof Error ? error.message : 'Unknown error';
    
    return NextResponse.json(
      { error: message },
      { status: 500 }
    );
  }
}