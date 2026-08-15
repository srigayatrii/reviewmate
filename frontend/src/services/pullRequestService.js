const API_BASE_URL = "http://localhost:8000/api/v1";

function getToken() {
  return localStorage.getItem("access_token");
}

export async function getPullRequests() {
  const response = await fetch(
    `${API_BASE_URL}/pull-requests`,
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch pull requests");
  }

  return response.json();
}

export async function getPullRequest(id) {
  const response = await fetch(
    `${API_BASE_URL}/pull-requests/${id}`,
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch pull request");
  }

  return response.json();
}

export async function analyzePullRequest(id) {
  const response = await fetch(
    `${API_BASE_URL}/pull-requests/${id}/analyze`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to analyze pull request");
  }

  return response.json();
}