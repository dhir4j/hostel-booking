import Image from "next/image";
import Link from "next/link";
import { Hostel } from "@/lib/types";
import { formatCurrency } from "@/lib/format";

type HostelCardProps = {
  hostel: Hostel;
};

export default function HostelCard({ hostel }: HostelCardProps) {
  return (
    <article className="overflow-hidden rounded-airbnb-card bg-white shadow-airbnb-card transition-transform hover:-translate-y-0.5">
      <div className="relative h-56 w-full">
        <Image
          src={hostel.coverImage}
          alt={hostel.name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 33vw"
        />
      </div>
      <div className="p-4">
        <div className="mb-1 flex items-start justify-between gap-2">
          <h3 className="text-[16px] font-semibold text-near-black">{hostel.name}</h3>
          <span className="text-[13px] font-medium text-near-black">★ {hostel.rating}</span>
        </div>
        <p className="text-[13px] text-secondary-gray">{hostel.city}</p>
        <p className="mt-1 line-clamp-2 text-[13px] text-secondary-gray">{hostel.description}</p>
        <p className="mt-3 text-[14px] text-near-black">
          <span className="font-semibold">{formatCurrency(hostel.fromPrice)}</span> night
        </p>
        <Link
          href={`/hostels/${hostel.id}`}
          className="mt-4 inline-flex rounded-airbnb-sm border border-near-black px-4 py-2 text-[13px] font-semibold text-near-black transition-colors hover:bg-near-black hover:!text-white"
        >
          View details
        </Link>
      </div>
    </article>
  );
}
