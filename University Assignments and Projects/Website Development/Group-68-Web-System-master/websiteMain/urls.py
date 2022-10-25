from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
#Main Pages
    url(r'^$', views.index, name='index'),
	url(r'^/information', views.information, name='information'),
	url(r'^/help', views.help, name='help'),
	url(r'^/contacts', views.contacts, name='contacts'),

	url(r'^/register', views.register, name='register'),
	#url(r'^login', views.user_login, name ='login'),
	url(r'^logout', views.user_logout, name='logout'),

	url(r'^/categories', views.categories, name='categories'),

        # /information/malls
    url(r'^information/malls$', views.malls, name='malls'),
    
        # /information/malls/#/
    url(r'^mall_ID/(?P<mall_id>[0-9]+)/$', views.mall_detail, name='detail'),
	


#create update delete items

    # /websiteMain/mall/add/
    url(r'^/mall/add',views.MallCreate.as_view(), name='mall-add'),

    # /websiteMain/mall/id/
    #url(r'^/mall/(?P<id>[0-9]+)',views.MallUpdate.as_view(), name='mall-update'),

    # /websiteMain/mall/id/delete/
    url(r'^/mall(?P<id>[0-9]+)/delete',views.MallDelete.as_view(), name='mall-delete'),
    
#Data Stores


]
