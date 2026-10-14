from heapq import heappush, heappop, heapify
from itertools import count


def frequencies(s):
    """Return list of (character, frequency) pairs."""
    freq = {}

    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    return list(freq.items())


def build_tree(freqs):
    """
    Builds the Huffman tree.

    Leaf:
        ('leaf', character)

    Internal node:
        ('node', left, right)
    """

    # Unique counter prevents Python from trying to compare tree nodes
    # when two frequencies are equal.
    unique = count()

    heap = [
        (freq, next(unique), ('leaf', char))
        for char, freq in freqs
    ]

    heapify(heap)

    while len(heap) > 1:
        freq1, _, left = heappop(heap)
        freq2, _, right = heappop(heap)

        node = ('node', left, right)

        heappush(
            heap,
            (freq1 + freq2, next(unique), node)
        )

    return heap[0][2]


def build_codes(tree):
    """Generate {character: binary_code} from the Huffman tree."""

    codes = {}

    def traverse(node, code):
        if node[0] == 'leaf':
            codes[node[1]] = code
            return

        # 0 -> left
        traverse(node[1], code + '0')

        # 1 -> right
        traverse(node[2], code + '1')

    traverse(tree, '')

    return codes


def encode(freqs, s):
    # A frequency list containing <= 1 symbol is invalid
    if len(freqs) <= 1:
        return None

    tree = build_tree(freqs)
    codes = build_codes(tree)

    return ''.join(codes[ch] for ch in s)


def decode(freqs, bits):
    # A frequency list containing <= 1 symbol is invalid
    if len(freqs) <= 1:
        return None

    tree = build_tree(freqs)

    result = []
    node = tree

    for bit in bits:
        if bit == '0':
            node = node[1]
        else:
            node = node[2]

        # Reached a leaf
        if node[0] == 'leaf':
            result.append(node[1])
            node = tree

    return ''.join(result)
