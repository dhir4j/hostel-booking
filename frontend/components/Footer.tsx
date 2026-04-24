import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-light-surface border-t border-border-gray mt-12">
      <div className="max-w-[2520px] mx-auto px-6 sm:px-10 md:px-20 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-sm font-semibold text-near-black mb-4">Support</h3>
            <ul className="space-y-3">
              <li><Link href="#" className="text-sm text-near-black hover:underline">Help Center</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Safety information</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Cancellation options</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Contact us</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-near-black mb-4">Community</h3>
            <ul className="space-y-3">
              <li><Link href="#" className="text-sm text-near-black hover:underline">About us</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Newsroom</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Careers</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Investors</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-near-black mb-4">Hosting</h3>
            <ul className="space-y-3">
              <li><Link href="/admin" className="text-sm text-near-black hover:underline">Become a Host</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Host resources</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Community forum</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Hosting responsibly</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-near-black mb-4">Legal</h3>
            <ul className="space-y-3">
              <li><Link href="#" className="text-sm text-near-black hover:underline">Terms of Service</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Privacy Policy</Link></li>
              <li><Link href="#" className="text-sm text-near-black hover:underline">Cookie Policy</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border-gray mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-secondary-gray">
            © 2026 Sahil Bay Hostel. All rights reserved.
          </div>
          <div className="flex gap-6">
            <Link href="#" className="text-sm text-near-black hover:underline">English (AZ)</Link>
            <Link href="#" className="text-sm text-near-black hover:underline">DA Dinar</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
