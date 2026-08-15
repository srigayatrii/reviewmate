import { useEffect, useState } from "react";
import {
  GitPullRequest,
  ExternalLink,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import Layout from "../../components/layout/Layout";
import { getPullRequests } from "../../services/pullRequestService";

export default function PullRequests() {
  const [pullRequests, setPullRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    loadPullRequests();
  }, []);

  async function loadPullRequests() {
    try {
      const data = await getPullRequests();

      console.log("Pull Requests:", data);

      setPullRequests(data);
    } catch (error) {
      console.error("Pull request error:", error);
      setError("Failed to load pull requests.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">
          Pull Requests
        </h1>

        <p className="text-slate-500 mt-2">
          Review and analyze your pull requests
        </p>
      </div>

      {loading && (
        <p className="text-slate-500">
          Loading pull requests...
        </p>
      )}

      {error && (
        <p className="text-red-500">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="space-y-4">
          {pullRequests.map((pr) => (
            <div
              key={pr.id}
              onClick={() => navigate(`/pull-requests/${pr.id}`)}
              className="
                bg-white
                border
                border-slate-200
                rounded-2xl
                p-6
                shadow-sm
                hover:shadow-md
                transition
                cursor-pointer
              "
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex gap-4">
                  <div className="w-11 h-11 rounded-xl bg-blue-50 flex items-center justify-center">
                    <GitPullRequest
                      className="text-blue-600"
                      size={22}
                    />
                  </div>

                  <div>
                    <h2 className="text-lg font-semibold text-slate-900">
                      {pr.title}
                    </h2>

                    <p className="text-sm text-slate-500 mt-1">
                      PR #{pr.pr_number}
                    </p>
                  </div>
                </div>

                <span className="text-xs px-3 py-1 rounded-full bg-green-50 text-green-600">
                  Open
                </span>
              </div>

              <div className="flex items-center justify-between mt-6">
                <p className="text-sm text-slate-500">
                  Created{" "}
                  {new Date(pr.created_at).toLocaleDateString()}
                </p>

                {pr.html_url && (
                  <a
                    href={pr.html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700"
                  >
                    View on GitHub
                    <ExternalLink size={15} />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}