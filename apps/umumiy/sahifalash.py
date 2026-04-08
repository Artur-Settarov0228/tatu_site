from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MaxsusSahifalash(PageNumberPagination):
    """Maxsus sahifalash - har bir sahifada 20 ta element"""
    
    page_size = 20
    page_size_query_param = 'sahifa_olchami'
    max_page_size = 100
    page_query_param = 'sahifa'
    
    def get_paginated_response(self, data):
        return Response({
            'boglamlar': {
                'keyingi': self.get_next_link(),
                'oldingi': self.get_previous_link(),
            },
            'jami': self.page.paginator.count,
            'sahifalar_soni': self.page.paginator.num_pages,
            'joriy_sahifa': self.page.number,
            'natijalar': data
        })


class KichikSahifalash(PageNumberPagination):
    """Kichik sahifalash - har bir sahifada 10 ta element"""
    
    page_size = 10
    page_size_query_param = 'sahifa_olchami'
    max_page_size = 50
    page_query_param = 'sahifa'


class KattaSahifalash(PageNumberPagination):
    """Katta sahifalash - har bir sahifada 50 ta element"""
    
    page_size = 50
    page_size_query_param = 'sahifa_olchami'
    max_page_size = 200
    page_query_param = 'sahifa'