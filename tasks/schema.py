import django_filters

from graphene import (
    relay,
    ObjectType,
)
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .models import Task


class TaskNode(DjangoObjectType):

    class Meta:
        model = Task
        filter_fields = ['title', 'done']
        interfaces = (relay.Node,)


class Query:

    task = relay.Node.Field(TaskNode)
    tasks = DjangoFilterConnectionField(TaskNode)
