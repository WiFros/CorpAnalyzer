class CompressedTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = None


class CompressedTrie:
    def __init__(self):
        self.root = CompressedTrieNode()

    def insert(self, key, data):
        node = self.root
        i = 0
        while i < len(key):
            if key[i] not in node.children:
                node.children[key[i]] = CompressedTrieNode()

            child = node.children[key[i]]

            # Try to compress
            j = i + 1
            while j < len(key) and len(child.children) == 1 and not child.is_end:
                only_child_key = next(iter(child.children))
                if key[j] != only_child_key:
                    break
                child = child.children[only_child_key]
                j += 1

            if j > i + 1:
                # Compression possible
                compressed_key = key[i:j]
                new_node = CompressedTrieNode()
                new_node.children = child.children
                node.children[compressed_key] = new_node
                node = new_node
                i = j
            else:
                node = child
                i += 1

        node.is_end = True
        node.data = data

    def search_prefix(self, prefix):
        node = self.root
        i = 0
        while i < len(prefix):
            found = False
            for k, child in node.children.items():
                if prefix.startswith(k, i):
                    i += len(k)
                    node = child
                    found = True
                    break
            if not found:
                return []
        return self._collect_all(node, prefix)

    def search_substring(self, substring):
        results = []
        self._search_substring_helper(self.root, "", substring.lower(), results)
        return results

    def _search_substring_helper(self, node, current_word, substring, results):
        if node.is_end and substring in current_word:
            results.append(node.data)

        for char, child_node in node.children.items():
            self._search_substring_helper(child_node, current_word + char, substring, results)

    def _collect_all(self, node, prefix):
        results = []
        if node.is_end:
            results.append(node.data)
        for k, child in node.children.items():
            results.extend(self._collect_all(child, prefix + k))
        return results