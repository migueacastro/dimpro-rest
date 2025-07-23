from rest_framework.pagination import PageNumberPagination
import django_filters
from auditlog.models import LogEntry

class StardardResultsSetPagination(PageNumberPagination):
    page_size = 1000000 #idk, just change it if you see fit
    page_size_query_param = 'page_size'
    max_page_size = 10000

class LogsResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000

class LogEntryFilter(django_filters.FilterSet):
    actor_id = django_filters.CharFilter(field_name='actor__id', lookup_expr='icontains')
    actor_name = django_filters.CharFilter(field_name='actor__name', lookup_expr='icontains')
    actor_email = django_filters.CharFilter(field_name='actor__email', lookup_expr='icontains')
    content_type_model = django_filters.CharFilter(field_name='content_type__model', lookup_expr='icontains')
    remote_addr = django_filters.CharFilter(field_name='remote_addr', lookup_expr='icontains')
    timestamp = django_filters.IsoDateTimeFromToRangeFilter(field_name='timestamp', lookup_expr='date')
    not_system = django_filters.BooleanFilter(method='filter_not_system')
    action_name = django_filters.CharFilter(method='filter_action_name')
    changes_text = django_filters.CharFilter(method='filter_changes_text')
    # ...otros filtros...

    def filter_not_system(self, queryset, name, value):
        # Si value es True, excluye los registros del sistema (por ejemplo, actor es None)
        if value:
            return queryset.exclude(actor__isnull=True)
        # Si value es False o no está presente, no filtra nada
        return queryset
    # Custom filter for action name
    

    def filter_action_name(self, queryset, name, value):
        mapping = {
            "creación": 0,
            "actualización": 1,
            "eliminación": 2,
            "inicio / cierre de sesión": 3,
        }
        norm_value = value.lower().strip()
        # Find all matching numeric values whose keys contain the normalized value.
        matches = [num for key, num in mapping.items() if norm_value in key.lower()]
        print("Matches found:", matches)
        if matches:
            # Use __in so that if more than one key partially matches, you get any of them.
            return queryset.filter(action__in=matches)
        else:
            return queryset.none()
    
    def filter_changes_text(self, queryset, name, value):
        mapping = {
            "creación": 0,
            "actualización": 1,
            "eliminación": 2,
            "inicio / cierre de sesión": 3,
        }
        norm_value = value.lower().strip()
        matches = [num for key, num in mapping.items() if norm_value in key.lower()]
        if matches:
            return queryset.filter(action__in=matches)
        else:
            return queryset.none()

    class Meta:
        model = LogEntry
        fields = {
            'actor__name': ['icontains'],
            'actor__email': ['icontains'],
            'content_type__model': ['icontains'],
            'changes_text': ['icontains'],
            'remote_addr': ['icontains'],
            'timestamp': ['date'],
        }