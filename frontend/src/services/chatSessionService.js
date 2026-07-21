import api from "./api";

export const createSession = async (title, documentId) => {
  const { data } = await api.post("/chat/session", {
    title,
    document_id: documentId,
  });

  return data;
};

export const getMessages = async (sessionId) => {
  const { data } = await api.get(`/chat/session/${sessionId}`);
  return data;
};

export const deleteSession = async (sessionId) => {
  await api.delete(`/chat/session/${sessionId}`);
};