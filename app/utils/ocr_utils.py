import fitz


class OCRUtils:

    @staticmethod
    def pdf_to_pages(pdf_path: str):

        document = fitz.open(pdf_path)

        pages = []

        for page_index in range(len(document)):

            page = document.load_page(page_index)

            raw_text = page.get_text()

            pages.append(
                {
                    "page_number": page_index + 1,
                    "raw_content": raw_text
                }
            )

        document.close()

        return pages