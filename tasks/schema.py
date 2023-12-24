import graphene
from graphene_django import DjangoObjectType
from .models import Task


class TasksType(DjangoObjectType):
    class Meta:
        model = Task


class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=False)

    task = graphene.Field(TasksType)

    def mutate(self, info, title, description):
        task = Task(title=title, description=description)
        task.save()
        return CreateTaskMutation(task=task)


class Query(graphene.ObjectType):
    all_tasks = graphene.List(TasksType)

    def resolve_all_tasks(self, info):
        return Task.objects.all()


class Mutation(graphene.ObjectType):
    create_task = CreateTaskMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)