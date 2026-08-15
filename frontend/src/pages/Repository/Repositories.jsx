import { useEffect, useState } from "react";
import { FolderGit2, GitPullRequest, Star } from "lucide-react";
import Layout from "../../components/layout/Layout";
import { getRepositories } from "../../services/repositoryService";

export default function Repositories() {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadRepositories();
  }, []);

  async function loadRepositories() {
    try {
      const data = await getRepositories();
      setRepositories(data);
    } catch (error) {
      console.error("Repository error:", error);
      setError("Failed to load repositories.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Repositories
          </h1>

          <p className="text-slate-500 mt-2">
            Your GitHub repositories
          </p>
        </div>

        <button
          onClick={loadRepositories}
          className="px-5 py-3 rounded-xl bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
        >
          Refresh
        </button>
      </div>

      {loading && (
        <p className="text-slate-500">
          Loading repositories...
        </p>
      )}

      {error && (
        <p className="text-red-500">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {repositories.map((repo) => (
            <div
              key={repo.id}
              className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition"
            >
              <div className="flex items-start justify-between">
                <div className="w-11 h-11 rounded-xl bg-blue-50 flex items-center justify-center">
                  <FolderGit2 className="text-blue-600" size={22} />
                </div>

                <span className="text-xs px-3 py-1 rounded-full bg-green-50 text-green-600">
                  Active
                </span>
              </div>

              <h2 className="text-lg font-semibold text-slate-900 mt-5">
                {repo.name}
              </h2>

              <p className="text-sm text-slate-500 mt-1 truncate">
                {repo.full_name}
              </p>

              <div className="flex items-center gap-5 mt-6 text-sm text-slate-500">
                <span className="flex items-center gap-1.5">
                  <GitPullRequest size={16} />
                  PRs
                </span>

                <span className="flex items-center gap-1.5">
                  <Star size={16} />
                  GitHub
                </span>
              </div>

              <a
                href={`https://github.com/${repo.full_name}`}
                target="_blank"
                rel="noopener noreferrer"
                className="
                  block
                  w-full
                  mt-6
                  py-2.5
                  rounded-xl
                  border
                  border-slate-200
                  text-slate-700
                  font-medium
                  text-center
                  hover:bg-slate-50
                  transition
                "
              >
                    View Repository
              </a>    

            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}