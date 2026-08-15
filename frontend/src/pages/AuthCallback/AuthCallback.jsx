import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      navigate("/");
      return;
    }

    localStorage.setItem("access_token", token);

    navigate("/dashboard");
  }, [searchParams, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F7FAFC]">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-[#103A5C]">
          Signing you in...
        </h1>

        <p className="text-slate-500 mt-2">
          Preparing your ReviewMate workspace.
        </p>
      </div>
    </div>
  );
}