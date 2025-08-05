"""
URL configuration for smartdoc_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core.views import upload_document
from django.conf import settings
from django.conf.urls.static import static
from core.views import upload_file
from core.views import document_pdf
from core.views import preview_document
from core.views import test_log_view
from core.views import test_log_from_utils

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_document, name='upload_document'),
    path('upload_success/',upload_document,name='upload_success'),
    path('upload-file/', upload_file, name='upload_file'),
    path('pdf/<int:doc_id>/', document_pdf, name='document_pdf'),
    path('preview/<int:pk>/', preview_document, name='preview_document'),
    path('test-log/', test_log_view,name='test_logging_view'),
    path('test-log_from_utils/', test_log_from_utils, name='test_logging_view_from_utils'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





