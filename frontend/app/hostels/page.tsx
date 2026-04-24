import { hostels } from '@/lib/mock-data';
import SearchBar from '@/components/SearchBar';
import HostelGrid from '@/components/HostelGrid';

type Props = {
  searchParams: Promise<{ city?: string; checkIn?: string; checkOut?: string; guests?: string }>;
};

export default async function HostelsPage({ searchParams }: Props) {
  const params = await searchParams;
  const city = params.city || '';
  const checkIn = params.checkIn || '';
  const checkOut = params.checkOut || '';
  const guests = Number(params.guests) || 1;

  const matchedCity = hostels.find(h => h.city.toLowerCase() === city.toLowerCase())?.city;

  return (
    <div className="page-shell py-8">
      <h1 className="text-[32px] font-bold text-near-black tracking-tight mb-6">
        {matchedCity ? `Hostels in ${matchedCity}` : 'All Hostels'}
      </h1>

      <div className="mb-8">
        <SearchBar
          initialCity={city}
          initialCheckIn={checkIn}
          initialCheckOut={checkOut}
          initialGuests={guests}
        />
      </div>

      <p className="text-[14px] text-secondary-gray mb-4">
        {hostels.length} hostel{hostels.length !== 1 ? 's' : ''} available across Algeria
      </p>

      <HostelGrid hostels={hostels} initialCity={matchedCity || 'all'} />
    </div>
  );
}
