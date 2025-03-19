import { apiClient } from "./client";

export interface SearchResult {
  filename: string;
  snippet: string;
  content:string;
}

export const searchByWord = async (word: string): Promise<SearchResult[]> => {
  try {
    const response = await apiClient.post("/search", { query: word });

    console.log(response.data);
    return response.data.results;
  } catch (error) {
    console.error("Hiba történt a keresés során:", error);
    throw error;
  }
};
