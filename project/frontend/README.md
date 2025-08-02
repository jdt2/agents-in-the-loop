# Todo App Frontend

A modern, responsive Todo application built with React, TypeScript, and Tailwind CSS. This frontend communicates with a FastAPI backend to provide full CRUD functionality for managing todos.

## Features

- ✅ Create, read, update, and delete todos
- 🔄 Real-time filtering (All, Active, Completed)
- ✏️ Inline editing with double-click
- 📱 Fully responsive design
- ♿ Accessibility features (WCAG AA compliant)
- ⚡ Fast loading with optimistic updates
- 🎨 Clean, modern UI with Tailwind CSS
- 🔒 TypeScript for type safety
- 🚀 Built with Vite for fast development

## Technology Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type safety and better developer experience
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **ESLint** - Code linting and formatting

## Prerequisites

- Node.js (version 16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will start on `http://localhost:3000`.

### 3. Build for Production

```bash
npm run build
```

### 4. Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # React components
│   ├── TodoApp.tsx     # Main application container
│   ├── TodoList.tsx    # List of todos with filtering
│   ├── TodoItem.tsx    # Individual todo item
│   ├── TodoForm.tsx    # Form for adding new todos
│   ├── FilterButtons.tsx # Filter by status buttons
│   └── TodoCounter.tsx # Count of active tasks
├── hooks/
│   └── useTodos.ts     # Custom hook for todo state management
├── services/
│   └── todoService.ts  # API communication layer
├── types/
│   └── todo.ts         # TypeScript interfaces
├── config/
│   └── api.ts          # API configuration
├── App.tsx             # Root component
├── main.tsx           # Entry point
└── index.css          # Global styles and Tailwind imports
```

## API Integration

The frontend expects the backend API to be running on `http://localhost:8000` with the following endpoints:

- `GET /api/todos` - Fetch all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

## User Interactions

### Keyboard Shortcuts
- **Tab** - Navigate through interactive elements
- **Enter** - Submit new todos or save edits
- **Escape** - Cancel inline editing
- **Space** - Toggle todo completion (when checkbox is focused)

### Mouse Interactions
- **Click checkbox** - Toggle completion status
- **Double-click todo text** - Start inline editing
- **Click delete button** - Delete todo (with confirmation)
- **Click filter buttons** - Change view (All/Active/Completed)

## Error Handling

The application includes comprehensive error handling:

- Network connection errors
- API validation errors
- Server errors with user-friendly messages
- Automatic error message clearing after 5 seconds
- Retry functionality for failed requests

## Accessibility Features

- Semantic HTML elements
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast color scheme
- Focus management
- Live regions for dynamic content updates

## Development Scripts

- `npm run dev` - Start development server on port 3000
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style and patterns
2. Ensure TypeScript strict mode compliance
3. Add proper error handling for all API calls
4. Include accessibility features for new components
5. Test responsiveness across different screen sizes

## Troubleshooting

### Common Issues

1. **Port 3000 already in use**: Change the port in `vite.config.ts` or kill the process using port 3000
2. **API connection failed**: Ensure the backend is running on `http://localhost:8000`
3. **Build errors**: Check TypeScript errors and ensure all dependencies are installed

### Environment Variables

Create a `.env.local` file if you need to override the default API URL:

```env
VITE_API_BASE_URL=http://your-api-server.com/api
```

## License

This project is part of a full-stack todo application demo.