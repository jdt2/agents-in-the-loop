export interface Todo {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;  // ISO date string
  updated_at: string;  // ISO date string
}

export interface CreateTodoRequest {
  title: string;
  completed: boolean;
}

export interface UpdateTodoRequest {
  title: string;
  completed: boolean;
}

export type FilterType = 'all' | 'active' | 'completed';