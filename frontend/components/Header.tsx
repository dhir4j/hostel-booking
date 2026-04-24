'use client';

import Link from 'next/link';
import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const CITIES = ['Algiers', 'Oran', 'Constantine', 'Annaba', 'Tlemcen', 'Ghardaïa', 'Tamanrasset', 'Béjaïa'];
type Section = 'where' | 'when' | 'who' | null;

export default function Header() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [active, setActive] = useState<Section>(null);
  const [city, setCity] = useState('');
  const [checkIn, setCheckIn] = useState('');
  const [checkOut, setCheckOut] = useState('');
  const [guests, setGuests] = useState(1);
  const pillRef = useRef<HTMLDivElement>(null);

  const suggestions = CITIES.filter(c => !city || c.toLowerCase().includes(city.toLowerCase()));

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (pillRef.current && !pillRef.current.contains(e.target as Node)) setActive(null);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSearch = () => {
    const params = new URLSearchParams();
    if (city) params.set('city', city);
    if (checkIn) params.set('checkIn', checkIn);
    if (checkOut) params.set('checkOut', checkOut);
    params.set('guests', String(guests));
    setActive(null);
    router.push(`/hostels?${params.toString()}`);
  };

  const whenLabel = checkIn && checkOut ? `${checkIn} → ${checkOut}` : checkIn || 'Add dates';

  const seg = (s: Section) =>
    `flex-1 px-5 py-2.5 text-left rounded-full transition-colors ${active === s ? 'bg-white shadow-sm' : 'hover:bg-[#e8e8e8]'}`;

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-[#ebebeb]">
      <div className="max-w-[2520px] mx-auto px-6 sm:px-10 md:px-20">
        <div className="flex items-center justify-between h-20">

          {/* Logo */}
          <Link href="/" className="flex items-center shrink-0">
            <span style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }} className="text-[22px] font-bold text-rausch tracking-tight">Sahil Bay Hostel</span>
          </Link>

          {/* Search Pill */}
          <div className="relative hidden md:block" ref={pillRef}>
            <div className={`flex items-center w-[480px] bg-[#f0f0f0] rounded-full border transition-all ${active ? 'border-border-gray shadow-md bg-white' : 'border-transparent'}`}>

              <button className={seg('where')} onClick={() => setActive(a => a === 'where' ? null : 'where')}>
                <div className="text-[10px] font-bold text-near-black">Where</div>
                <div className="text-sm text-secondary-gray truncate">{city || 'Search destination'}</div>
              </button>

              <span className="w-px h-6 bg-border-gray shrink-0" />

              <button className={seg('when')} onClick={() => setActive(a => a === 'when' ? null : 'when')}>
                <div className="text-[10px] font-bold text-near-black">When</div>
                <div className="text-sm text-secondary-gray truncate">{whenLabel}</div>
              </button>

              <span className="w-px h-6 bg-border-gray shrink-0" />

              <button className={`${seg('who')} pr-2`} onClick={() => setActive(a => a === 'who' ? null : 'who')}>
                <div className="text-[10px] font-bold text-near-black">Who</div>
                <div className="text-sm text-secondary-gray">{guests > 1 ? `${guests} guests` : 'Add guests'}</div>
              </button>

              <button onClick={handleSearch} className="mr-1.5 w-9 h-9 bg-rausch hover:bg-rausch-dark rounded-full flex items-center justify-center shrink-0 transition-colors">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>

            {/* Where dropdown */}
            {active === 'where' && (
              <div className="absolute top-[calc(100%+8px)] left-0 w-72 bg-white rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-border-gray p-3 z-50">
                <input
                  autoFocus
                  value={city}
                  onChange={e => setCity(e.target.value)}
                  placeholder="Search cities…"
                  className="w-full bg-[#f7f7f7] rounded-xl px-3 py-2.5 text-sm outline-none placeholder:text-secondary-gray mb-2"
                />
                {suggestions.map(c => (
                  <div key={c} onClick={() => { setCity(c); setActive('when'); }}
                    className="flex items-center gap-2 px-3 py-2.5 text-sm text-near-black hover:bg-light-surface rounded-xl cursor-pointer">
                    <span>📍</span>{c}
                  </div>
                ))}
              </div>
            )}

            {/* When dropdown */}
            {active === 'when' && (
              <div className="absolute top-[calc(100%+8px)] left-1/2 -translate-x-1/2 bg-white rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-border-gray p-4 z-50 w-64">
                <div className="mb-3">
                  <label className="text-[10px] font-bold text-secondary-gray uppercase tracking-widest block mb-1">Check-in</label>
                  <input autoFocus type="date" value={checkIn} onChange={e => setCheckIn(e.target.value)}
                    className="w-full bg-[#f7f7f7] rounded-xl px-3 py-2.5 text-sm outline-none" style={{ colorScheme: 'light' }} />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-secondary-gray uppercase tracking-widest block mb-1">Check-out</label>
                  <input type="date" value={checkOut} onChange={e => { setCheckOut(e.target.value); setActive('who'); }}
                    className="w-full bg-[#f7f7f7] rounded-xl px-3 py-2.5 text-sm outline-none" style={{ colorScheme: 'light' }} />
                </div>
              </div>
            )}

            {/* Who dropdown */}
            {active === 'who' && (
              <div className="absolute top-[calc(100%+8px)] right-0 bg-white rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-border-gray p-4 z-50 w-52">
                <p className="text-[10px] font-bold text-secondary-gray uppercase tracking-widest mb-3">Guests</p>
                <div className="flex items-center justify-between">
                  <button onClick={() => setGuests(g => Math.max(1, g - 1))}
                    className="w-8 h-8 rounded-full border border-border-gray flex items-center justify-center hover:border-near-black transition-colors text-lg">−</button>
                  <span className="text-base font-semibold">{guests}</span>
                  <button onClick={() => setGuests(g => g + 1)}
                    className="w-8 h-8 rounded-full border border-border-gray flex items-center justify-center hover:border-near-black transition-colors text-lg">+</button>
                </div>
              </div>
            )}
          </div>

          {/* Right Menu */}
          <div className="flex items-center gap-4 shrink-0">
            <Link href="/admin" className="hidden lg:block text-sm font-medium text-near-black hover:bg-light-surface px-4 py-2 rounded-[32px] transition-colors">
              Become a Host
            </Link>
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="flex items-center gap-3 border border-border-gray rounded-[32px] px-3 py-2 hover:shadow-[0_2px_4px_rgba(0,0,0,0.18)] transition-shadow relative"
            >
              <svg className="w-5 h-5 text-near-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <div className="w-8 h-8 bg-secondary-gray rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              {isMenuOpen && (
                <div className="absolute top-full right-0 mt-2 w-60 bg-white rounded-[20px] shadow-airbnb-card py-2">
                  <Link href="/login" className="block px-4 py-3 text-sm font-medium text-near-black hover:bg-light-surface">Log in</Link>
                  <Link href="/register" className="block px-4 py-3 text-sm text-near-black hover:bg-light-surface">Sign up</Link>
                  <div className="border-t border-border-gray my-2"></div>
                  <Link href="/dashboard" className="block px-4 py-3 text-sm text-near-black hover:bg-light-surface">Dashboard</Link>
                  <Link href="/bookings" className="block px-4 py-3 text-sm text-near-black hover:bg-light-surface">My Bookings</Link>
                  <Link href="/profile" className="block px-4 py-3 text-sm text-near-black hover:bg-light-surface">Profile</Link>
                </div>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Search */}
      <div className="md:hidden px-6 pb-4">
        <button className="w-full flex items-center gap-3 border border-border-gray rounded-[32px] px-4 py-3 shadow-[0_2px_4px_rgba(0,0,0,0.08)]">
          <svg className="w-5 h-5 text-near-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <div className="text-left">
            <div className="text-sm font-medium text-near-black">Where to?</div>
            <div className="text-xs text-secondary-gray">Anywhere • Any week • Add guests</div>
          </div>
        </button>
      </div>
    </header>
  );
}
