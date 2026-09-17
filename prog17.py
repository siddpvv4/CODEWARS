import math

class PaginationHelper:
    def __init__(self, collection, items_per_page):
        self.collection = collection
        self.items_per_page = items_per_page

    def item_count(self):
        return len(self.collection)

    def page_count(self):
        if self.items_per_page <= 0:
            return 0
        return math.ceil(len(self.collection) / self.items_per_page)

    def page_item_count(self, page_index):
        total_pages = self.page_count()
        
        if page_index < 0 or page_index >= total_pages:
            return -1
        
        if page_index == total_pages - 1:
            remainder = len(self.collection) % self.items_per_page
            return remainder if remainder != 0 else self.items_per_page
        
        return self.items_per_page

    def page_index(self, item_index):
        if item_index < 0 or item_index >= len(self.collection):
            return -1
        
        return item_index // self.items_per_page
