import json
import os
from collections import deque

class Memory:

    def __init__(self, file="memory.json", max_history=20):
        self.file = file
        self.max_history = max_history

        self.history = deque(maxlen=max_history)
        self.facts = {}

        self.load()

    # ------------------------
    # LOAD / SAVE
    # ------------------------
    def load(self):
        if os.path.exists(self.file):
            try:
                data = json.load(open(self.file, "r", encoding="utf-8"))
                self.history = deque(data.get("history", []), maxlen=self.max_history)
                self.facts = data.get("facts", {})
            except:
                pass

    def save(self):
        data = {
            "history": list(self.history),
            "facts": self.facts
        }
        json.dump(data, open(self.file, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # ------------------------
    # DIALOG HISTORY
    # ------------------------
    def add(self, role, text):
        self.history.append({"role": role, "text": text})
        self.save()

    def get_history(self):
        return list(self.history)

    # ------------------------
    # SIMPLE FACT MEMORY
    # ------------------------
    def remember_fact(self, key, value):
        self.facts[key] = value
        self.save()

    def get_facts_text(self):
        if not self.facts:
            return ""

        return "\n".join([f"{k}: {v}" for k, v in self.facts.items()])

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------