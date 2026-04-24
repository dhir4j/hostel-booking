import Link from "next/link";
import StatusBadge from "@/components/StatusBadge";
import { bookings, hostels } from "@/lib/mock-data";
import { formatCurrency, formatDate } from "@/lib/format";

export default function BookingsPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Booking history</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Track each booking lifecycle and payment action.</p>

      <div className="mt-6 space-y-4">
        {bookings.map((booking) => {
          const hostel = hostels.find((item) => item.id === booking.hostelId);
          return (
            <article key={booking.id} className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-[18px] font-semibold text-near-black">{hostel?.name}</p>
                  <p className="mt-1 text-[13px] text-secondary-gray">
                    {formatDate(booking.checkIn)} - {formatDate(booking.checkOut)} | {booking.guestsCount} guests
                  </p>
                  <p className="mt-1 text-[13px] text-secondary-gray">Booking ID: {booking.id}</p>
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  <StatusBadge status={booking.status} />
                  <p className="text-[15px] font-semibold text-near-black">{formatCurrency(booking.totalAmount)}</p>
                  <Link href={`/payment/${booking.id}`} className="rounded-airbnb-sm border border-near-black px-4 py-2 text-[13px] font-semibold text-near-black hover:bg-near-black hover:!text-white">
                    Payment
                  </Link>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
