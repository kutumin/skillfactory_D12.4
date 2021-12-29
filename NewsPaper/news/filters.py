from django_filters import FilterSet 
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = ('id', 'post_author', 'post_type', 'category', 'post_raiting','post_date_created')
 