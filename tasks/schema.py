import django_filters
import graphene

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .models import Task


class LoginRequiredNode:
    """
    Mixin that injects `login_required` decorator to `get_node`
    """

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return cls._meta.model.objects.filter(
            user=info.context.user).get(id=id)


class TaskNode(LoginRequiredNode, DjangoObjectType):

    class Meta:
        model = Task
        filter_fields = ['title', 'done']
        interfaces = (graphene.relay.Node,)


class Query:

    task = graphene.relay.Node.Field(TaskNode)
    tasks = DjangoFilterConnectionField(TaskNode)

    @login_required
    def resolve_tasks(self, info, **kwargs):
        return Task.objects.filter(user=info.context.user)


class CreateTask(graphene.relay.ClientIDMutation):

    class Input:
        title = graphene.String(required=True)

    task = graphene.Field(TaskNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, title):
        task = Task.objects.create(title=title, user=info.context.user)
        return CreateTask(task=task)


class Mutation:
    create_task = CreateTask.Field()
