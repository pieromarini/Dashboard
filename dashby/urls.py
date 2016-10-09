from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .forms import LoginForm
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    #dashby/
    url(r'^$', views.DashbyView.as_view(),
        name = 'dashby'),

    #dashby/users/
    url(r'^users/$', views.AllUsersViews.as_view(),
        name = 'users'),

    #dashby/files/
    url(r'^files/$', views.IndexView.as_view(),
        name = 'files'),

    #dashby/private/
    url(r'^private/$', views.PrivateFilesView.as_view(),
        name = 'private'),

    #dashby/files/<pk>/
    url(r'^files/(?P<pk>[0-9]+)/$', views.DetailView.as_view(),
        name = 'detail'),

    #dashby/files/add/
    url(r'^files/add/$', views.DocumentCreate.as_view(),
        name = 'document-add'),

    #dashby/files/<pk>/edit/
    url(r'^files/(?P<pk>[0-9]+)/edit/$',
        views.DocumentUpdate.as_view(),
        name = 'document-update'),

    #dashby/files/<pk>/delete/
    url(r'^files/(?P<pk>[0-9]+)/delete/$',
        views.DocumentDelete.as_view(),
        name = 'document-delete'),

    #dashby/register/
    url(r'^register/$', views.UserFormView.as_view(),
        name = 'register'),

    url(r'^login/$', views.LoginFormView.as_view(),
        name = 'login'),

    url(r'^logout/$', views.LogoutFormView.as_view(),
        name = 'logout'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
