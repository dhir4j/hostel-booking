import Link from "next/link";
import { notFound } from "next/navigation";
import { getHostelById, getRoomsByHostelId } from "@/lib/mock-data";
import { formatCurrency } from "@/lib/format";

type BookingPageProps = {
  params: Promise<{ hostelId: string }>;
};

export default async function BookingPage({ params }: BookingPageProps) {
  const { hostelId } = await params;
  const hostel = getHostelById(hostelId);
  if (!hostel) notFound();
  const hostelRooms = getRoomsByHostelId(hostelId);

  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Booking request</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">{hostel.name} | {hostel.city}</p>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <form className="rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
          <h2 className="text-[22px] font-semibold text-near-black">Guest and stay details</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Full name" />
            <input type="email" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Email address" />
            <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
              {hostelRooms.map((room) => (
                <option key={room.id} value={room.id}>
                  Room {room.roomNumber} | {room.capacity} guests
                </option>
              ))}
            </select>
            <input type="number" min={1} defaultValue={1} className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          </div>
          <label className="mt-4 flex items-center gap-2 text-[13px] text-secondary-gray">
            <input type="checkbox" />
            I accept cancellation and hostel rules.
          </label>
          <button type="submit" className="mt-5 h-11 rounded-airbnb-sm bg-rausch px-5 text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors">
            Submit booking request
          </button>
        </form>

        <aside className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <h3 className="text-[18px] font-semibold text-near-black">Price summary</h3>
          <p className="mt-3 text-[14px] text-secondary-gray">Base price</p>
          <p className="text-[15px] font-semibold text-near-black">{formatCurrency(hostel.fromPrice)} x 3 nights</p>
          <p className="mt-3 text-[14px] text-secondary-gray">Taxes and fee</p>
          <p className="text-[15px] font-semibold text-near-black">{formatCurrency(420)}</p>
          <div className="mt-4 border-t border-[#ececec] pt-3">
            <p className="text-[14px] text-secondary-gray">Estimated total</p>
            <p className="text-[24px] font-semibold text-near-black">{formatCurrency(hostel.fromPrice * 3 + 420)}</p>
          </div>
          <Link href="/payment/b1" className="mt-4 inline-flex h-11 w-full items-center justify-center rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch transition-colors">
            Continue to payment
          </Link>
        </aside>
      </div>
    </div>
  );
}
