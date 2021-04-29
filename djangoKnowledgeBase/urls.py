"""djangoKnowledgeBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from demo.views import HomePageView
from django.conf import settings
from django.conf.urls.static import static

from middleware.views import mid_test

urlpatterns = [
    path('admin/', admin.site.urls),
    # MARK: - include()
    path('demo/', include('demo.urls', namespace='demo')),
    path('', HomePageView.as_view(), name='home'),
    path('transanction/', include('transanction_demo.urls', namespace='transanction')),
    # MAR: - 中间件 demo
    path('middleware/',mid_test),
    # 信号
    path('signal/', include('mySignal.urls', namespace='signal')),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
