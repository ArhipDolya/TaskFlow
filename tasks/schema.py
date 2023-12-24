import graphene
from graphene_django import DjangoObjectType
from .models import Task


class TasksType(DjangoObjectType):
    class Meta:
        model = Task


class Query(graphene.ObjectType):
    all_tasks = graphene.List(TasksType)

    def resolve_all_tasks(root, info):
        return Task.objects.all()


schema = graphene.Schema(query=Query)