import { BookingStatus, PaymentStatus } from "@/lib/types";
import { statusBadgeClass, toLabel } from "@/lib/format";

type StatusBadgeProps = {
  status: BookingStatus | PaymentStatus;
};

export default function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex rounded-full border px-2.5 py-1 text-[11px] font-semibold ${statusBadgeClass(
        status,
      )}`}
    >
      {toLabel(status)}
    </span>
  );
}
