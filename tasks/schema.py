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


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=False)

    task = graphene.Field(TasksType)

    def mutate(self, info, id, title=None, description=None):
        task = Task.objects.get(id=id)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.save()
        return UpdateTaskMutation(task=task)


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    is_deleted = graphene.Boolean()

    def mutate(self, info, id):
        try:
            Task.objects.get(id=id).delete()
            is_deleted = True
        except Task.DoesNotExist:
            is_deleted = False

        return DeleteTaskMutation(is_deleted=is_deleted)


class Query(graphene.ObjectType):
    all_tasks = graphene.List(TasksType)

    def resolve_all_tasks(self, info):
        return Task.objects.all()


class Mutation(graphene.ObjectType):
    create_task = CreateTaskMutation.Field()
    update_task = UpdateTaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)