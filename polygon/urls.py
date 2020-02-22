from django.urls import path, include
from .views import polygon_home, PolygonAssigmentListView

app_name='polygon'

urlpatterns = [
    path('', polygon_home, name='home'),    
    path('assignment/', PolygonAssigmentListView.as_view(), name='assignment_list'),

    path('course/', include('polygon.course.urls')),
]
