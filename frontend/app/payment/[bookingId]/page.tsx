import { notFound } from "next/navigation";
import StatusBadge from "@/components/StatusBadge";
import { getBookingById, getHostelById, payments } from "@/lib/mock-data";
import { formatCurrency, formatDate } from "@/lib/format";

type PaymentPageProps = {
  params: Promise<{ bookingId: string }>;
};

export default async function PaymentPage({ params }: PaymentPageProps) {
  const { bookingId } = await params;
  const booking = getBookingById(bookingId);
  if (!booking) notFound();
  const payment = payments.find((item) => item.bookingId === bookingId);
  const hostel = getHostelById(booking.hostelId);

  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Payment</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Complete your payment to confirm booking.</p>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1.3fr_1fr]">
        <section className="rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
          <h2 className="text-[22px] font-semibold text-near-black">Payment method</h2>
          <div className="mt-4 grid gap-3">
            <label className="flex items-center gap-2 rounded-airbnb-sm border border-[#d9d9d9] p-3 text-[14px]">
              <input type="radio" name="provider" defaultChecked />
              Local card gateway
            </label>
            <label className="flex items-center gap-2 rounded-airbnb-sm border border-[#d9d9d9] p-3 text-[14px]">
              <input type="radio" name="provider" />
              Stripe
            </label>
            <label className="flex items-center gap-2 rounded-airbnb-sm border border-[#d9d9d9] p-3 text-[14px]">
              <input type="radio" name="provider" />
              Mock payment (test)
            </label>
          </div>
          <button className="mt-5 h-11 rounded-airbnb-sm bg-rausch px-5 text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors">
            Pay {formatCurrency(booking.totalAmount)}
          </button>
        </section>

        <aside className="rounded-airbnb-card bg-white p-5 shadow-airbnb-card">
          <h3 className="text-[18px] font-semibold text-near-black">Booking summary</h3>
          <p className="mt-2 text-[14px] text-secondary-gray">{hostel?.name}</p>
          <p className="text-[13px] text-secondary-gray">
            {formatDate(booking.checkIn)} - {formatDate(booking.checkOut)}
          </p>
          <p className="mt-3 text-[14px] text-secondary-gray">Amount</p>
          <p className="text-[20px] font-semibold text-near-black">{formatCurrency(booking.totalAmount)}</p>
          <div className="mt-3 flex items-center gap-2">
            <span className="text-[13px] text-secondary-gray">Status:</span>
            {payment ? <StatusBadge status={payment.status} /> : <span className="text-[13px] text-secondary-gray">Not initiated</span>}
          </div>
        </aside>
      </div>
    </div>
  );
}
