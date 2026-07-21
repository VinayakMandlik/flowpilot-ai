import { useQuery } from "@tanstack/react-query";
import api from "@/services/api";

export default function useDocuments() {
  return useQuery({
    queryKey: ["documents"],

    queryFn: async () => {
      const response = await api.get("/documents");
      return response.data;
    },

    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}