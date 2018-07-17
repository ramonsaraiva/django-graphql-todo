import django_filters
import graphene

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from users.mixins import LoginRequiredNodeMixin
from .models import Task


class TaskNode(LoginRequiredNodeMixin, DjangoObjectType):

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
    """
    Mutation that creates a task with a given title, to the current
    authenticated user.

    This could be simplified using DRF Serializers, as pointed out here:
    http://docs.graphene-python.org/projects/django/en/latest/rest-framework/ 
    """ 

    class Input:
        title = graphene.String(required=True)

    task = graphene.Field(TaskNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, title):
        task = Task.objects.create(title=title, user=info.context.user)
        return CreateTask(task=task)


class UpdateTask(graphene.relay.ClientIDMutation):
    """
    Mutation that updates a task with a given id, title and done
    to the current authenticated user.

    This could be simplified using DRF Serializers, as pointed out here:
    http://docs.graphene-python.org/projects/django/en/latest/rest-framework/ 
    """ 

    class Input:
        id = graphene.ID(required=True)
        title = graphene.String()
        done = graphene.Boolean()

    task = graphene.Field(TaskNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        qs = Task.objects.filter(id=input['id'])
        if not qs:
            cls()
        qs.update(**input)
        return cls(task=qs.first())


class Mutation:
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
