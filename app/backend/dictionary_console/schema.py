import graphene
from graphene_django import DjangoObjectType
from .models import *


class WordGraphql(DjangoObjectType):
    class Meta:
        model = Word


class Query(graphene.ObjectType):
    items = graphene.List(WordGraphql)