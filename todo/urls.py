from django.contrib import admin
from django.urls import path

from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gql/', GraphQLView.as_view(graphiql=True))
]
