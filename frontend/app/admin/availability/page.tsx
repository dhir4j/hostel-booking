import { rooms } from "@/lib/mock-data";

export default function AdminAvailabilityPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Availability control</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Block or unblock room inventory by date range.</p>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">Create availability block</h2>
        <form className="mt-4 grid gap-3 md:grid-cols-2">
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                Room {room.roomNumber} ({room.hostelId})
              </option>
            ))}
          </select>
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Reason (maintenance, hold, etc.)" />
          <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch hover:text-white md:col-span-2">
            Block room dates
          </button>
        </form>
      </section>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">Active blocks</h2>
        <div className="mt-4 space-y-3">
          <div className="flex flex-col gap-2 rounded-airbnb-sm border border-[#ececec] p-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-[15px] font-semibold text-near-black">Room 401 (h4)</p>
              <p className="text-[13px] text-secondary-gray">May 12, 2026 - May 15, 2026 | Maintenance</p>
            </div>
            <button className="rounded-airbnb-sm border border-near-black px-4 py-2 text-[13px] font-semibold text-near-black hover:bg-near-black hover:text-white transition-colors">
              Unblock
            </button>
          </div>
          <div className="flex flex-col gap-2 rounded-airbnb-sm border border-[#ececec] p-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-[15px] font-semibold text-near-black">Room 201 (h2)</p>
              <p className="text-[13px] text-secondary-gray">Apr 28, 2026 - Apr 30, 2026 | Private hold</p>
            </div>
            <button className="rounded-airbnb-sm border border-near-black px-4 py-2 text-[13px] font-semibold text-near-black hover:bg-near-black hover:text-white transition-colors">
              Unblock
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
