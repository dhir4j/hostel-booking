'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const CITIES = ['Algiers', 'Oran', 'Constantine', 'Annaba', 'Tlemcen', 'Ghardaïa', 'Tamanrasset', 'Béjaïa'];

interface SearchBarProps {
  initialCity?: string;
  initialCheckIn?: string;
  initialCheckOut?: string;
  initialGuests?: number;
}

export default function SearchBar({
  initialCity = '',
  initialCheckIn = '',
  initialCheckOut = '',
  initialGuests = 1,
}: SearchBarProps) {
  const router = useRouter();
  const [city, setCity] = useState(initialCity);
  const [checkIn, setCheckIn] = useState(initialCheckIn);
  const [checkOut, setCheckOut] = useState(initialCheckOut);
  const [guests, setGuests] = useState(initialGuests);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const suggestions = city ? CITIES.filter(c => c.toLowerCase().includes(city.toLowerCase())) : [];

  const handleSearch = () => {
    const params = new URLSearchParams();
    if (city) params.set('city', city);
    if (checkIn) params.set('checkIn', checkIn);
    if (checkOut) params.set('checkOut', checkOut);
    params.set('guests', String(guests));
    router.push(`/hostels?${params.toString()}`);
  };

  return (
    <div className="flex items-stretch bg-white rounded-[32px] border border-border-gray shadow-airbnb-card">
      {/* Location */}
      <div className="relative flex-[1.5] px-5 py-3.5 border-r border-border-gray">
        <div className="text-[11px] font-bold tracking-wider text-near-black mb-1">WHERE</div>
        <input
          value={city}
          onChange={e => { setCity(e.target.value); setShowSuggestions(true); }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
          placeholder="Search cities in Algeria"
          className="w-full bg-transparent outline-none text-[14px] text-near-black placeholder:text-secondary-gray"
        />
        {showSuggestions && suggestions.length > 0 && (
          <div className="absolute top-full left-0 right-0 bg-white rounded-[16px] shadow-[rgba(0,0,0,0.12)_0px_8px_24px] z-50 mt-2 overflow-hidden">
            {suggestions.map(c => (
              <div
                key={c}
                onMouseDown={() => { setCity(c); setShowSuggestions(false); }}
                className="flex items-center gap-2.5 px-5 py-2.5 text-[14px] text-near-black cursor-pointer hover:bg-light-surface"
              >
                <span>📍</span>{c}, Algeria
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Check-in */}
      <div className="flex-1 px-5 py-3.5 border-r border-border-gray min-w-0">
        <div className="text-[11px] font-bold tracking-wider text-near-black mb-1">CHECK-IN</div>
        <input
          type="date"
          value={checkIn}
          onChange={e => setCheckIn(e.target.value)}
          className="w-full bg-transparent outline-none text-[14px] text-near-black"
          style={{ colorScheme: 'light' }}
        />
      </div>

      {/* Check-out */}
      <div className="flex-1 px-5 py-3.5 border-r border-border-gray min-w-0">
        <div className="text-[11px] font-bold tracking-wider text-near-black mb-1">CHECK-OUT</div>
        <input
          type="date"
          value={checkOut}
          onChange={e => setCheckOut(e.target.value)}
          className="w-full bg-transparent outline-none text-[14px] text-near-black"
          style={{ colorScheme: 'light' }}
        />
      </div>

      {/* Guests */}
      <div className="flex-1 px-5 py-3.5 border-r border-border-gray min-w-[130px]">
        <div className="text-[11px] font-bold tracking-wider text-near-black mb-1">GUESTS</div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setGuests(g => Math.max(1, g - 1))}
            className="w-6 h-6 rounded-full border border-border-gray flex items-center justify-center text-near-black text-sm hover:border-near-black transition-colors"
          >−</button>
          <span className="text-[14px] font-semibold text-near-black min-w-[16px] text-center">{guests}</span>
          <button
            type="button"
            onClick={() => setGuests(g => g + 1)}
            className="w-6 h-6 rounded-full border border-border-gray flex items-center justify-center text-near-black text-sm hover:border-near-black transition-colors"
          >+</button>
        </div>
      </div>

      {/* Search button */}
      <div className="flex items-center p-2">
        <button
          type="button"
          onClick={handleSearch}
          className="bg-rausch hover:bg-rausch-dark text-white rounded-[24px] flex items-center gap-2 px-6 py-3 font-bold text-[14px] transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <span>Search</span>
        </button>
      </div>
    </div>
  );
}
