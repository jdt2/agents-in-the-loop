import { useTodos } from '../hooks/useTodos';
import { TodoForm } from './TodoForm';
import { TodoList } from './TodoList';
import { FilterButtons } from './FilterButtons';
import { TodoCounter } from './TodoCounter';

export const TodoApp = () => {
  const {
    todos,
    filter,
    loading,
    error,
    activeTodosCount,
    setFilter,
    createTodo,
    updateTodo,
    deleteTodo,
    clearError,
    refetch
  } = useTodos();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Todo App</h1>
          <p className="text-gray-600">Stay organized and get things done</p>
        </header>

        <div className="bg-white rounded-lg shadow-lg p-6">
          {error && (
            <div className="error-message flex justify-between items-center">
              <span>{error}</span>
              <button
                onClick={clearError}
                className="text-red-700 hover:text-red-900 font-bold text-lg"
                aria-label="Dismiss error"
              >
                ×
              </button>
            </div>
          )}

          <TodoForm onSubmit={createTodo} loading={loading} />

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <FilterButtons
              currentFilter={filter}
              onFilterChange={setFilter}
            />
            <TodoCounter count={activeTodosCount} />
          </div>

          <TodoList
            todos={todos}
            filter={filter}
            onUpdate={updateTodo}
            onDelete={deleteTodo}
            loading={loading}
          />

          {error && (
            <div className="mt-6 text-center">
              <button
                onClick={refetch}
                className="btn-secondary"
                disabled={loading}
              >
                {loading ? 'Retrying...' : 'Try Again'}
              </button>
            </div>
          )}
        </div>

        <footer className="text-center mt-8 text-gray-500 text-sm">
          <p>Built with React, TypeScript, and Tailwind CSS</p>
        </footer>
      </div>
    </div>
  );
};