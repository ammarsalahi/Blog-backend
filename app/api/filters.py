from django_filters import FilterSet


class NewsFilter(FilterSet):
    q=CharFilter(method='search_project')
    sort=CharFilter(method='sorting')
    class Meta:
        model=Project
        fields=('q','sort')

    def search_post(self,queryset,name,value):
        return  queryset.filter(
            Q(title__icontains=value)|
            Q(description__icontains=value)
        )    
    def sorting(self,queryset,name,value):
        if value==True:
            return queryset.order_by('created_at')
        else:
            return queryset.order_by('-created_at')