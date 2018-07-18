import django_filters
import graphene

from graphene.relay.node import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from users.mixins import LoginRequiredNodeMixin
from .inputs import (
    TaskCreateInput,
    TaskUpdateInput
)
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
    """ 

    class Input:
        task = graphene.Argument(TaskCreateInput)

    task = graphene.Field(TaskNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, title):
        task = Task.objects.create(title=title, user=info.context.user)
        return CreateTask(task=task)


class UpdateTask(graphene.relay.ClientIDMutation):
    """
    Mutation that updates a task with a given a global id, title and done
    to the current authenticated user.
    """ 

    class Input:
        id = graphene.String(required=True)
        task = graphene.Argument(TaskUpdateInput)

    task = graphene.Field(TaskNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            _, task_id = Node.from_global_id(input['id'])
        except:
            return cls()
        qs = Task.objects.filter(user=info.context.user, id=task_id)
        if not qs:
            cls()
        qs.update(**input['task'])
        return cls(task=qs.first())


class DeleteTask(graphene.relay.ClientIDMutation):
    """
    Mutation that deletes a task with a given id to the current
    authenticated user.
    """ 

    class Input:
        id = graphene.String(required=True)

    count = graphene.Int()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            _, task_id = Node.from_global_id(input['id'])
        except:
            return cls()
        n, _ = Task.objects.filter(user=info.context.user, id=task_id).delete()
        return cls(count=n)


class Mutation:
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()