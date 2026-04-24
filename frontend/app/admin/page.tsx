import Link from "next/link";
import { analytics } from "@/lib/mock-data";
import { formatCurrency } from "@/lib/format";

export default function AdminOverviewPage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Admin panel</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Manage hostels, rooms, bookings, payments, and availability.</p>

      <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Total bookings</p>
          <p className="mt-2 text-[22px] font-semibold text-near-black">{analytics.totalBookings}</p>
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Monthly revenue</p>
          <p className="mt-2 text-[22px] font-semibold text-near-black">{formatCurrency(analytics.monthlyRevenue)}</p>
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Occupancy rate</p>
          <p className="mt-2 text-[22px] font-semibold text-near-black">{analytics.occupancyRate}%</p>
        </div>
        <div className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <p className="text-[12px] uppercase tracking-[0.3px] text-secondary-gray">Pending approvals</p>
          <p className="mt-2 text-[22px] font-semibold text-near-black">{analytics.pendingApprovals}</p>
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <Link href="/admin/bookings" className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card hover:bg-light-surface">
          <h2 className="text-[18px] font-semibold text-near-black">Booking management</h2>
          <p className="mt-1 text-[14px] text-secondary-gray">Approve, reject, and track check-in/check-out.</p>
        </Link>
        <Link href="/admin/payments" className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card hover:bg-light-surface">
          <h2 className="text-[18px] font-semibold text-near-black">Payment management</h2>
          <p className="mt-1 text-[14px] text-secondary-gray">Review statuses, reconcile, and handle refunds.</p>
        </Link>
      </div>
    </div>
  );
}
