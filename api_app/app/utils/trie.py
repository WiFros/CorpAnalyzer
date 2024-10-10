# app/utils/trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.companies = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, company: dict):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.companies.append(company)
        node.is_end = True

    def search_prefix(self, prefix: str):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return node.companies

    def search_substring(self, substring: str):
        results = set()
        def dfs(node, current_word):
            if substring.lower() in current_word.lower():
                results.update(node.companies)
            for char, child in node.children.items():
                dfs(child, current_word + char)

        dfs(self.root, "")
        return list(results)

    def build_from_companies(self, companies):
        for company in companies:
            self.insert(company['corp_name'], company)