// client/src/app/api/dummy/route.ts
import { NextResponse } from 'next/server';
import { ApiResponse } from '../../types';

export async function GET() {
  try {
    const apiServiceUrl = process.env.API_SERVICE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiServiceUrl}/api/dummy-data`);
    const data: ApiResponse = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching dummy data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch data' }, 
      { status: 500 }
    );
  }
}