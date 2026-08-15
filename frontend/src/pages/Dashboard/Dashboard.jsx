import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  IconFolder,
  IconGitPullRequest,
  IconRobot,
  IconClock,
  IconCircleCheck,
  IconAlertTriangle,
} from "@tabler/icons-react";

import Layout from "../../components/layout/Layout";
import StatCard from "../../components/ui/StatCard";
import { getDashboard } from "../../services/dashboardService";

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const data = await getDashboard();
      setDashboard(data);
    } catch (error) {
      console.error(error);
    }
  }

  if (!dashboard) {
    return (
      <Layout>
        <h2 className="text-2xl font-bold">
          Loading Dashboard...
        </h2>
      </Layout>
    );
  }

  return (
    <Layout>
      <div>

        <h1 className="text-4xl font-bold">
          Welcome back 👋
        </h1>

        <p className="text-slate-500 mt-2">
          Here's what's happening in your workspace.
        </p>

        {/* MAIN STATS */}

        <div className="grid grid-cols-4 gap-6 mt-10">

          <StatCard
            title="Repositories"
            value={dashboard.repositories}
            icon={<IconFolder size={36} />}
          />

          <StatCard
            title="Pull Requests"
            value={dashboard.pull_requests}
            icon={<IconGitPullRequest size={36} />}
          />

          <StatCard
            title="AI Reviews"
            value={dashboard.analyses}
            icon={<IconRobot size={36} />}
          />

          <StatCard
            title="Open PRs"
            value={dashboard.open_pull_requests}
            icon={<IconClock size={36} />}
          />

        </div>

        {/* REVIEW STATS */}

        <div className="grid grid-cols-2 gap-6 mt-8">

          <StatCard
            title="Completed Reviews"
            value={dashboard.completed_analyses}
            icon={<IconCircleCheck size={36} />}
          />

          <StatCard
            title="High Risk PRs"
            value={dashboard.risk_distribution.high}
            icon={<IconAlertTriangle size={36} />}
          />

        </div>

        {/* RISK DISTRIBUTION */}

        <div className="mt-8 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">

          <h2 className="text-xl font-semibold text-slate-900">
            Risk Distribution
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            AI-detected risk across analyzed pull requests
          </p>

          <div className="grid grid-cols-3 gap-4 mt-6">

            <div className="bg-red-50 rounded-xl p-5">
              <p className="text-sm text-red-600">
                High Risk
              </p>

              <p className="text-3xl font-bold text-red-700 mt-2">
                {dashboard.risk_distribution.high}
              </p>
            </div>

            <div className="bg-yellow-50 rounded-xl p-5">
              <p className="text-sm text-yellow-600">
                Medium Risk
              </p>

              <p className="text-3xl font-bold text-yellow-700 mt-2">
                {dashboard.risk_distribution.medium}
              </p>
            </div>

            <div className="bg-green-50 rounded-xl p-5">
              <p className="text-sm text-green-600">
                Low Risk
              </p>

              <p className="text-3xl font-bold text-green-700 mt-2">
                {dashboard.risk_distribution.low}
              </p>
            </div>

          </div>

        </div>

        {/* RECENT PULL REQUESTS */}


        <div className="mt-8 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">


          <h2 className="text-xl font-semibold text-slate-900">
            Recent Pull Requests
          </h2>


          <p className="text-sm text-slate-500 mt-1">
            Latest pull requests processed by ReviewMate
          </p>


          <div className="mt-6 space-y-4">


            {dashboard.recent_pull_requests.map((pr) => (
              <div
                key={pr.id}
                onClick={() => navigate(`/pull-requests/${pr.id}`)}
                className="flex items-center justify-between border border-slate-100 rounded-xl p-4 cursor-pointer hover:bg-slate-50 transition"
              >


                <div>
                  <h3 className="font-semibold text-slate-900">
                    {pr.title}
                  </h3>


                  <p className="text-sm text-slate-500 mt-1">
                    PR #{pr.pr_number} · {pr.author}
                  </p>
                </div>


                <span
                  className={`text-xs px-3 py-1 rounded-full ${
                    pr.state === "open"
                      ? "bg-green-50 text-green-600"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {pr.state}
                </span>


              </div>
            ))}


          </div>


        </div>

      </div>
    </Layout>
  );
}
