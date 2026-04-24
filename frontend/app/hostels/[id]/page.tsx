import Link from "next/link";
import Image from "next/image";
import { notFound } from "next/navigation";
import { formatCurrency } from "@/lib/format";
import { getHostelById, getRoomsByHostelId } from "@/lib/mock-data";

type HostelDetailsPageProps = {
  params: Promise<{ id: string }>;
};

export default async function HostelDetailsPage({ params }: HostelDetailsPageProps) {
  const { id } = await params;
  const hostel = getHostelById(id);
  if (!hostel) notFound();
  const hostelRooms = getRoomsByHostelId(id);

  return (
    <div className="page-shell py-8">
      <h1 className="text-[32px] font-semibold text-near-black">{hostel.name}</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">
        {hostel.city} | {hostel.address}
      </p>

      <div className="relative mt-5 h-[380px] overflow-hidden rounded-airbnb-card">
        <Image src={hostel.coverImage} alt={hostel.name} fill className="object-cover" sizes="100vw" />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <section>
          <h2 className="text-[22px] font-semibold text-near-black">About this hostel</h2>
          <p className="mt-2 text-[14px] text-secondary-gray">{hostel.description}</p>
          <h3 className="mt-5 text-[18px] font-semibold text-near-black">Amenities</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {hostel.amenities.map((amenity) => (
              <span key={amenity} className="rounded-full bg-light-surface px-3 py-1 text-[12px] font-medium text-near-black">
                {amenity}
              </span>
            ))}
          </div>
        </section>

        <aside className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[14px] text-secondary-gray">Starting from</p>
          <p className="mt-1 text-[24px] font-semibold text-near-black">{formatCurrency(hostel.fromPrice)}</p>
          <p className="text-[13px] text-secondary-gray">per night</p>
          <Link
            href={`/booking/${hostel.id}`}
            className="mt-5 inline-flex h-11 w-full items-center justify-center rounded-airbnb-sm bg-rausch text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors"
          >
            Book now
          </Link>
          <p className="mt-3 text-[12px] text-secondary-gray">Rating: ★ {hostel.rating} ({hostel.reviewCount} reviews)</p>
        </aside>
      </div>

      <section className="mt-8 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[22px] font-semibold text-near-black">Available rooms</h2>
        <div className="mt-4 space-y-3">
          {hostelRooms.map((room) => (
            <div key={room.id} className="flex flex-col gap-2 rounded-airbnb-sm border border-[#ececec] p-4 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-[15px] font-semibold text-near-black">
                  Room {room.roomNumber} | Capacity {room.capacity}
                </p>
                <p className="text-[13px] text-secondary-gray">Status: {room.availabilityStatus}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-[14px] font-semibold text-near-black">{formatCurrency(room.pricePerNight)}</span>
                <Link href={`/booking/${hostel.id}`} className="rounded-airbnb-sm bg-near-black px-4 py-2 text-[13px] font-semibold text-white hover:bg-rausch transition-colors">
                  Select
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
