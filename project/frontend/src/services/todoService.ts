import { Todo, CreateTodoRequest, UpdateTodoRequest } from '../types/todo';

const API_BASE_URL = 'http://localhost:8000/api';

export const todoService = {
  // GET /api/todos
  async getAllTodos(): Promise<Todo[]> {
    const response = await fetch(`${API_BASE_URL}/todos`);
    if (!response.ok) throw new Error('Failed to fetch todos');
    return response.json();
  },

  // POST /api/todos
  async createTodo(todo: CreateTodoRequest): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(todo)
    });
    if (!response.ok) throw new Error('Failed to create todo');
    return response.json();
  },

  // PUT /api/todos/{id}
  async updateTodo(id: number, todo: UpdateTodoRequest): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(todo)
    });
    if (!response.ok) throw new Error('Failed to update todo');
    return response.json();
  },

  // DELETE /api/todos/{id}
  async deleteTodo(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete todo');
  }
};