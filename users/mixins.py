from graphql_jwt.decorators import login_required


class LoginRequiredNodeMixin:
    """
    Mixin that injects `login_required` decorator to `get_node`.
    There should probably be a better way of doing this.
    """

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return cls._meta.model.objects.filter(
            user=info.context.user).get(id=id)
