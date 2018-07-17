import graphql_jwt

from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth import get_user_model


User = get_user_model()


class UserNode(DjangoObjectType):

    class Meta:
        model = User
        filter_fields = ['username']
        exclude_fields = ['password']
        interfaces = (relay.Node,)


class Query:

    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)



class Mutation:
    """JWT Authentication mutations"""
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
