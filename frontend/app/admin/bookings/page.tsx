import StatusBadge from "@/components/StatusBadge";
import { bookings, hostels } from "@/lib/mock-data";
import { formatCurrency, formatDate } from "@/lib/format";

export default function AdminBookingsPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Booking management</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Accept/reject requests and update check-in/check-out events.</p>

      <div className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <div className="grid gap-3 md:grid-cols-4">
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
            <option>All statuses</option>
            <option>pending_admin_approval</option>
            <option>awaiting_payment</option>
            <option>confirmed</option>
          </select>
          <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          <button className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch hover:text-white">Filter</button>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="min-w-full text-left text-[14px]">
            <thead className="border-b border-[#ebebeb] text-[12px] uppercase text-secondary-gray">
              <tr>
                <th className="py-3">Booking</th>
                <th className="py-3">Guest</th>
                <th className="py-3">Dates</th>
                <th className="py-3">Status</th>
                <th className="py-3">Amount</th>
                <th className="py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map((booking) => (
                <tr key={booking.id} className="border-b border-[#f1f1f1]">
                  <td className="py-3 font-medium text-near-black">{hostels.find((hostel) => hostel.id === booking.hostelId)?.name}</td>
                  <td className="py-3 text-secondary-gray">{booking.userName}</td>
                  <td className="py-3 text-secondary-gray">
                    {formatDate(booking.checkIn)} - {formatDate(booking.checkOut)}
                  </td>
                  <td className="py-3"><StatusBadge status={booking.status} /></td>
                  <td className="py-3 font-medium text-near-black">{formatCurrency(booking.totalAmount)}</td>
                  <td className="py-3">
                    <div className="flex flex-wrap gap-2">
                      <button className="rounded-airbnb-sm bg-emerald-50 px-3 py-1 text-[12px] font-semibold text-emerald-700">Accept</button>
                      <button className="rounded-airbnb-sm bg-red-50 px-3 py-1 text-[12px] font-semibold text-red-700">Reject</button>
                      <button className="rounded-airbnb-sm bg-light-surface px-3 py-1 text-[12px] font-semibold text-near-black">Check-in</button>
                      <button className="rounded-airbnb-sm bg-light-surface px-3 py-1 text-[12px] font-semibold text-near-black">Check-out</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
