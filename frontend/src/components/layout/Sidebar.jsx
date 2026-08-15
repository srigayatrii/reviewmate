import {
  LayoutDashboard,
  FolderGit2,
  GitPullRequest,
  Bot,
  Settings,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    name: "Repositories",
    icon: FolderGit2,
    path: "/repositories",
  },
  {
    name: "Pull Requests",
    icon: GitPullRequest,
    path: "/pull-requests",
  },
  {
    name: "AI Reviews",
    icon: Bot,
    path: "/ai-reviews",
  },
  {
    name: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

export default function Sidebar() {
  const navigate = useNavigate();

  return (
    <aside className="w-72 bg-slate-900 text-white min-h-screen p-6">

      <div className="mb-12">
        <h1 className="text-3xl font-bold">
          🤖 ReviewMate
        </h1>

        <p className="text-slate-400 mt-2 text-sm">
          AI Code Reviews
        </p>
      </div>

      <nav className="space-y-3">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.name}
              onClick={() => navigate(item.path)}
              className="
                w-full
                flex
                items-center
                gap-4
                px-4
                py-3
                rounded-2xl
                hover:bg-slate-800
                transition
              "
            >
              <Icon size={20} />

              {item.name}
            </button>
          );
        })}

      </nav>

    </aside>
  );
}