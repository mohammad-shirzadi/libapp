from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from libapp.models import borrowModel



@receiver(post_migrate)
def groupsAndPermission(sender,**kwarg):
    user_group = Group.objects.get_or_create(name='user_group')[0]
    lib_group = Group.objects.get_or_create(name='lib_group')[0]

    contenttype = ContentType.objects.get_for_model(borrowModel)

    libperm = Permission.objects.get_or_create(
        codename='libperm',
        name='libperm',
        content_type=contenttype,
    )[0]
    normalperm = Permission.objects.get_or_create(
        codename='normalperm',
        name='normalperm',
        content_type=contenttype,
    )[0]

    user_group.permissions.add(normalperm)
    lib_group.permissions.add(libperm)
    