from django.conf.urls import url

from orders import views

urlpatterns = [
    url(r"^health/$", views.health, name="health"),
    url(r"^config/$", views.config, name="config"),
    url(r"^items/(?P<sku>[\w-]+)/$", views.item, name="item"),
    url(r"^items/(?P<sku>[\w-]+)/reserve/$", views.reserve, name="reserve"),
]
