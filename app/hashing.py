import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, replicas: int = 50):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_shard(self, shard_url: str):
        for i in range(self.replicas):
            h = self._hash(f"{shard_url}:{i}")
            self.ring[h] = shard_url
            bisect.insort(self.sorted_keys, h)

    def get_shard(self, key: str) -> str:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, h)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]