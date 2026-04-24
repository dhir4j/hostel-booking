export type UserRole = "guest" | "user" | "admin";

export type BookingStatus =
  | "pending_admin_approval"
  | "awaiting_payment"
  | "payment_pending"
  | "confirmed"
  | "checked_in"
  | "checked_out"
  | "completed"
  | "rejected"
  | "cancelled";

export type PaymentStatus = "pending" | "success" | "failed" | "refunded";

export type Amenity =
  | "WiFi"
  | "AC"
  | "Laundry"
  | "Kitchen"
  | "Parking"
  | "Security"
  | "Breakfast"
  | "Rooftop";

export interface Room {
  id: string;
  hostelId: string;
  roomNumber: string;
  capacity: number;
  pricePerNight: number;
  availabilityStatus: "available" | "unavailable" | "maintenance";
}

export interface Hostel {
  id: string;
  name: string;
  city: string;
  address: string;
  description: string;
  coverImage: string;
  rating: number;
  reviewCount: number;
  fromPrice: number;
  amenities: Amenity[];
  isFeatured: boolean;
}

export interface Booking {
  id: string;
  hostelId: string;
  roomId: string;
  userName: string;
  checkIn: string;
  checkOut: string;
  guestsCount: number;
  totalAmount: number;
  status: BookingStatus;
}

export interface Payment {
  id: string;
  bookingId: string;
  provider: "mock" | "stripe" | "local_gateway";
  amount: number;
  status: PaymentStatus;
  createdAt: string;
}

export interface AnalyticsSummary {
  totalBookings: number;
  monthlyRevenue: number;
  occupancyRate: number;
  pendingApprovals: number;
  paymentFailures: number;
}
