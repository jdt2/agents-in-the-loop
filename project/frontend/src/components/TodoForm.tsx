import { useState } from 'react';
import { CreateTodoRequest } from '../types/todo';

interface TodoFormProps {
  onSubmit: (todo: CreateTodoRequest) => Promise<any>;
  loading: boolean;
}

export const TodoForm = ({ onSubmit, loading }: TodoFormProps) => {
  const [title, setTitle] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateTitle(title)) {
      return;
    }

    try {
      await onSubmit({
        title: title.trim(),
        completed: false
      });
      setTitle('');
      setValidationError(null);
    } catch (error) {
      // Error handling is done by the parent component
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e as any);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex gap-2">
        <input
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (validationError) {
              validateTitle(e.target.value);
            }
          }}
          onKeyDown={handleKeyDown}
          placeholder="What needs to be done?"
          className="flex-1 input-field"
          disabled={loading}
          maxLength={200}
          aria-label="New todo title"
          aria-describedby={validationError ? "title-error" : undefined}
        />
        <button
          type="submit"
          disabled={loading || title.trim().length === 0}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loading && <div className="loading-spinner"></div>}
          Add Todo
        </button>
      </div>
      {validationError && (
        <div 
          id="title-error" 
          className="mt-2 text-sm text-red-600"
          role="alert"
          aria-live="polite"
        >
          {validationError}
        </div>
      )}
    </form>
  );
};