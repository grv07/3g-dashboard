from utils import create_object_permission


def create_course(sender, instance,  **kwargs):
    """
    Create a course permission that allow admin to permit a user for a course and
    Make a API POST call with course JSON.
    :param sender:
    :param instance:
    :param kwargs:
    :return: Call back API function when create a course
    """
    print('done ....', instance.title)
    from .serializers import CourseSerializer
    obj_serializer = CourseSerializer(instance)
    print(obj_serializer.data)
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_subject(sender, instance, **kwargs):
    """
    Create permission when create a subject of a course and
    Make a API POST call with subject JSON.
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when subject create
    """
    # TODO: Call api when module create
    from .serializers import SubjectSerializer
    obj_serializer = SubjectSerializer(instance)
    print(obj_serializer.data)
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_chapter(sender, instance, **kwargs):
    """
    Create permission when create a chapter of a subject and
    Make a API POST call with chapter JSON.
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when chapter create
    """
    # TODO: Call api when module create
    from .serializers import ChapterSerializer
    obj_serializer = ChapterSerializer(instance)
    print(obj_serializer.data)
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_topic(sender, instance, **kwargs):
    """
    Create permission when create a Topic of a chapter and
    Make a API POST call with topic JSON.
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when Topic create
    """
    # TODO: Call api when module create
    from .serializers import TopicSerializer
    obj_serializer = TopicSerializer(instance)
    print(obj_serializer.data)
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_module(sender, instance, **kwargs):
    """
    Create permission when create a Module of a topic and
    Make a API POST call with module-data JSON.
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when Module create
    """
    # TODO: Call api when module create
    from .serializers import ModuleDataSerializer
    obj_serializer = ModuleDataSerializer(instance)
    print(obj_serializer.data)
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])
