interface TodoCounterProps {
  count: number;
}

export const TodoCounter = ({ count }: TodoCounterProps) => {
  const itemText = count === 1 ? 'item' : 'items';
  
  return (
    <div className="text-sm text-gray-600" role="status" aria-live="polite">
      {count} {itemText} left
    </div>
  );
};