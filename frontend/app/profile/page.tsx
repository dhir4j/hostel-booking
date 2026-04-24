export default function ProfilePage() {
  return (
    <div className="page-shell py-8">
      <h1 className="text-[30px] font-semibold text-near-black">Profile management</h1>
      <p className="mt-1 text-[14px] text-secondary-gray">Update account details and password.</p>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <section className="rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
          <h2 className="text-[22px] font-semibold text-near-black">Personal details</h2>
          <form className="mt-4 grid gap-3">
            <input defaultValue="Priya Sharma" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <input defaultValue="priya@example.com" type="email" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <input defaultValue="+994 50 123 45 67" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <button type="submit" className="h-11 rounded-airbnb-sm bg-near-black text-[14px] font-semibold text-white hover:bg-rausch transition-colors">
              Save profile
            </button>
          </form>
        </section>

        <section className="rounded-airbnb-card bg-white p-6 shadow-airbnb-card">
          <h2 className="text-[22px] font-semibold text-near-black">Password & security</h2>
          <form className="mt-4 grid gap-3">
            <input type="password" placeholder="Current password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <input type="password" placeholder="New password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <input type="password" placeholder="Confirm new password" className="h-11 rounded-airbnb-sm border border-[#d9d9d9] px-3" />
            <button type="submit" className="h-11 rounded-airbnb-sm bg-rausch text-[14px] font-semibold text-white hover:bg-rausch-dark transition-colors">
              Update password
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}
