from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_text(text: str):
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_chunks(chunks: list[str]):
    return model.encode(
        chunks,
        normalize_embeddings=True,
    ).tolist()