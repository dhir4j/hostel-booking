"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/admin", label: "Overview" },
  { href: "/admin/hostels", label: "Hostels" },
  { href: "/admin/rooms", label: "Rooms" },
  { href: "/admin/bookings", label: "Bookings" },
  { href: "/admin/payments", label: "Payments" },
  { href: "/admin/availability", label: "Availability" },
  { href: "/admin/analytics", label: "Analytics" },
];

export default function AdminNav() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-20 z-40 mb-6 overflow-x-auto border-b border-[#ebebeb] bg-white">
      <div className="page-shell flex min-w-max gap-2 py-3">
        {links.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-full px-4 py-2 text-[13px] font-medium transition-colors ${
                isActive
                  ? "bg-near-black !text-white"
                  : "bg-light-surface text-near-black hover:bg-near-black hover:text-white"
              }`}
            >
              {link.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
