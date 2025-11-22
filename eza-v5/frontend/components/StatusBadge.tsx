/**
 * Status Badge Component
 * Shows data source status (Live/Preview/Loading)
 */

'use client';

import { cn } from '@/lib/utils';

export type StatusType = 'live' | 'preview' | 'loading';

interface StatusBadgeProps {
  status: StatusType;
  className?: string;
}

export default function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = {
    live: {
      label: 'Live data loaded',
      bgColor: 'bg-green-100',
      textColor: 'text-green-800',
      borderColor: 'border-green-300',
      dotColor: 'bg-green-500',
    },
    preview: {
      label: 'Preview data (backend offline)',
      bgColor: 'bg-amber-100',
      textColor: 'text-amber-800',
      borderColor: 'border-amber-300',
      dotColor: 'bg-amber-500',
    },
    loading: {
      label: 'Loading…',
      bgColor: 'bg-blue-100',
      textColor: 'text-blue-800',
      borderColor: 'border-blue-300',
      dotColor: 'bg-blue-500',
    },
  };

  const current = config[status];

  return (
    <div
      className={cn(
        'inline-flex items-center gap-2 px-3 py-1.5 rounded-full border text-sm font-medium',
        current.bgColor,
        current.textColor,
        current.borderColor,
        status === 'loading' && 'animate-pulse',
        className
      )}
    >
      <span className={cn('w-2 h-2 rounded-full', current.dotColor)} />
      <span>{current.label}</span>
    </div>
  );
}

