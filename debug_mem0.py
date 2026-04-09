import os
from config import config
from mem0 import Memory

def debug_mem0():
    print("Mem0 Config:")
    print(config.MEM0_CONFIG)
    
    memory = Memory.from_config(config.MEM0_CONFIG)
    
    print("\nEmbedder Provider:", memory.embedder.provider)
    # Check if there's a way to get the embedding dimension
    # Some mem0 versions have memory.embedder.embedding_dimension
    try:
        # Check if we can get dimension from a dummy embedding
        dummy_text = "test"
        embedding = memory.embedder.embed(dummy_text)
        print(f"Embedding dimension for '{dummy_text}': {len(embedding)}")
    except Exception as e:
        print(f"Could not get embedding dimension: {e}")

    # Check existing collections in Qdrant if possible
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(path=config.MEM0_CONFIG["vector_store"]["config"]["path"])
        collections = client.get_collections().collections
        print("\nQdrant Collections:")
        for col in collections:
            print(f"- {col.name}")
            info = client.get_collection(col.name)
            print(f"  Vector size: {info.config.params.vectors.size}")
    except Exception as e:
        print(f"Could not check Qdrant collections: {e}")

if __name__ == "__main__":
    debug_mem0()
