import Link from "next/link";

type ResetPasswordProps = {
  params: Promise<{ token: string }>;
};

export default async function ResetPasswordPage({ params }: ResetPasswordProps) {
  const { token } = await params;

  return (
    <div className="page-shell py-10">
      <div className="mx-auto max-w-lg rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
        <h1 className="text-[28px] font-semibold text-near-black">Create a new password</h1>
        <p className="mt-1 text-[14px] text-secondary-gray">Use a strong password. Reset token: {token.slice(0, 10)}...</p>
        <form className="mt-6 grid gap-4">
          <input type="password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="New password" />
          <input type="password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" placeholder="Confirm new password" />
          <button type="submit" className="h-11 rounded-airbnb-sm bg-rausch text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors">
            Update password
          </button>
        </form>
        <p className="mt-4 text-[14px] text-secondary-gray">
          Return to{" "}
          <Link href="/login" className="font-semibold text-rausch hover:underline">
            login
          </Link>
        </p>
      </div>
    </div>
  );
}
