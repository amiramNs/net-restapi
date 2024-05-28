from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from project.apps.profile.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(f">>> {self.style.SUCCESS('Start seeding...')}\n")
        try:
            # group admin
            user_admin_permission = Permission.objects.get_or_create(
                codename='user_admin',
                name='Can handle project.',
                content_type=ContentType.objects.get_for_model(User)
            )[0]
            admin_group, admin_group_created = Group.objects.get_or_create(name='net_admin')
            if admin_group_created:
                admin_group.permissions.add(user_admin_permission)

            # group operator
            user_operator_permission = Permission.objects.get_or_create(
                codename='user_operator',
                name='Can handle project.',
                content_type=ContentType.objects.get_for_model(User)
            )[0]
            operator_group, operator_group_created = Group.objects.get_or_create(name='net-operator')
            if operator_group_created:
                operator_group.permissions.add(user_operator_permission)

            # group repairman
            user_repairman_permission = Permission.objects.get_or_create(
                codename='user_repair',
                name='Can handle project.',
                content_type=ContentType.objects.get_for_model(User)
            )[0]
            repair_group, repiar_group_created = Group.objects.get_or_create(name='net-repairman')
            if repiar_group_created:
                repair_group.permissions.add(user_repairman_permission)

        except Exception as e:
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS('\n\u2713 successfully.'))
