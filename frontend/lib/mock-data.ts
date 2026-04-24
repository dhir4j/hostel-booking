import { AnalyticsSummary, Booking, Hostel, Payment, Room } from "@/lib/types";

export const hostels: Hostel[] = [
  {
    id: "h1",
    name: "Nomad Square Hostel",
    city: "Algiers",
    address: "12 Rue Didouche Mourad, Algiers",
    description: "Modern social hostel near central Algiers with cowork lounge and cafe.",
    coverImage: "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.8,
    reviewCount: 318,
    fromPrice: 49,
    amenities: ["WiFi", "AC", "Laundry", "Kitchen", "Security"],
    isFeatured: true,
  },
  {
    id: "h2",
    name: "Harborline Hostel",
    city: "Oran",
    address: "4 Corniche Avenue, Oran",
    description: "Coastal stay overlooking the Mediterranean with easy city access and 24/7 front desk.",
    coverImage: "https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.6,
    reviewCount: 242,
    fromPrice: 59,
    amenities: ["WiFi", "AC", "Breakfast", "Security"],
    isFeatured: true,
  },
  {
    id: "h3",
    name: "Backpack Base",
    city: "Constantine",
    address: "22 Rue Larbi Ben M'hidi, Constantine",
    description: "Budget-friendly property perched above the dramatic gorges of Constantine.",
    coverImage: "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.4,
    reviewCount: 187,
    fromPrice: 39,
    amenities: ["WiFi", "Laundry", "Kitchen", "Parking"],
    isFeatured: false,
  },
  {
    id: "h4",
    name: "Campus Stay Hub",
    city: "Annaba",
    address: "68 Boulevard du 1er Novembre, Annaba",
    description: "Quiet, secure stay near the Annaba corniche and Roman ruins of Hippo Regius.",
    coverImage: "https://images.pexels.com/photos/1579253/pexels-photo-1579253.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.7,
    reviewCount: 206,
    fromPrice: 45,
    amenities: ["WiFi", "AC", "Kitchen", "Security", "Parking"],
    isFeatured: true,
  },
  {
    id: "h5",
    name: "Medina Riad Hostel",
    city: "Tlemcen",
    address: "7 Rue de la Grande Mosquée, Tlemcen",
    description: "Charming riad-style hostel inside the historic medina with rooftop terrace views.",
    coverImage: "https://images.pexels.com/photos/2029722/pexels-photo-2029722.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.9,
    reviewCount: 154,
    fromPrice: 55,
    amenities: ["WiFi", "Breakfast", "Security", "AC"],
    isFeatured: true,
  },
  {
    id: "h6",
    name: "Desert Gate Hostel",
    city: "Ghardaïa",
    address: "3 Avenue des Oasis, Ghardaïa",
    description: "Gateway to the Sahara — cool courtyard, traditional architecture, and stargazing nights.",
    coverImage: "https://images.pexels.com/photos/1134176/pexels-photo-1134176.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.5,
    reviewCount: 98,
    fromPrice: 42,
    amenities: ["WiFi", "Kitchen", "Parking", "AC"],
    isFeatured: true,
  },
  {
    id: "h7",
    name: "Kasbah Collective",
    city: "Algiers",
    address: "5 Impasse Sidi Ramdane, Casbah, Algiers",
    description: "Boutique hostel inside a restored Ottoman house in the UNESCO-listed Casbah.",
    coverImage: "https://images.pexels.com/photos/2467285/pexels-photo-2467285.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.7,
    reviewCount: 211,
    fromPrice: 62,
    amenities: ["WiFi", "AC", "Breakfast", "Security"],
    isFeatured: false,
  },
  {
    id: "h8",
    name: "Blue Bay Hostel",
    city: "Béjaïa",
    address: "11 Rue de la Plage, Béjaïa",
    description: "Steps from the beach with a lively common area, hammocks, and sea-view balconies.",
    coverImage: "https://images.pexels.com/photos/338504/pexels-photo-338504.jpeg?auto=compress&cs=tinysrgb&w=800",
    rating: 4.6,
    reviewCount: 173,
    fromPrice: 52,
    amenities: ["WiFi", "AC", "Laundry", "Breakfast"],
    isFeatured: true,
  },
];

export const rooms: Room[] = [
  { id: "r1", hostelId: "h1", roomNumber: "101", capacity: 2, pricePerNight: 49, availabilityStatus: "available" },
  { id: "r2", hostelId: "h1", roomNumber: "102", capacity: 4, pricePerNight: 69, availabilityStatus: "available" },
  { id: "r3", hostelId: "h2", roomNumber: "201", capacity: 2, pricePerNight: 59, availabilityStatus: "available" },
  { id: "r4", hostelId: "h3", roomNumber: "301", capacity: 1, pricePerNight: 39, availabilityStatus: "available" },
  { id: "r5", hostelId: "h4", roomNumber: "401", capacity: 3, pricePerNight: 55, availabilityStatus: "maintenance" },
];

export const bookings: Booking[] = [
  {
    id: "b1",
    hostelId: "h1",
    roomId: "r1",
    userName: "Priya Sharma",
    checkIn: "2026-04-24",
    checkOut: "2026-04-27",
    guestsCount: 2,
    totalAmount: 147,
    status: "awaiting_payment",
  },
  {
    id: "b2",
    hostelId: "h2",
    roomId: "r3",
    userName: "Arjun Singh",
    checkIn: "2026-05-02",
    checkOut: "2026-05-05",
    guestsCount: 2,
    totalAmount: 177,
    status: "pending_admin_approval",
  },
  {
    id: "b3",
    hostelId: "h4",
    roomId: "r5",
    userName: "Neha Rao",
    checkIn: "2026-04-19",
    checkOut: "2026-04-22",
    guestsCount: 1,
    totalAmount: 135,
    status: "confirmed",
  },
];

export const payments: Payment[] = [
  { id: "p1", bookingId: "b1", provider: "local_gateway", amount: 147, status: "pending", createdAt: "2026-04-19T10:30:00Z" },
  { id: "p2", bookingId: "b3", provider: "stripe", amount: 135, status: "success", createdAt: "2026-04-18T16:42:00Z" },
  { id: "p3", bookingId: "b2", provider: "mock", amount: 177, status: "failed", createdAt: "2026-04-19T08:11:00Z" },
];

export const analytics: AnalyticsSummary = {
  totalBookings: 1248,
  monthlyRevenue: 126340,
  occupancyRate: 78,
  pendingApprovals: 16,
  paymentFailures: 6,
};

export const featuredHostels = hostels.filter((hostel) => hostel.isFeatured);

export function getHostelById(hostelId: string): Hostel | undefined {
  return hostels.find((hostel) => hostel.id === hostelId);
}

export function getRoomsByHostelId(hostelId: string): Room[] {
  return rooms.filter((room) => room.hostelId === hostelId);
}

export function getBookingById(bookingId: string): Booking | undefined {
  return bookings.find((booking) => booking.id === bookingId);
}
