from django.urls import path
from .views import (
    ReverseView,
    HomePageWithContextView,
    RedirectView,
    PostDetailView,
    redirect_view,
    path_demo_view,
)

app_name = 'demo'

urlpatterns = [
    # MARK: - reverse()
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

    # MARK: - redirect()

    # byModel
    path('redirect/<int:id>/', RedirectView.as_view(), name='redirect'),
    # byView
    path('redirect-by-view/<int:id>/', redirect_view, name='redirect_view'),
    # 被跳转 url
    path('post-detail/<int:id>/', PostDetailView.as_view(), name='detail'),

    # MARK: - path()
    path('path/<int:count>/<str:salute>/', path_demo_view, name='path'),
]
