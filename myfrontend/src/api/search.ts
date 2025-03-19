import { apiClient } from "./client";

export const searchByWord = async (word : string) => {
  try {
    const response = await apiClient.post("/search", { query: word });

    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error("Error searching:", error);
    throw error;
  }
};
