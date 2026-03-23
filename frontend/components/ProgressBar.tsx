interface ProgressBarProps {
  current: number | null;
  total: number | null;
}

export function ProgressBar({ current, total }: ProgressBarProps) {
  if (total === null || current === null) return null;

  const percentage = Math.min((current / total) * 100, 100);

  return (
    <div className="mb-4">
      <p className="text-sm text-gray-600 mb-2">
        Checking claim {current} of {total}...
      </p>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
