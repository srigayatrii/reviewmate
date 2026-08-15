import { BrowserRouter, Routes, Route } from "react-router-dom";
import PullRequests from "./pages/PullRequest/PullRequests";
import AuthCallback from "./pages/AuthCallback/AuthCallback";
import Login from "./pages/Login/Login";
import PullRequestDetail from "./pages/PullRequestDetail/PullRequestDetail";
import Dashboard from "./pages/Dashboard/Dashboard";
import Repositories from "./pages/Repository/Repositories";
import AIReviews from "./pages/AIReviews/AIReviews";
import Settings from "./pages/Settings/Settings";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route
          path="/auth/callback"
          element={<AuthCallback />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />
        <Route
          path="/pull-requests"
          element={<PullRequests />}
        />
        <Route
          path="/pull-requests/:id"
          element={<PullRequestDetail />}
        />

        <Route
          path="/repositories"
          element={<Repositories />}
        />

        <Route
          path="/ai-reviews"
          element={<AIReviews />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
