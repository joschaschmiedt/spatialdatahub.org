from django.conf.urls import url

from accounts import views

app_name = "accounts"

urlpatterns = [

    url(r'^accounts/$',
        views.account_list,
        name="account_list"),

    url(r'^new_account/$',
        views.new_account,
        name="new_account"),

    url(r'^(?P<account_slug>[-\w]*)/$',
        views.account_detail,
        name="account_detail"),

    url(r'^(?P<account_slug>[-\w]*)/portal/$',
        views.account_portal,
        name="account_portal"),

    url(r'^(?P<account_slug>[-\w]*)/remove/$',
        views.account_remove,
        name="account_remove"),

    url(r'^(?P<account_slug>[-\w]*)/update/$',
        views.account_update,
        name="account_update"),

]