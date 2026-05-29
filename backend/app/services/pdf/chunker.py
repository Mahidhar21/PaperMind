def chunk_text(pages, chunk_size=500, overlap=100):

    chunks = []

    chunk_id = 0

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({
                "chunk_id": chunk_id,
                "page": page["page"],
                "text": chunk
            })

            chunk_id += 1

            start += chunk_size - overlap

    return chunks