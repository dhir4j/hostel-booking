import { analytics } from "@/lib/mock-data";
import { formatCurrency } from "@/lib/format";

export default function AdminAnalyticsPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Admin analytics</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Booking, revenue, and occupancy snapshots.</p>

      <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Total bookings</p>
          <p className="mt-2 text-[24px] font-semibold text-near-black">{analytics.totalBookings}</p>
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Revenue (MTD)</p>
          <p className="mt-2 text-[24px] font-semibold text-near-black">{formatCurrency(analytics.monthlyRevenue)}</p>
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Occupancy</p>
          <p className="mt-2 text-[24px] font-semibold text-near-black">{analytics.occupancyRate}%</p>
        </div>
      </div>

      <section className="mt-6 rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h2 className="text-[20px] font-semibold text-near-black">Operational queue</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div className="rounded-airbnb-sm border border-[#ececec] p-4">
            <p className="text-[13px] text-secondary-gray">Pending approvals</p>
            <p className="text-[20px] font-semibold text-near-black">{analytics.pendingApprovals}</p>
          </div>
          <div className="rounded-airbnb-sm border border-[#ececec] p-4">
            <p className="text-[13px] text-secondary-gray">Payment failures</p>
            <p className="text-[20px] font-semibold text-near-black">{analytics.paymentFailures}</p>
          </div>
        </div>
      </section>
    </div>
  );
}
