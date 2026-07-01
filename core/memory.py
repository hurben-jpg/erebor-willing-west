import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Any

class Memory:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="erebor_memories")

    def add_memory(self, text: str, metadata: Dict[str, Any] = None):
        """
        Adds a new memory to the database.
        """
        if metadata is None:
            metadata = {}
            
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )

    def get_relevant_memories(self, query: str, n_results: int = 3) -> List[str]:
        """
        Retrieves the most relevant memories for a given query.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # ChromaDB returns a list of lists, we want to flatten it
        if results and results['documents']:
            return results['documents'][0]
        return []

    def clear_memory(self):
        """
        Clears all memories (useful for testing).
        """
        self.client.delete_collection("erebor_memories")
        self.collection = self.client.get_or_create_collection(name="erebor_memories")
