import { BookingStatus, PaymentStatus } from "@/lib/types";

export function formatCurrency(value: number): string {
  return `${new Intl.NumberFormat("en").format(value)} DA`;
}

export function formatDate(value: string): string {
  return new Date(value).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function statusBadgeClass(status: BookingStatus | PaymentStatus): string {
  if (status === "confirmed" || status === "completed" || status === "success") {
    return "bg-emerald-50 text-emerald-700 border-emerald-200";
  }
  if (status === "pending_admin_approval" || status === "awaiting_payment" || status === "payment_pending" || status === "pending") {
    return "bg-amber-50 text-amber-700 border-amber-200";
  }
  if (status === "checked_in" || status === "checked_out") {
    return "bg-blue-50 text-blue-700 border-blue-200";
  }
  return "bg-red-50 text-red-700 border-red-200";
}

export function toLabel(value: string): string {
  return value.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}
