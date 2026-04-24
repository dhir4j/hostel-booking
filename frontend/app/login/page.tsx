import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="page-shell py-10">
      <div className="mx-auto max-w-lg rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h1 className="text-[28px] font-semibold text-near-black">Welcome back</h1>
        <p className="mt-1 text-[14px] text-secondary-gray">Log in to continue your bookings.</p>
        <form className="mt-6 grid gap-4">
          <input type="email" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Email address" />
          <input type="password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Password" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch transition-colors">
            Login
          </button>
        </form>
        <div className="mt-4 flex items-center justify-between text-[14px]">
          <Link href="/forgot-password" className="text-rausch hover:underline">
            Forgot password?
          </Link>
          <Link href="/register" className="font-semibold text-near-black hover:underline">
            Create account
          </Link>
        </div>
      </div>
    </div>
  );
}
