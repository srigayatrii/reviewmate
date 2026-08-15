import api from "./api";

export const getRepositories = async () => {
  const response = await api.get("/repositories");
  return response.data;
};

export const syncRepositories = async () => {
  const response = await api.get("/repositories/sync");
  return response.data;
};

export const connectRepository = async (repositoryId) => {
  const response = await api.post(
    `/repositories/${repositoryId}/connect`
  );

  return response.data;
};

export const disconnectRepository = async (repositoryId) => {
  const response = await api.post(
    `/repositories/${repositoryId}/disconnect`
  );

  return response.data;
};