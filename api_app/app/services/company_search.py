from app.utils.compressed_trie import CompressedTrie
from app.database import get_database
from app.models.company import Company

class CompanySearchService:
    def __init__(self):
        self.trie = CompressedTrie()

    async def initialize_trie(self):
        db = await get_database()
        async for company in db.companies.find({}, {"corp_code": 1, "corp_name": 1, "_id": 0}):
            self.trie.insert(company['corp_name'].lower(), {
                'corp_code': company['corp_code'],
                'corp_name': company['corp_name']
            })

    def search_companies(self, query: str, search_type: str = 'prefix', page: int = 1, page_size: int = 10):
        if search_type == 'prefix':
            results = self.trie.search_prefix(query.lower())
        elif search_type == 'substring':
            results = self.trie.search_substring(query.lower())
        else:
            raise ValueError("Invalid search type. Use 'prefix' or 'substring'.")

        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = results[start:end]

        companies = [Company.model_validate(company) for company in paginated_results]
        total_pages = -(-total // page_size)  # Ceiling division

        return {
            "companies": companies,
            "total": total,
            "page": page,
            "total_pages": total_pages
        }