from django.core.management import BaseCommand
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from ...models import Institution


class Command(BaseCommand):
    help = gettext("Update education institutions distance to the nearest fiber optic node.")

    def add_arguments(self, parser):

        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help=_("Maximum number of records that can internally be processed as a single batch"),
        )

    def handle(self, *args, **options):
        updated = Institution.objects.refresh_fon_distances(batch_size=options["batch_size"])
        self.stdout.write(
            self.style.SUCCESS(
                _("%(updated)d objects updated") % {"updated": updated},
            )
        )
