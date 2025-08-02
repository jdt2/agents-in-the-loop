import { Todo, UpdateTodoRequest, FilterType } from '../types/todo';
import { TodoItem } from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  filter: FilterType;
  onUpdate: (id: number, todo: UpdateTodoRequest) => Promise<any>;
  onDelete: (id: number) => Promise<void>;
  loading: boolean;
}

export const TodoList = ({ todos, filter, onUpdate, onDelete, loading }: TodoListProps) => {
  if (todos.length === 0) {
    const emptyMessages = {
      all: 'No todos yet. Add one above!',
      active: 'No active todos. Great job!',
      completed: 'No completed todos yet.'
    };

    return (
      <div 
        id="todo-list"
        className="text-center py-8 text-gray-500"
        role="tabpanel"
        aria-labelledby={`filter-${filter}`}
      >
        <div className="text-4xl mb-4">📝</div>
        <p>{emptyMessages[filter]}</p>
      </div>
    );
  }

  return (
    <div 
      id="todo-list"
      className="space-y-3"
      role="tabpanel"
      aria-labelledby={`filter-${filter}`}
      aria-live="polite"
    >
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onUpdate={onUpdate}
          onDelete={onDelete}
          loading={loading}
        />
      ))}
    </div>
  );
};