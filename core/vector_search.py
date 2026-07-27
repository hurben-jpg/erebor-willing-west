import os
import json
import hashlib
from typing import List, Dict

class VectorSearch:
    def __init__(self, kb_file: str, name: str):
        self.kb_file = kb_file
        self.name = name
        self.cache_file = kb_file.replace(".json", "_embeddings.json")
        self.embeddings_model = None
        
        # Load API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if google_key:
            try:
                from langchain_google_genai import GoogleGenAIEmbeddings
                # Using standard task type for retrieval query/document matching
                self.embeddings_model = GoogleGenAIEmbeddings(
                    google_api_key=google_key,
                    model="models/text-embedding-004"
                )
                print(f"[{self.name}] Initialized Google GenAI Embeddings.")
            except Exception as e:
                print(f"[{self.name}] Warning: Failed to load Google Embeddings: {e}")
                
        if not self.embeddings_model and openai_key:
            try:
                from langchain_openai import OpenAIEmbeddings
                self.embeddings_model = OpenAIEmbeddings(api_key=openai_key)
                print(f"[{self.name}] Initialized OpenAI Embeddings.")
            except Exception as e:
                print(f"[{self.name}] Warning: Failed to load OpenAI Embeddings: {e}")
                
        if not self.embeddings_model:
            print(f"[{self.name}] Warning: No embedding model available. Vector search will use mock scores.")

    def calculate_md5(self, filepath: str) -> str:
        """Calculates MD5 hash of a file to check for updates."""
        if not os.path.exists(filepath):
            return ""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def load_cache(self) -> Dict[str, List[float]]:
        """Loads cached embeddings from disk."""
        if not os.path.exists(self.cache_file):
            return {}
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                
            # Verify if the cache is still valid by checking the source KB MD5
            kb_md5 = self.calculate_md5(self.kb_file)
            if cache_data.get("kb_md5") == kb_md5:
                return cache_data.get("embeddings", {})
            else:
                print(f"[{self.name}] Knowledge base updated. Regenerating embeddings...")
        except Exception as e:
            print(f"[{self.name}] Error loading embeddings cache: {e}")
        return {}

    def save_cache(self, embeddings: Dict[str, List[float]]):
        """Saves embeddings cache to disk."""
        try:
            kb_md5 = self.calculate_md5(self.kb_file)
            cache_data = {
                "kb_md5": kb_md5,
                "embeddings": embeddings
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            print(f"[{self.name}] Saved embeddings cache to {self.cache_file}")
        except Exception as e:
            print(f"[{self.name}] Error saving embeddings cache: {e}")

    def rebuild_cache(self, knowledge: List[dict]) -> Dict[str, List[float]]:
        """Embeds all facts in the knowledge base and saves them to cache."""
        if not self.embeddings_model:
            return {}
            
        print(f"[{self.name}] Generating embeddings for {len(knowledge)} facts. This may take a moment...")
        embeddings = {}
        
        # Gather all facts
        facts = [entry.get("fact") for entry in knowledge if entry.get("fact")]
        
        try:
            # Batch embed all documents
            doc_embeddings = self.embeddings_model.embed_documents(facts)
            for fact, emb in zip(facts, doc_embeddings):
                embeddings[fact] = emb
            self.save_cache(embeddings)
        except Exception as e:
            print(f"[{self.name}] Error generating document embeddings: {e}")
            
        return embeddings

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculates cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(v1, v2))
        magnitude1 = sum(x * x for x in v1) ** 0.5
        magnitude2 = sum(x * x for x in v2) ** 0.5
        if magnitude1 * magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def get_matching_knowledge(self, query: str, knowledge: List[dict], k: int = 3) -> str:
        """Retrieves top-k relevant facts using vector semantic search."""
        if not query or not knowledge:
            return ""
            
        # Try loading cached embeddings
        embeddings_cache = self.load_cache()
        
        # If cache is empty or incomplete, rebuild it
        if not embeddings_cache or len(embeddings_cache) < len(knowledge):
            embeddings_cache = self.rebuild_cache(knowledge)
            
        if not self.embeddings_model or not embeddings_cache:
            # Fallback to simple mock/keyword similarity if no embedding model is available
            print(f"[{self.name}] Fallback: Using simple keyword scoring for query.")
            query_words = set(query.lower().replace("?", " ").replace(".", " ").replace(",", " ").split())
            scored_facts = []
            for entry in knowledge:
                fact = entry.get("fact", "")
                kws = entry.get("keywords", [])
                score = sum(1 for kw in kws if kw.lower() in query_words)
                if score > 0:
                    scored_facts.append((score, fact))
            scored_facts.sort(key=lambda x: x[0], reverse=True)
            matched = [fact for score, fact in scored_facts[:k]]
            return "\n".join([f"- {fact}" for fact in matched])
            
        try:
            # Embed query
            query_embedding = self.embeddings_model.embed_query(query)
            
            # Compute similarities
            scored_facts = []
            for fact, emb in embeddings_cache.items():
                sim = self.cosine_similarity(query_embedding, emb)
                # Filter out low similarity matches (threshold = 0.55)
                if sim >= 0.55:
                    scored_facts.append((sim, fact))
                    
            # Sort by similarity score descending
            scored_facts.sort(key=lambda x: x[0], reverse=True)
            
            matched = [fact for sim, fact in scored_facts[:k]]
            if matched:
                print(f"[{self.name}] Vector search matched {len(matched)} facts. Top similarity: {scored_facts[0][0]:.3f}")
                return "\n".join([f"- {fact}" for fact in matched])
        except Exception as e:
            print(f"[{self.name}] Error during vector search: {e}")
            
        return ""
