import graphene


class TaskCreateInput(graphene.InputObjectType):
    title = graphene.String(required=True)


class TaskUpdateInput(graphene.InputObjectType):
    title = graphene.String()
    done = graphene.Boolean()