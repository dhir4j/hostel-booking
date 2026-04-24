import Link from "next/link";
import StatusBadge from "@/components/StatusBadge";
import { bookings, hostels, payments } from "@/lib/mock-data";
import { formatCurrency, formatDate } from "@/lib/format";

export default function DashboardPage() {
  const upcoming = bookings[0];
  const pendingPayment = payments.find((payment) => payment.status === "pending");
  const recentBookings = bookings.slice(0, 3);

  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">User dashboard</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Track upcoming stays, approvals, and payments.</p>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Upcoming booking</p>
          <p className="mt-2 text-[18px] font-semibold text-near-black">
            {upcoming ? hostels.find((hostel) => hostel.id === upcoming.hostelId)?.name : "No upcoming booking"}
          </p>
          {upcoming && (
            <p className="mt-1 text-[13px] text-secondary-gray">
              {formatDate(upcoming.checkIn)} - {formatDate(upcoming.checkOut)}
            </p>
          )}
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Pending payment</p>
          <p className="mt-2 text-[18px] font-semibold text-near-black">
            {pendingPayment ? formatCurrency(pendingPayment.amount) : "None"}
          </p>
          {pendingPayment && (
            <Link href={`/payment/${pendingPayment.bookingId}`} className="mt-2 inline-block text-[13px] font-semibold text-rausch hover:underline">
              Complete payment
            </Link>
          )}
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Total bookings</p>
          <p className="mt-2 text-[18px] font-semibold text-near-black">{bookings.length}</p>
          <Link href="/bookings" className="mt-2 inline-block text-[13px] font-semibold text-rausch hover:underline">
            View history
          </Link>
        </div>
      </div>

      <section className="mt-8 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-[22px] font-semibold text-near-black">Recent bookings</h2>
          <Link href="/bookings" className="text-[13px] font-semibold text-rausch hover:underline">
            See all
          </Link>
        </div>
        <div className="space-y-3">
          {recentBookings.map((booking) => {
            const hostel = hostels.find((item) => item.id === booking.hostelId);
            return (
              <div key={booking.id} className="flex flex-col gap-2 rounded-airbnb-sm border border-[#ececec] p-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-[15px] font-semibold text-near-black">{hostel?.name}</p>
                  <p className="text-[13px] text-secondary-gray">
                    {formatDate(booking.checkIn)} - {formatDate(booking.checkOut)} | {booking.guestsCount} guests
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge status={booking.status} />
                  <span className="text-[14px] font-semibold text-near-black">{formatCurrency(booking.totalAmount)}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
