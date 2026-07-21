import { useState } from "react";
import { Upload, Loader2 } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { uploadDocument } from "@/services/uploadService";

export default function UploadDialog({ open, onClose }) {
  const [file, setFile] = useState(null);

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: uploadDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["documents"],
      });

      alert("Document uploaded successfully!");

      setFile(null);
      onClose();
    },

    onError: (err) => {
      alert(err.response?.data?.detail || "Upload failed");
    },
  });

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="w-[500px] rounded-2xl bg-zinc-900 p-6">

        <h2 className="mb-5 text-xl font-semibold text-white">
          Upload PDF
        </h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-6 w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 text-white"
        />

        <div className="flex justify-end gap-3">

          <button
            onClick={onClose}
            className="rounded-lg bg-zinc-700 px-4 py-2 text-white hover:bg-zinc-600"
          >
            Cancel
          </button>

          <button
            disabled={!file || mutation.isPending}
            onClick={() => mutation.mutate(file)}
            className="flex items-center gap-2 rounded-lg bg-white px-4 py-2 font-medium text-black disabled:opacity-50"
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="animate-spin" size={18} />
                Uploading...
              </>
            ) : (
              <>
                <Upload size={18} />
                Upload
              </>
            )}
          </button>

        </div>

      </div>
    </div>
  );
}