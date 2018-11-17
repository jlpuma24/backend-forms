from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from api.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/login', login, name='login'),
    url(r'^api/cluster', clusterReport, name='clusterReport'),
    url(r'^api/graphs/(\d+)', grapsHttpResponse, name='grapsHttpResponse'),
    url(r'^api/charts/(\d+)/(\d+)', pieChart, name='pieChart'),
    url(r'^api/addCompany', addCompany, name='addCompany'),
    url(r'^api/editEmployee', editEmployee, name='editEmployee'),
    url(r'^api/addEmployee', addEmployee, name='addEmployee'),
    url(r'^api/employeeReport', employeeReport, name='employeeReport'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
