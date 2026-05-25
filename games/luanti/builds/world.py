"""Thin wrapper so build functions can place nodes via Miney."""

from miney import Node

from .blocks import NODES

_BATCH_SIZE = 20_000


class LuantiWorld:
    """Miney-backed world with mcpi-like set_block / set_blocks helpers."""

    def __init__(self, lt):
        self.lt = lt

    def set_block(self, x, y, z, node_name):
        self.lt.nodes.set(Node(int(x), int(y), int(z), name=node_name))

    def set_blocks(self, x1, y1, z1, x2, y2, z2, node_name):
        xa, xb = min(x1, x2), max(x1, x2)
        ya, yb = min(y1, y2), max(y1, y2)
        za, zb = min(z1, z2), max(z1, z2)
        batch = []
        for x in range(xa, xb + 1):
            for y in range(ya, yb + 1):
                for z in range(za, zb + 1):
                    batch.append(Node(x, y, z, name=node_name))
                    if len(batch) >= _BATCH_SIZE:
                        self.lt.nodes.set(batch)
                        batch = []
        if batch:
            self.lt.nodes.set(batch)

    def node(self, key):
        return NODES[key]
