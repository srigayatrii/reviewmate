import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  GitPullRequest,
  ExternalLink,
  Sparkles,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

import Layout from "../../components/layout/Layout";
import {
  getPullRequest,
  analyzePullRequest,
} from "../../services/pullRequestService";

export default function PullRequestDetail() {
  const { id } = useParams();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadPullRequest();
  }, [id]);

  async function loadPullRequest() {
    try {
      const result = await getPullRequest(id);
      setData(result);
    } catch (error) {
      console.error(error);
      setError("Failed to load pull request.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAnalyze() {
    try {
      setAnalyzing(true);
      setError("");

      await analyzePullRequest(id);

      // Give the RQ worker a little time to process.
      setTimeout(async () => {
        await loadPullRequest();
        setAnalyzing(false);
      }, 5000);

    } catch (error) {
      console.error(error);
      setError("Failed to start AI analysis.");
      setAnalyzing(false);
    }
  }

  if (loading) {
    return (
      <Layout>
        <p className="text-slate-500">
          Loading pull request...
        </p>
      </Layout>
    );
  }

  if (error && !data) {
    return (
      <Layout>
        <p className="text-red-500">{error}</p>
      </Layout>
    );
  }

  const pr = data?.pull_request;
  const analysis = data?.analysis;

  return (
    <Layout>
      <div className="max-w-5xl">

        {/* PR HEADER */}
        <div className="flex items-start justify-between gap-6 mb-8">

          <div className="flex gap-4">

            <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center">
              <GitPullRequest
                className="text-blue-600"
                size={24}
              />
            </div>

            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                {pr?.title}
              </h1>

              <p className="text-slate-500 mt-2">
                PR #{pr?.pr_number}
              </p>
            </div>

          </div>

          {pr?.html_url && (
            <a
              href={pr.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm font-medium text-blue-600"
            >
              View on GitHub
              <ExternalLink size={16} />
            </a>
          )}

        </div>

        {/* AI REVIEW */}
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">

          <div className="flex items-center justify-between gap-6">

            <div>
              <h2 className="text-xl font-semibold text-slate-900">
                AI Code Review
              </h2>

              <p className="text-slate-500 mt-1">
                Analyze this pull request with ReviewMate AI.
              </p>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="
                flex
                items-center
                gap-2
                px-6
                py-3
                rounded-xl
                bg-[#103A5C]
                text-white
                font-semibold
                hover:bg-[#0B2B45]
                disabled:opacity-50
                disabled:cursor-not-allowed
                transition
              "
            >
              <Sparkles size={18} />

              {analyzing
                ? "Analyzing..."
                : "Analyze PR"}
            </button>

          </div>

          {error && (
            <p className="mt-6 text-red-500">
              {error}
            </p>
          )}

          {/* ANALYSIS RESULT */}

          {analysis && (
            <div className="mt-8 border-t border-slate-200 pt-8">

              {/* STATUS + RISK */}

              <div className="flex flex-wrap gap-4">

                <div className="px-4 py-3 rounded-xl bg-slate-50">
                  <p className="text-xs text-slate-500">
                    Status
                  </p>

                  <p className="font-semibold text-slate-900 mt-1 flex items-center gap-2">
                    <CheckCircle size={16} />
                    {analysis.status}
                  </p>
                </div>

                <div className="px-4 py-3 rounded-xl bg-slate-50">
                  <p className="text-xs text-slate-500">
                    Risk
                  </p>

                  <p className="font-semibold text-slate-900 mt-1 flex items-center gap-2">
                    <AlertTriangle size={16} />
                    {analysis.risk_score}
                  </p>
                </div>

                <div className="px-4 py-3 rounded-xl bg-slate-50">
                  <p className="text-xs text-slate-500">
                    Missing Tests
                  </p>

                  <p className="font-semibold text-slate-900 mt-1">
                    {analysis.missing_tests
                      ? "Yes"
                      : "No"}
                  </p>
                </div>

              </div>

              {/* SUMMARY */}

              <div className="mt-8">
                <h3 className="text-lg font-semibold text-slate-900">
                  Summary
                </h3>

                <p className="text-slate-600 mt-3 leading-7">
                  {analysis.summary}
                </p>
              </div>

              {/* RECOMMENDATIONS */}

              <div className="mt-8">
                <h3 className="text-lg font-semibold text-slate-900">
                  Recommendations
                </h3>

                <div className="mt-3 bg-slate-50 rounded-xl p-5">
                  <p className="text-slate-600 whitespace-pre-line leading-7">
                    {analysis.recommendations}
                  </p>
                </div>
              </div>

            </div>
          )}

        </div>

      </div>
    </Layout>
  );
}

