from django.core.management.base import BaseCommand, CommandError
from quickstart.models import Advice


class Command(BaseCommand):
    help = 'Hiding the specified advice'

    def add_arguments(self, parser):
        parser.add_argument('advice_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for advice_id in options['advice_ids']:
            try:
                poll = Advice.objects.get(pk=advice_id)
            except Advice.DoesNotExist:
                raise CommandError('Advice "%s" does not exist' % advice_id)

            poll.is_hidden = True
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully hide advice "%s"' % advice_id))
