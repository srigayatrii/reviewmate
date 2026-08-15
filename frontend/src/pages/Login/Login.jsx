import { motion } from "framer-motion";
import {
  IconBrandGithub,
  IconCheck,
} from "@tabler/icons-react";

import Button from "../../components/ui/Button";

export default function Login() {
  const handleLogin = () => {
    window.location.href =
      "http://localhost:8000/api/v1/auth/github/login";
  };

  return (
    <div className="min-h-screen bg-[#F7FAFC]">

      <div className="max-w-7xl mx-auto min-h-screen grid lg:grid-cols-2">

        {/* LEFT */}

        <div className="flex items-center px-10 lg:px-20">

          <motion.div
            initial={{
              opacity: 0,
              x: -30,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            transition={{
              duration: 0.6,
            }}
          >

            <div className="w-16 h-16 rounded-2xl bg-[#103A5C] flex items-center justify-center text-white text-3xl mb-8">

              RM

            </div>

            <h1 className="text-6xl font-bold text-slate-900 leading-tight">

              ReviewMate

            </h1>

            <p className="text-xl text-slate-500 mt-6 max-w-lg">

              AI-powered pull request reviews for modern engineering teams.

            </p>

            <div className="space-y-5 mt-12">

              <Feature text="AI generated summaries" />

              <Feature text="Risk detection" />

              <Feature text="Smart recommendations" />

            </div>

            <Button
              onClick={handleLogin}
              className="mt-12 flex items-center justify-center gap-3"
            >
              <IconBrandGithub size={22} />

              Continue with GitHub

            </Button>

          </motion.div>

        </div>

        {/* RIGHT */}

        <div className="hidden lg:flex items-center justify-center">

          <motion.div
            initial={{
              opacity: 0,
              scale: 0.9,
            }}
            animate={{
              opacity: 1,
              scale: 1,
            }}
            transition={{
              delay: 0.3,
            }}
            className="
              w-[520px]
              rounded-3xl
              bg-white
              shadow-2xl
              border
              border-slate-200
              p-8
            "
          >

            <div className="flex justify-between">

              <h2 className="font-bold text-xl">

                Dashboard Preview

              </h2>

              <span className="text-emerald-500 font-medium">

                Live

              </span>

            </div>

            <div className="mt-8 grid grid-cols-2 gap-5">

              <MiniCard
                title="Repositories"
                value="30"
              />

              <MiniCard
                title="Pull Requests"
                value="14"
              />

              <MiniCard
                title="AI Reviews"
                value="54"
              />

              <MiniCard
                title="Open PRs"
                value="5"
              />

            </div>

          </motion.div>

        </div>

      </div>

    </div>
  );
}

function Feature({ text }) {
  return (
    <div className="flex items-center gap-3">

      <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">

        <IconCheck
          size={18}
          className="text-[#103A5C]"
        />

      </div>

      <p className="text-slate-700">

        {text}

      </p>

    </div>
  );
}

function MiniCard({
  title,
  value,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 p-6">

      <p className="text-slate-500">

        {title}

      </p>

      <h3 className="text-4xl font-bold mt-3">

        {value}

      </h3>

    </div>
  );
}
