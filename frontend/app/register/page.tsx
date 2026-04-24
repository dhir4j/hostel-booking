import Link from "next/link";

export default function RegisterPage() {
  return (
    <div className="page-shell py-10">
      <div className="mx-auto max-w-xl rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h1 className="text-[28px] font-semibold text-near-black">Create your account</h1>
        <p className="mt-1 text-[14px] text-secondary-gray">Register to book hostels and track payments.</p>
        <form className="mt-6 grid gap-4">
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Full name" />
          <input type="email" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Email address" />
          <input className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Phone number (optional)" />
          <input type="password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Password" />
          <input type="password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Confirm password" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-rausch text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors">
            Create account
          </button>
        </form>
        <p className="mt-4 text-[14px] text-secondary-gray">
          Already registered?{" "}
          <Link href="/login" className="font-semibold text-rausch hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
