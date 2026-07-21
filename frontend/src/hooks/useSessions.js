import { useQuery } from "@tanstack/react-query";
import api from "@/services/api";

const getSessions = async () => {
  const { data } = await api.get("/chat/session");
  return data;
};

export default function useSessions() {
  return useQuery({
    queryKey: ["sessions"],
    queryFn: getSessions,
  });
}