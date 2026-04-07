import numpy as np


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


def cluster_faces(faces: list[dict], threshold: float = 0.40) -> list[list[int]]:
    """
    Cluster faces by cosine similarity using Union-Find.

    Args:
        faces: list of {id, embedding} dicts
        threshold: cosine distance threshold (VGG-Face default ~0.40)

    Returns:
        list of groups, each group is a list of face IDs
    """
    n = len(faces)
    if n == 0:
        return []

    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_similarity(faces[i]["embedding"], faces[j]["embedding"])
            if sim >= (1 - threshold):
                uf.union(i, j)

    groups = {}
    for i in range(n):
        root = uf.find(i)
        groups.setdefault(root, []).append(faces[i]["id"])
    return list(groups.values())
