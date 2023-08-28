from django.urls import path
from inventoryData.views import AddBoxApi, DeleteBoxApi, ListAllBoxesApi, UpdateBoxApi, ListMyBoxesApi

urlpatterns = [
    path("add-box", AddBoxApi.as_view()),
    path("delete-box", DeleteBoxApi.as_view()),
    path("list-all-box", ListAllBoxesApi.as_view()),
    path("update-box", UpdateBoxApi.as_view()),
    path("list-my-box", ListMyBoxesApi.as_view()),
]
