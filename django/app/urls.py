from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .views import IndexView, LogOutView

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path(r"", IndexView.as_view(), name="index"),
    path(r"logout/", LogOutView.as_view(), name="logout"),
]
