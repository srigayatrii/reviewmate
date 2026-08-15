import Layout from "../../components/layout/Layout";

export default function Settings() {
  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          Settings
        </h1>

        <p className="text-slate-500 mt-2">
          Manage your ReviewMate settings.
        </p>

        <div className="mt-8 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">
            Account
          </h2>

          <p className="text-slate-500 mt-2">
            ReviewMate is connected to your GitHub account.
          </p>
        </div>
      </div>
    </Layout>
  );
}