export interface Product {
  id: number;
  name: string;
  price: number;
}

export interface DummyData {
  products: Product[];
  timestamp: string;
}

export interface ApiResponse {
  source: 'redis' | 'generated';
  data: DummyData;
}