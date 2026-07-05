from app.clients.llm import LLMClient


class ParagraphLLM:

    @staticmethod
    def extract_paragraphs(pages):

        text = ""

        for page in pages:

            text += f"""

==============================
PAGE NUMBER: {page.page_number}
==============================

{page.raw_content}

"""

        prompt = f"""
You are an expert book parser.

Your task is to process the following book pages.

Instructions:

1. Check whether each page is relevant for paragraph extraction.
2. Ignore pages that are:
   - Table of Contents
   - Index
   - Copyright page
   - Blank page
   - Publisher information
3. If the page is relevant:
   - Extract logical paragraphs.
   - Preserve paragraph order.
   - Preserve page numbers.
   - If a paragraph continues onto the next page, identify it correctly.
4. Return ONLY valid JSON.
5. Do not add explanations or markdown.

Book Pages:

{text}
"""

        llm = LLMClient()

        return llm.generate_content(
            prompt=prompt
        )