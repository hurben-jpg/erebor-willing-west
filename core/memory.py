import json
import os
import uuid
from typing import List, Dict, Any

class Memory:
    def __init__(self, persist_file: str = "./memories.json"):
        # Support fallback path for different running environments
        possible_paths = [
            persist_file,
            os.path.join(os.path.dirname(__file__), "..", persist_file),
            os.path.join(r"d:\PROJECTS\Antigravity\Erebor", persist_file)
        ]
        self.persist_file = persist_file
        for path in possible_paths:
            if os.path.exists(path) or os.path.exists(os.path.dirname(path) or '.'):
                self.persist_file = path
                break
                
        self.memories = []
        self.load_memories()

    def load_memories(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, "r", encoding="utf-8") as f:
                    self.memories = json.load(f)
            except Exception as e:
                print(f"Error loading memories: {e}")
                self.memories = []

    def save_memories(self):
        try:
            with open(self.persist_file, "w", encoding="utf-8") as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memories: {e}")

    def add_memory(self, text: str, metadata: Dict[str, Any] = None):
        if metadata is None:
            metadata = {}
        self.memories.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "metadata": metadata
        })
        self.save_memories()

    def get_relevant_memories(self, query: str, n_results: int = 3) -> List[str]:
        query_words = set(w.strip("?,.!:;\"'") for w in query.lower().split() if len(w) > 2)
        if not query_words:
            return []
            
        scored_memories = []
        for mem in self.memories:
            text = mem["text"]
            text_words = set(w.strip("?,.!:;\"'") for w in text.lower().split())
            score = sum(1 for w in query_words if w in text_words)
            if score > 0:
                scored_memories.append((score, text))
                
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [text for score, text in scored_memories[:n_results]]

    def clear_memory(self):
        self.memories = []
        self.save_memories()
