def chunk_text(text: str, chunk_size: int = 400, overlap: int = 60) -> list[str]:
    """
    Split text into overlapping chunks of roughly `chunk_size` characters.
    Prefers to break at a paragraph or sentence boundary, but only if that
    boundary is in the second half of the window, so chunks never get tiny.
    """
    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            last = text[start:].strip()
            if last:
                chunks.append(last)
            break

        window = text[start:end]
        break_point = max(window.rfind("\n\n"), window.rfind(". "))

        # Ignore breaks in the first half of the window; cut at the target size instead
        if break_point < chunk_size // 2:
            actual_end = end
        else:
            actual_end = start + break_point + 2

        chunk = text[start:actual_end].strip()
        if chunk:
            chunks.append(chunk)

        # Step forward, keeping some overlap, but ALWAYS make progress
        start = max(actual_end - overlap, start + 1)

    return chunks