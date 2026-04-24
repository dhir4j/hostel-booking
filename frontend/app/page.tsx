import Link from 'next/link';
import { featuredHostels } from '@/lib/mock-data';
import HostelCard from '@/components/HostelCard';
import SearchBar from '@/components/SearchBar';

const MOSAIC_ITEMS = [
  { image: 'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=900', label: 'Algiers Medina', sub: 'From 4,800 DA/night', span: 2, h: 200 },
  { image: 'https://images.pexels.com/photos/1134176/pexels-photo-1134176.jpeg?auto=compress&cs=tinysrgb&w=600', label: 'Saharan Oasis', sub: 'From 6,500 DA/night', span: 1, h: 160 },
  { image: 'https://images.pexels.com/photos/338504/pexels-photo-338504.jpeg?auto=compress&cs=tinysrgb&w=600', label: 'Mediterranean Coast', sub: 'From 5,200 DA/night', span: 1, h: 160 },
];

const DESTINATIONS = [
  { city: 'Algiers', count: '62 hostels', image: 'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=400' },
  { city: 'Oran', count: '38 hostels', image: 'https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg?auto=compress&cs=tinysrgb&w=400' },
  { city: 'Constantine', count: '24 hostels', image: 'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=400' },
  { city: 'Annaba', count: '18 hostels', image: 'https://images.pexels.com/photos/1579253/pexels-photo-1579253.jpeg?auto=compress&cs=tinysrgb&w=400' },
  { city: 'Tlemcen', count: '16 hostels', image: 'https://images.pexels.com/photos/2029722/pexels-photo-2029722.jpeg?auto=compress&cs=tinysrgb&w=400' },
  { city: 'Ghardaïa', count: '12 hostels', image: 'https://images.pexels.com/photos/1134176/pexels-photo-1134176.jpeg?auto=compress&cs=tinysrgb&w=400' },
];

const HOW_IT_WORKS = [
  { step: '01', title: 'Search & Discover', desc: 'Browse hostels by city, travel dates, and budget. Filter by type and amenities.' },
  { step: '02', title: 'Book Instantly', desc: 'Select your room, confirm your dates, and submit your booking in minutes.' },
  { step: '03', title: 'Pay Securely', desc: 'Complete secure payment with full booking confirmation sent to your email.' },
];

const STATS = [
  { num: '400+', label: 'Verified Hostels' },
  { num: '18K+', label: 'Happy Guests' },
  { num: '4.87★', label: 'Avg Rating' },
];

