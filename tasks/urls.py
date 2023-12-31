from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path('authentication/graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
