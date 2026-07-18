import fitz


def extract_pdf_pages(path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
    [
        {
            "page": 1,
            "text": "..."
        },
        ...
    ]
    """

    doc = fitz.open(path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text().strip()

        if text:
            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    doc.close()

    return pages


def extract_pdf_text(path: str) -> str:
    """
    Backward-compatible helper.
    """

    pages = extract_pdf_pages(path)

    return "\n\n".join(
        page["text"]
        for page in pages
    )    