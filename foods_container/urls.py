from django.urls import path


from .views import *

urlpatterns = [
    path("home/", Home.as_view(), name="home"),
    path("detail/<uuid:id>", ContainerDetail.as_view(), name="detail"),
    path('create/', CreateContainer.as_view(), name="create"),
    path('edit/<uuid:id>', EditContainer.as_view(), name="edit"),
    path('delete/<uuid:id>', DeleteContainer.as_view(), name="delete"),
]