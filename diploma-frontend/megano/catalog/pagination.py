from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PaginationCatalog(PageNumberPagination):
    def get_paginated_response(self, data, items):
        self.max_page_size = 2
        all_items = items
        result = all_items / self.max_page_size

        if result != (all_items // self.max_page_size):
            total_pages = all_items // self.max_page_size + 1
        else:
            total_pages = all_items // self.max_page_size

        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': total_pages,
        })
