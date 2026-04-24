import Link from "next/link";

export default function ForgotPasswordPage() {
  return (
    <div className="page-shell py-10">
      <div className="mx-auto max-w-lg rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h1 className="text-[28px] font-semibold text-near-black">Reset password</h1>
        <p className="mt-1 text-[14px] text-secondary-gray">
          Enter your account email and we&apos;ll send a reset link.
        </p>
        <form className="mt-6 grid gap-4">
          <input type="email" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Email address" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch transition-colors">
            Send reset link
          </button>
        </form>
        <p className="mt-4 text-[14px] text-secondary-gray">
          Back to{" "}
          <Link href="/login" className="font-semibold text-rausch hover:underline">
            login
          </Link>
        </p>
      </div>
    </div>
  );
}
