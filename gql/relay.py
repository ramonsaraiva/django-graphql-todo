import graphene

from graphql_jwt.decorators import login_required


class NodeOwnerMixin:
    """
    Mixin that changes the behaviour of `get_node`, when defining a an
    object type that uses the relay Node interface.

    To access this particular node, the user needs to be authenticated in
    `graphql_jwt` and "own" the model of the node.
    """

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return cls._meta.model.objects.filter(
            user=info.context.user).get(id=id)


class LoginRequiredMutation(graphene.relay.ClientIDMutation):
    """
    Mutation class that requires the user to be authenticated in `graphql_jwt`
    to perform the mutation.
    """

    @classmethod
    @login_required
    def mutate(cls, *args, **kwargs):
        return super(LoginRequiredMutation, self).mutate(*args, **kwargs)
