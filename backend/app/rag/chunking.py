def chunk_text(text: str, chunk_size: int = 400, overlap: int = 60) -> list[str]:
    """
    Split text into overlapping chunks of roughly `chunk_size` characters.
    Tries to break at a paragraph or sentence boundary when possible,
    instead of cutting mid-sentence.
    """
    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Try to find a natural breakpoint near the target end
        window = text[start:end]
        break_point = max(window.rfind("\n\n"), window.rfind(". "))

        if break_point == -1:
            # No natural break found, cut at the target size anyway
            actual_end = end
        else:
            # +2 to include the period+space or the double newline
            actual_end = start + break_point + 2

        chunk = text[start:actual_end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start forward, but back up by `overlap` characters
        start = actual_end - overlap

    return chunks