export default function HomePage() {
  return (
    <>
      {/* ── Hero ── */}
      <section className="max-w-[1280px] mx-auto px-6 pt-14 flex flex-col lg:flex-row items-center gap-12">
        <div className="flex-1 max-w-[580px]">
          <h1 className="text-[clamp(36px,5vw,60px)] font-extrabold text-near-black leading-[1.08] tracking-[-1.5px] mb-5">
            Your bed awaits<br />
            <span className="text-rausch">across Algeria.</span>
          </h1>
          <p className="text-lg text-secondary-gray leading-relaxed max-w-[460px] mb-10">
            Dorm beds, private rooms, and social spaces — hand-picked hostels in every corner of Algeria. Meet fellow travellers, spend less, experience more.
          </p>
          <div className="flex flex-wrap gap-3 mb-10">
            <Link
              href="/hostels"
              className="bg-rausch text-white rounded-airbnb-sm px-7 py-3.5 text-[15px] font-bold hover:bg-rausch-dark transition-colors"
            >
              Explore Hostels
            </Link>
            <Link
              href="/register"
              className="text-near-black border border-border-gray rounded-airbnb-sm px-7 py-3.5 text-[15px] font-semibold hover:bg-light-surface transition-colors"
            >
              Create account
            </Link>
          </div>
          <div className="flex gap-9">
            {STATS.map(b => (
              <div key={b.label}>
                <div className="text-[22px] font-extrabold text-near-black tracking-tight">{b.num}</div>
                <div className="text-[12px] text-secondary-gray font-medium mt-0.5">{b.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Photo mosaic */}
        <div className="hidden lg:grid flex-1 grid-cols-2 gap-3 max-w-[520px]">
          {MOSAIC_ITEMS.map((img, i) => (
            <div
              key={i}
              className="relative overflow-hidden transition-transform hover:scale-[1.02] cursor-pointer"
              style={{
                borderRadius: i === 0 ? 20 : 16,
                height: img.h,
                gridColumn: `span ${img.span}`,
              }}
            >
              <img src={img.image} alt={img.label} className="absolute inset-0 w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
              <div className="absolute bottom-3 left-3">
                <div className="text-white font-bold text-[14px] [text-shadow:0_1px_4px_rgba(0,0,0,0.3)]">{img.label}</div>
                <div className="text-[12px] mt-0.5" style={{ color: 'rgba(255,255,255,0.85)' }}>{img.sub}</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Search bar ── */}
      <div className="max-w-[1100px] mx-auto px-6 mt-10 mb-14">
        <SearchBar />
      </div>

      {/* ── Featured hostels ── */}
      <section className="max-w-[1280px] mx-auto px-6 mb-16">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-[24px] font-bold text-near-black tracking-tight">Featured hostels</h2>
          <Link href="/hostels" className="text-[14px] font-semibold text-near-black underline hover:text-secondary-gray transition-colors">
            View all
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {featuredHostels.map(h => (
            <HostelCard key={h.id} hostel={h} />
          ))}
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="border-y border-border-gray py-20 px-6">
        <div className="max-w-[1100px] mx-auto">
          <div className="flex flex-col md:flex-row md:items-end gap-3 mb-16">
            <h2 className="text-[28px] font-bold text-near-black tracking-tight shrink-0">
              How it works
            </h2>
            <div className="hidden md:block flex-1 h-px bg-border-gray mb-1" />
            <p className="text-secondary-gray text-[14px] shrink-0">
              Three steps to your perfect stay
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-border-gray">
            {HOW_IT_WORKS.map(s => (
              <div key={s.step} className="py-8 md:py-0 md:px-10 first:md:pl-0 last:md:pr-0">
                <div className="text-rausch font-black leading-none mb-4 select-none" style={{ fontSize: 48, letterSpacing: '-2px' }}>
                  {s.step}
                </div>
                <h3 className="text-[16px] font-bold text-near-black tracking-tight mb-3">
                  {s.title}
                </h3>
                <p className="text-[14px] text-secondary-gray leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Popular destinations ── */}
      <section className="max-w-[1280px] mx-auto px-6 py-16">
        <h2 className="text-[26px] font-bold text-near-black tracking-tight mb-1">Popular destinations</h2>
        <p className="text-secondary-gray text-[14px] mb-8">Top cities travellers are booking right now</p>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {DESTINATIONS.map(d => (
            <Link
              key={d.city}
              href={`/hostels?city=${d.city}`}
              className="group relative rounded-2xl overflow-hidden h-[160px] block"
            >
              <img src={d.image} alt={d.city} className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-3">
                <div className="text-white font-bold text-[15px] leading-tight">{d.city}</div>
                <div className="text-[11px] text-white/70 mt-0.5">{d.count}</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="bg-near-black py-20 px-6">
        <div className="max-w-[580px] mx-auto text-center">
          <h2 className="text-[clamp(28px,4vw,44px)] font-extrabold text-white tracking-[-1px] leading-[1.15] mb-4">
            Ready to explore Algeria?
          </h2>
          <p className="text-[16px] mb-10 leading-relaxed" style={{ color: 'rgba(255,255,255,0.65)' }}>
            Join 18,000+ travellers discovering Algeria's hidden gems with Sahil Bay.
          </p>
          <div className="flex gap-3 justify-center flex-wrap">
            <Link
              href="/register"
              className="bg-rausch text-white rounded-airbnb-sm px-9 py-4 text-[16px] font-bold hover:bg-rausch-dark transition-colors"
            >
              Create free account
            </Link>
            <Link
              href="/login"
              className="text-white border rounded-airbnb-sm px-9 py-4 text-[16px] font-semibold hover:bg-white/10 transition-colors"
              style={{ borderColor: 'rgba(255,255,255,0.3)' }}
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
