import json
import os
import argparse
from sentence_transformers import SentenceTransformer
import faiss
import glob

# --------------------------
# Step 1: Load and chunk documentation
# --------------------------

def load_docs(root="./postman-twitter-api-master"):
    chunks = []
    metadata = []
    chunk_id = 0
    
    for file in glob.glob(root + "/**/*.json", recursive=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Flatten JSON and extract all text fields
                def extract(obj):
                    texts = []
                    if isinstance(obj, dict):
                        for v in obj.values():
                            texts.extend(extract(v))
                    elif isinstance(obj, list):
                        for item in obj:
                            texts.extend(extract(item))
                    elif isinstance(obj, str):
                        texts.append(obj)
                    return texts

                raw_text = extract(data)
                for t in raw_text:
                    if len(t.strip()) > 20:  # avoid tiny fragments
                        chunks.append(t.strip())
                        metadata.append({
                            "chunk_id": chunk_id,
                            "source": file,
                            "text": t.strip()
                        })
                        chunk_id += 1

        except:
            pass
    return chunks, metadata


# --------------------------
# Step 2: Build FAISS Index
# --------------------------

def build_index(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return model, index, embeddings


# --------------------------
# Step 3: Query Function
# --------------------------

def search(query, model, index, chunks, metadata, k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    distances, ids = index.search(q_emb, k)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], ids[0]), start=1):
        meta = metadata[idx]
        results.append({
            "rank": rank,
            "score": float(dist),
            "chunk_id": meta["chunk_id"],
            "source": meta["source"],
            "text": meta["text"]
        })
    return results


# --------------------------
# Step 4: Command Line
# --------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    print("Loading documentation...")
    chunks, metadata = load_docs()

    print("Building embeddings + FAISS index...")
    model, index, _ = build_index(chunks)

    print("Searching...")
    results = search(args.query, model, index, chunks, metadata, k=args.top_k)

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
