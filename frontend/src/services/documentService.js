import axios from "axios";

const API = "http://localhost:8000/api/v1/documents";

export async function deleteDocument(documentId) {
  const { data } = await axios.delete(`${API}/${documentId}`);
  return data;
}