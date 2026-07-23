import fitz


class PDFService:

    @staticmethod
    def extract_pages(file_bytes: bytes):

        pdf = fitz.open(stream=file_bytes, filetype="pdf")

        pages = []

        for page_number, page in enumerate(pdf, start=1):

            pages.append(
                {
                    "page": page_number,
                    "text": page.get_text()
                }
            )

        pdf.close()

        return pages