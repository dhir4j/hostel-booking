import StatusBadge from "@/components/StatusBadge";
import { payments } from "@/lib/mock-data";
import { formatCurrency, formatDate } from "@/lib/format";

export default function AdminPaymentsPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Payment management</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Monitor transaction status and run reconcile/refund actions.</p>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <div className="grid gap-3 md:grid-cols-4">
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
            <option>All providers</option>
            <option>local_gateway</option>
            <option>stripe</option>
            <option>mock</option>
          </select>
          <select className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3">
            <option>All statuses</option>
            <option>pending</option>
            <option>success</option>
            <option>failed</option>
            <option>refunded</option>
          </select>
          <input type="date" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
          <button className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch hover:text-white">Filter</button>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="min-w-full text-left text-[14px]">
            <thead className="border-b border-[#ebebeb] text-[12px] uppercase text-secondary-gray">
              <tr>
                <th className="py-3">Payment ID</th>
                <th className="py-3">Booking ID</th>
                <th className="py-3">Provider</th>
                <th className="py-3">Amount</th>
                <th className="py-3">Status</th>
                <th className="py-3">Created</th>
                <th className="py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((payment) => (
                <tr key={payment.id} className="border-b border-[#f1f1f1]">
                  <td className="py-3 font-medium text-near-black">{payment.id}</td>
                  <td className="py-3 text-secondary-gray">{payment.bookingId}</td>
                  <td className="py-3 text-secondary-gray">{payment.provider}</td>
                  <td className="py-3 font-medium text-near-black">{formatCurrency(payment.amount)}</td>
                  <td className="py-3"><StatusBadge status={payment.status} /></td>
                  <td className="py-3 text-secondary-gray">{formatDate(payment.createdAt)}</td>
                  <td className="py-3">
                    <div className="flex gap-2">
                      <button className="rounded-airbnb-sm bg-light-surface px-3 py-1 text-[12px] font-semibold text-near-black">Reconcile</button>
                      <button className="rounded-airbnb-sm bg-red-50 px-3 py-1 text-[12px] font-semibold text-red-700">Refund</button>
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
