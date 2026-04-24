'use client';

import { useState } from 'react';
import { Hostel } from '@/lib/types';
import HostelCard from './HostelCard';

const CATEGORIES = [
  { id: 'all', label: 'All Stays', icon: '🏠' },
  { id: 'Algiers', label: 'Algiers', icon: '🕌' },
  { id: 'Oran', label: 'Oran', icon: '🌊' },
  { id: 'Constantine', label: 'Constantine', icon: '🌉' },
  { id: 'Annaba', label: 'Annaba', icon: '🌴' },
];

interface HostelGridProps {
  hostels: Hostel[];
  initialCity?: string;
}

export default function HostelGrid({ hostels, initialCity = 'all' }: HostelGridProps) {
  const [activeCity, setActiveCity] = useState(initialCity);

  const filtered = activeCity === 'all'
    ? hostels
    : hostels.filter(h => h.city === activeCity);

  return (
    <div>
      {/* Category pills */}
      <div
        className="flex overflow-x-auto border-b border-border-gray mb-6"
        style={{ scrollbarWidth: 'none' }}
      >
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => setActiveCity(cat.id)}
            className={[
              'flex flex-col items-center gap-1 px-5 py-3 flex-shrink-0 border-b-2 -mb-px transition-all',
              activeCity === cat.id
                ? 'border-near-black opacity-100'
                : 'border-transparent opacity-55 hover:opacity-90',
            ].join(' ')}
          >
            <span className="text-2xl">{cat.icon}</span>
            <span className="text-[12px] font-semibold text-near-black whitespace-nowrap">{cat.label}</span>
          </button>
        ))}
      </div>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pb-14">
          {filtered.map(h => (
            <HostelCard key={h.id} hostel={h} />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center py-16 text-center">
          <span className="text-5xl mb-4">🔍</span>
          <h3 className="text-[18px] font-semibold text-near-black mb-2">No hostels in this category yet</h3>
          <button
            onClick={() => setActiveCity('all')}
            className="mt-2 bg-rausch text-white rounded-airbnb-sm px-6 py-2.5 text-[14px] font-bold hover:bg-rausch-dark transition-colors"
          >
            View all hostels
          </button>
        </div>
      )}
    </div>
  );
}
