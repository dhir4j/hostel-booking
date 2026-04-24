import { hostels, rooms } from "@/lib/mock-data";
import { formatCurrency } from "@/lib/format";

export default function AdminRoomsPage() {
  return (
    <div className="page-shell py-8">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-[30px] font-semibold text-near-black">Room management</h1>
          <p className="text-[14px] text-secondary-gray">Configure capacity, pricing, and room availability status.</p>
        </div>
        <button className="h-11 rounded-airbnb-sm bg-rausch px-5 text-[14px] font-semibold text-white hover:bg-rausch-dark hover:text-white">
          Add room
        </button>
      </div>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">Create / edit room</h2>
        <form className="mt-4 grid gap-3 md:grid-cols-2">
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
            {hostels.map((hostel) => (
              <option key={hostel.id} value={hostel.id}>
                {hostel.name}
              </option>
            ))}
          </select>
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Room number" />
          <input type="number" min={1} className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Capacity" />
          <input type="number" min={0} className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Price per night" />
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3 md:col-span-2">
            <option>available</option>
            <option>unavailable</option>
            <option>maintenance</option>
          </select>
          <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch hover:text-white md:col-span-2">
            Save room
          </button>
        </form>
      </section>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">All rooms</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-[14px]">
            <thead className="border-b border-[#ebebeb] text-[12px] uppercase text-secondary-gray">
              <tr>
                <th className="py-3">Hostel</th>
                <th className="py-3">Room no.</th>
                <th className="py-3">Capacity</th>
                <th className="py-3">Price</th>
                <th className="py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {rooms.map((room) => (
                <tr key={room.id} className="border-b border-[#f1f1f1]">
                  <td className="py-3 font-medium text-near-black">{hostels.find((hostel) => hostel.id === room.hostelId)?.name}</td>
                  <td className="py-3 text-secondary-gray">{room.roomNumber}</td>
                  <td className="py-3 text-secondary-gray">{room.capacity}</td>
                  <td className="py-3 text-secondary-gray">{formatCurrency(room.pricePerNight)}</td>
                  <td className="py-3">
                    <span className="rounded-full bg-light-surface px-2.5 py-1 text-[11px] font-semibold text-near-black">{room.availabilityStatus}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
