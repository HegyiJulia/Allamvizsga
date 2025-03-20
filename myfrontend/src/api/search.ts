import { apiClient } from "./client";

export interface SearchResult {
  filename: string;
  snippet: string;
  content:string;
}

export const searchDocuments = async (query: string, mode:"word"|"phrase"): Promise<SearchResult[]> => {
  try {
    const response = await apiClient.post("/search", { query, mode });

    console.log(response.data);
    return response.data.results;
  } catch (error) {
    console.error("Hiba történt a keresés során:", error);
    throw error;
  }
};
