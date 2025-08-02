import { useState, useRef, useEffect } from 'react';
import { Todo, UpdateTodoRequest } from '../types/todo';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: number, todo: UpdateTodoRequest) => Promise<any>;
  onDelete: (id: number) => Promise<void>;
  loading: boolean;
}

export const TodoItem = ({ todo, onUpdate, onDelete, loading }: TodoItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(todo.title);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  const validateTitle = (value: string): boolean => {
    if (value.trim().length === 0) {
      setValidationError('Todo title cannot be empty');
      return false;
    }
    if (value.length > 200) {
      setValidationError('Todo title must be 200 characters or less');
      return false;
    }
    setValidationError(null);
    return true;
  };

  const handleToggleComplete = async () => {
    try {
      await onUpdate(todo.id, {
        title: todo.title,
        completed: !todo.completed
      });
    } catch (error) {
      // Error handled by parent
    }
  };

  const handleStartEdit = () => {
    setIsEditing(true);
    setEditValue(todo.title);
    setValidationError(null);
  };

  const handleSaveEdit = async () => {
    if (!validateTitle(editValue)) {
      return;
    }

    try {
      await onUpdate(todo.id, {
        title: editValue.trim(),
        completed: todo.completed
      });
      setIsEditing(false);
      setValidationError(null);
    } catch (error) {
      // Error handled by parent
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditValue(todo.title);
    setValidationError(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSaveEdit();
    } else if (e.key === 'Escape') {
      handleCancelEdit();
    }
  };

  const handleDelete = async () => {
    if (!showDeleteConfirm) {
      setShowDeleteConfirm(true);
      return;
    }

    try {
      await onDelete(todo.id);
      setShowDeleteConfirm(false);
    } catch (error) {
      // Error handled by parent
    }
  };

  const handleCheckboxKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === ' ') {
      e.preventDefault();
      handleToggleComplete();
    }
  };

  return (
    <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm border border-gray-200 group hover:shadow-md transition-shadow">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggleComplete}
        onKeyDown={handleCheckboxKeyDown}
        disabled={loading}
        className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
        aria-label={`Mark "${todo.title}" as ${todo.completed ? 'incomplete' : 'complete'}`}
      />

      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div>
            <input
              ref={inputRef}
              type="text"
              value={editValue}
              onChange={(e) => {
                setEditValue(e.target.value);
                if (validationError) {
                  validateTitle(e.target.value);
                }
              }}
              onKeyDown={handleKeyDown}
              onBlur={handleCancelEdit}
              className="w-full input-field"
              disabled={loading}
              maxLength={200}
              aria-label="Edit todo title"
              aria-describedby={validationError ? "edit-error" : undefined}
            />
            {validationError && (
              <div 
                id="edit-error" 
                className="mt-1 text-sm text-red-600"
                role="alert"
              >
                {validationError}
              </div>
            )}
          </div>
        ) : (
          <span
            onDoubleClick={handleStartEdit}
            className={`block text-sm break-words cursor-pointer hover:text-blue-600 transition-colors ${
              todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
            title="Double-click to edit"
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleStartEdit();
              }
            }}
            aria-label={`Todo: ${todo.title}. Double-click to edit.`}
          >
            {todo.title}
          </span>
        )}
      </div>

      <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        {loading && <div className="loading-spinner"></div>}
        <button
          onClick={handleDelete}
          disabled={loading}
          className={`text-xs px-2 py-1 rounded transition-colors ${
            showDeleteConfirm
              ? 'bg-red-500 text-white hover:bg-red-600'
              : 'bg-gray-200 text-gray-600 hover:bg-red-100 hover:text-red-600'
          }`}
          aria-label={showDeleteConfirm ? `Confirm delete "${todo.title}"` : `Delete "${todo.title}"`}
        >
          {showDeleteConfirm ? 'Confirm' : 'Delete'}
        </button>
        {showDeleteConfirm && (
          <button
            onClick={() => setShowDeleteConfirm(false)}
            disabled={loading}
            className="text-xs px-2 py-1 bg-gray-200 text-gray-600 hover:bg-gray-300 rounded transition-colors"
            aria-label="Cancel delete"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
};