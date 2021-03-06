import django_filters
import graphene

import tasks.schema
import users.schema

from graphene_django.debug.types import DjangoDebug


class Query(users.schema.Query, tasks.schema.Query, graphene.ObjectType):
    """Bundle of queries across all sub applications"""
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(users.schema.Mutation,
               tasks.schema.Mutation,
               graphene.ObjectType):
    """Bundle of mutations across all sub applications"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
