export interface Design {
  id: string;
  name: string;
  description: string;
  style: string;
  price: number;
  imageUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Lease {
  id: string;
  designId: string;
  userId: string;
  startDate: Date;
  endDate: Date;
  status: 'active' | 'pending' | 'completed' | 'cancelled';
  totalCost: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'client' | 'designer' | 'admin';
  createdAt: Date;
}
