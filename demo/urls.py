from django.urls import path
from .views import (
    ReverseView,
    HomePageWithContextView,
)

app_name = 'demo'

urlpatterns = [
    # MARK: - Reverse()
    path('reverse/',
         ReverseView.as_view(),
         name='reverse'),

    path('reverse/<int:id>/',
         ReverseView.as_view(),
         name='reverse'),

    path('home-with-context/',
         HomePageWithContextView.as_view(),
         name='home_with_context'),

    path('home-with-context/<int:id>/',
         HomePageWithContextView.as_view(),
         name='home_with_context'),

]
