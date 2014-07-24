from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from app.models import Station


class Command(BaseCommand):
    help = 'Clean and generate stations.'

    option_list = BaseCommand.option_list + (
        make_option('-n', '--number', action="store", dest='number', default=50000),
    )

    def handle(self, *args, **options):

        errors = {
            "positive": u"Option `--number=...` must be only positive number.",
            "required": u"Option `--number=...` must be specified.",
        }

        if options['number'] is None:
            raise CommandError(errors["required"])

        if not options['number'].isdigit():
            raise CommandError(errors["positive"])

        number = int(options['number'])

        if not number:
            raise CommandError(errors["positive"])

        Station.objects.all().delete()
        for i in xrange(number):
            Station.objects.create_random_station()

        print u"Generated {0} stations.".format(number)