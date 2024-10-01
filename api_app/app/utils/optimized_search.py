from typing import Dict, List
import re


class OptimizedSearch:
    def __init__(self):
        self.company_data: Dict[str, Dict] = {}
        self.prefix_index: Dict[str, List[str]] = {}
        self.ngram_index: Dict[str, List[str]] = {}

    def add_company(self, company: Dict):
        company_name = company['corp_name'].lower()
        self.company_data[company_name] = company

        # Prefix indexing
        for i in range(1, len(company_name) + 1):
            prefix = company_name[:i]
            if prefix not in self.prefix_index:
                self.prefix_index[prefix] = []
            self.prefix_index[prefix].append(company_name)

        # N-gram indexing (for substring search)
        ngrams = self._get_ngrams(company_name, n=3)
        for ngram in ngrams:
            if ngram not in self.ngram_index:
                self.ngram_index[ngram] = []
            self.ngram_index[ngram].append(company_name)

    def _get_ngrams(self, text: str, n: int) -> List[str]:
        return [text[i:i + n] for i in range(len(text) - n + 1)]

    def search_prefix(self, query: str) -> List[Dict]:
        query = query.lower()
        if query in self.prefix_index:
            return [self.company_data[name] for name in self.prefix_index[query]]
        return []

    def search_substring(self, query: str) -> List[Dict]:
        query = query.lower()
        ngrams = self._get_ngrams(query, n=3)
        if not ngrams:
            return self.search_prefix(query)

        candidates = set(self.ngram_index.get(ngrams[0], []))
        for ngram in ngrams[1:]:
            candidates.intersection_update(self.ngram_index.get(ngram, []))

        results = []
        for candidate in candidates:
            if query in candidate:
                results.append(self.company_data[candidate])
        return results