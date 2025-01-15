from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from libapp.models import borrowModel



@receiver(post_migrate)
def groupsAndPermission(sender,**kwarg):
    user_group = Group.objects.get_or_create(name='user_group')[0]
    lib_group = Group.objects.get_or_create(name='libgroup')[0]

    contenttype = ContentType.objects.get_for_model(borrowModel)

    can_view_own_borrows = Permission.objects.get_or_create(
        codename='can_view_own_borrow',
        name='can view own borrow',
        content_type=contenttype,
    )[0]
    can_view_all_borrows = Permission.objects.get_or_create(
        codename='can_view_all_borrow',
        name='can view all borrow',
        content_type=contenttype,
    )[0]

    user_group.permissions.add(can_view_own_borrows)
    lib_group.permissions.add(can_view_all_borrows,can_view_own_borrows)
    