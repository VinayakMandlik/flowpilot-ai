from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150

    @staticmethod
    def chunk_text(text):

        if not text:
            return []

        text = text.replace("\r\n", "\n").strip()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=ChunkService.CHUNK_SIZE,
            chunk_overlap=ChunkService.CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n# ",
                "\n## ",
                "\n### ",
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                "",
            ],
        )

        chunks = splitter.split_text(text)

        cleaned_chunks = []
        seen = set()

        for chunk in chunks:

            chunk = " ".join(chunk.split()).strip()

            if len(chunk) < 50:
                continue

            if chunk in seen:
                continue

            seen.add(chunk)
            cleaned_chunks.append(chunk)

        return cleaned_chunks