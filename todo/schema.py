import django_filters
import graphene

import tasks.schema
import users.schema

from graphene import (
    relay,
    ObjectType,
)
from graphene_django import DjangoObjectType
from graphene_django.debug.types import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User


class UserNode(DjangoObjectType):

    class Meta:
        model = User
        filter_fields = ['username']
        interfaces = (relay.Node,)


class UserQuery:

    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Query(UserQuery, tasks.schema.Query, ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(users.schema.Mutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
