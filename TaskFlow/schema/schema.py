import graphene
from graphene_django.types import DjangoObjectType
from tasks.models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, info):
        return Task.objects.all()


schema = graphene.Schema(query=Query)