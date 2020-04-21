from django.urls import path
from .views import (
    ReverseToSomePageView,
    HomePageWithContextView,
    HomePageWithContextAndParamsView,
)

app_name = 'demo'

urlpatterns = [

    path('reverse/',
         ReverseToSomePageView.as_view(),
         name='reverse'),

    path('home-with-context/',
         HomePageWithContextView.as_view(),
         name='home_with_context'),

    path('home-with-context-and-params/<int:id>/',
         HomePageWithContextAndParamsView.as_view(),
         name='home_with_context_and_params'),
]
