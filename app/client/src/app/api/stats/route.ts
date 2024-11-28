import { NextResponse } from 'next/server';

const API_SERVICE = process.env.FASTAPI_INTERNAL_URL;

export async function GET() {
  try {
    const response = await fetch(`${API_SERVICE}/api/stats`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch stats');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json(
      { error: 'Failed to fetch stats' },
      { status: 500 }
    );
  }
}