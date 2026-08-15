import Layout from "../../components/layout/Layout";

export default function AIReviews() {
  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          AI Reviews
        </h1>

        <p className="text-slate-500 mt-2">
          View AI-powered code review results.
        </p>

        <div className="mt-8 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">
            AI Review History
          </h2>

          <p className="text-slate-500 mt-2">
            Your completed pull request analyses will appear here.
          </p>
        </div>
      </div>
    </Layout>
  );
}