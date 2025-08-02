# Frontend Development Instructions - Todo Application

## Project Overview
You are building the React TypeScript frontend for a full-stack todo application. This frontend will communicate with a FastAPI backend running on port 8000.

## Critical Configuration Requirements

### Development Server
- **Port**: 3001 (mandatory)
- **Start Command**: `npm run dev` or `yarn dev`
- **Base URL for API**: `http://localhost:8000/api`

### API Integration Settings
```typescript
// src/config/api.ts
export const API_BASE_URL = 'http://localhost:8000/api';
```

## Required Technology Stack

### Core Dependencies
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.0.0"
  }
}
```

### Build Tool Configuration
- Use Vite as the build tool
- Configure Vite to run on port 3001
- Enable TypeScript strict mode

## Exact Data Models (Must Match Backend)

### TypeScript Interface
```typescript
// src/types/todo.ts
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
```

## Exact API Endpoints (Must Match Backend Implementation)

### API Service Layer
Create `src/services/todoService.ts` with these exact endpoints:

```typescript
// src/services/todoService.ts
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
```

## Required Components Architecture

### Component Structure
```
src/
  components/
    TodoApp.tsx         # Main application container
    TodoList.tsx        # List of todos with filtering
    TodoItem.tsx        # Individual todo item
    TodoForm.tsx        # Form for adding new todos
    FilterButtons.tsx   # Filter by status buttons
    TodoCounter.tsx     # Count of active tasks
  services/
    todoService.ts      # API communication layer
  types/
    todo.ts            # TypeScript interfaces
  hooks/
    useTodos.ts        # Custom hook for todo state management
  App.tsx              # Root component
  main.tsx            # Entry point
```

### Component Specifications

#### TodoApp.tsx (Main Container)
- Manages global todo state using useState
- Handles all API calls through todoService
- Passes data and handlers to child components
- Implements error handling with user-friendly messages
- Manages filter state (All, Active, Completed)

#### TodoList.tsx
- Receives todos array and filter state as props
- Filters todos based on current filter
- Renders TodoItem components
- Handles empty states

#### TodoItem.tsx
- Displays individual todo with checkbox and text
- Implements inline editing on double-click
- Delete button with confirmation
- Toggle completion status
- Handles loading states during API calls

#### TodoForm.tsx
- Input field for new todo title
- Submit on Enter key or button click
- Client-side validation (1-200 characters)
- Clear input after successful submission

#### FilterButtons.tsx
- Three buttons: All, Active, Completed
- Highlights current active filter
- Updates parent component's filter state

#### TodoCounter.tsx
- Displays count of active (incomplete) todos
- Updates in real-time as todos change

## State Management Requirements

### Main State Structure
```typescript
const [todos, setTodos] = useState<Todo[]>([]);
const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

### Data Flow
1. Load todos on component mount
2. Update local state after successful API calls
3. Handle loading states during API operations
4. Display error messages for failed operations
5. Clear errors after successful operations

## Styling Requirements

### Tailwind CSS Setup
- Configure Tailwind CSS for utility-first styling
- Implement responsive design (mobile-first)
- Use consistent color scheme throughout app

### UI Requirements
- Clean, professional design
- Mobile-friendly responsive layout
- Smooth hover effects and transitions
- Accessible color contrast (WCAG AA)
- Loading spinners for API operations
- Error message styling (red backgrounds/text)

## User Interaction Specifications

### Keyboard Accessibility
- Tab navigation through all interactive elements
- Enter key submits new todos
- Escape key cancels inline editing
- Space bar toggles todo completion

### Mouse Interactions
- Click checkbox to toggle completion
- Double-click todo text to edit inline
- Click delete button to remove todo
- Click filter buttons to change view

## Error Handling Requirements

### API Error Handling
- Network errors: "Unable to connect to server"
- Validation errors: Display specific field errors
- Server errors: "Something went wrong, please try again"
- Timeout errors: "Request timed out"

### User Feedback
- Show loading states during API calls
- Display success messages for actions
- Highlight errors with red styling
- Auto-clear error messages after 5 seconds

## Development Workflow

### Setup Commands
```bash
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm run dev  # Must run on port 3001
```

### Development Guidelines
1. Start with component structure before implementing functionality
2. Implement API service layer first
3. Add components one by one, testing API integration
4. Implement error handling for all API calls
5. Add responsive styling last
6. Test all user interactions thoroughly

## Integration Testing Checklist

### API Integration Tests
- [ ] Can fetch all todos from backend
- [ ] Can create new todos
- [ ] Can update existing todos
- [ ] Can delete todos
- [ ] Error handling works for all endpoints
- [ ] Loading states display correctly

### User Experience Tests
- [ ] All filter buttons work correctly
- [ ] Todo counter updates in real-time
- [ ] Inline editing saves changes
- [ ] Keyboard navigation works
- [ ] Mobile responsive design works
- [ ] Error messages are user-friendly

## Critical Success Factors

1. **API Compatibility**: All API calls must exactly match backend endpoints
2. **Data Consistency**: Todo data model must match backend exactly
3. **Port Configuration**: Frontend must run on port 3001
4. **Error Handling**: Graceful handling of all error scenarios
5. **Responsive Design**: Works on mobile and desktop
6. **Performance**: Fast loading and smooth interactions

## Notes for Implementation

- Always validate user input before sending to API
- Implement optimistic updates where appropriate
- Use TypeScript strictly - no 'any' types
- Follow React best practices for state management
- Ensure CORS will work with backend on port 8000
- Test thoroughly with backend before considering complete

The backend team is implementing the exact API endpoints specified above. Your frontend implementation must match these specifications precisely for successful integration.