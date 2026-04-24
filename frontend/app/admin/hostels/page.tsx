import { hostels } from "@/lib/mock-data";

export default function AdminHostelsPage() {
  return (
    <div className="page-shell py-8">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-[30px] font-semibold text-near-black">Hostel management</h1>
          <p className="text-[14px] text-secondary-gray">Add, edit, and remove hostel listings and amenities.</p>
        </div>
        <button className="h-11 rounded-airbnb-sm bg-rausch px-5 text-[14px] font-semibold text-white hover:bg-rausch-dark hover:text-white">
          Add hostel
        </button>
      </div>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">Create / edit hostel</h2>
        <form className="mt-4 grid gap-3 md:grid-cols-2">
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Hostel name" />
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="City" />
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3 md:col-span-2" placeholder="Address" />
          <textarea className="min-h-28 rounded-airbnb-sm border border-[#d9d9d9] px-3 py-2 md:col-span-2" placeholder="Description" />
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Amenities (comma separated)" />
          <input type="file" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3 pt-2" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch hover:text-white md:col-span-2">
            Save hostel
          </button>
        </form>
      </section>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">All hostels</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-[14px]">
            <thead className="border-b border-[#ebebeb] text-[12px] uppercase text-secondary-gray">
              <tr>
                <th className="py-3">Name</th>
                <th className="py-3">City</th>
                <th className="py-3">Amenities</th>
                <th className="py-3">Status</th>
                <th className="py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {hostels.map((hostel) => (
                <tr key={hostel.id} className="border-b border-[#f1f1f1]">
                  <td className="py-3 font-medium text-near-black">{hostel.name}</td>
                  <td className="py-3 text-secondary-gray">{hostel.city}</td>
                  <td className="py-3 text-secondary-gray">{hostel.amenities.join(", ")}</td>
                  <td className="py-3">
                    <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-semibold text-emerald-700">Active</span>
                  </td>
                  <td className="py-3">
                    <div className="flex gap-2">
                      <button className="rounded-airbnb-sm border border-near-black px-3 py-1 text-[12px] font-semibold text-near-black hover:bg-near-black hover:text-white transition-colors">
                        Edit
                      </button>
                      <button className="rounded-airbnb-sm border border-red-200 px-3 py-1 text-[12px] font-semibold text-red-700 hover:bg-red-50">
                        Delete
                      </button>
                    </div>
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
