import { Bell, Search, UserCircle2 } from "lucide-react";

export default function Navbar() {
  return (
    <header className="h-20 bg-white border-b border-slate-200 px-8 flex items-center justify-between">

      <div>
        <h2 className="text-2xl font-bold text-slate-900">
          Dashboard
        </h2>

        <p className="text-slate-500 text-sm">
          Welcome back 👋
        </p>
      </div>

      <div className="flex items-center gap-5">

        <div className="relative">
          <Search
            size={18}
            className="absolute left-3 top-3 text-slate-400"
          />

          <input
            placeholder="Search..."
            className="
              pl-10
              pr-4
              py-2
              rounded-xl
              border
              border-slate-300
              focus:outline-none
              focus:ring-2
              focus:ring-blue-500
            "
          />
        </div>

        <Bell className="cursor-pointer" />

        <UserCircle2 size={34} />
      </div>
    </header>
  );
}