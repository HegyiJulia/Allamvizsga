import { apiClient } from "./client";

export interface SearchResult {
  filename: string;
  snippet: string;
  content:string;
}

export const searchDocuments = async (
  query: string,
  mode: "word" | "phrase",
  startDate?: string,
  endDate?: string
): Promise<SearchResult[]> => {
  try {
    const payload: any = {
      query,
      mode,
    };

    const formatDate = (date: string) => {
      return date.replace(/-/g, ".");
    };

    if (startDate && startDate.trim() !== "") {
      payload.startDate = formatDate(startDate);
    }

    if (endDate && endDate.trim() !== "") {
      payload.endDate = formatDate(endDate);
    }

    const response = await apiClient.post("/search/", payload);
    return response.data.results;
  } catch (error) {
    console.error("Hiba történt a keresés során:", error);
    throw error;
  }
};
