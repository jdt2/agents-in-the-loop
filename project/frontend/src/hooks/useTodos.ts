import { useState, useEffect, useCallback } from 'react';
import { Todo, CreateTodoRequest, UpdateTodoRequest, FilterType } from '../types/todo';
import { todoService } from '../services/todoService';

export const useTodos = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<FilterType>('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const loadTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTodos = await todoService.getAllTodos();
      setTodos(fetchedTodos);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  }, []);

  const createTodo = useCallback(async (todoRequest: CreateTodoRequest) => {
    try {
      setLoading(true);
      setError(null);
      const newTodo = await todoService.createTodo(todoRequest);
      setTodos(prev => [...prev, newTodo]);
      return newTodo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateTodo = useCallback(async (id: number, todoRequest: UpdateTodoRequest) => {
    try {
      setLoading(true);
      setError(null);
      const updatedTodo = await todoService.updateTodo(id, todoRequest);
      setTodos(prev => prev.map(todo => todo.id === id ? updatedTodo : todo));
      return updatedTodo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteTodo = useCallback(async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await todoService.deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const filteredTodos = todos.filter(todo => {
    switch (filter) {
      case 'active':
        return !todo.completed;
      case 'completed':
        return todo.completed;
      default:
        return true;
    }
  });

  const activeTodosCount = todos.filter(todo => !todo.completed).length;

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(clearError, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  return {
    todos: filteredTodos,
    filter,
    loading,
    error,
    activeTodosCount,
    setFilter,
    createTodo,
    updateTodo,
    deleteTodo,
    clearError,
    refetch: loadTodos
  };
};