import random
from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Report

fake = Faker('id_ID')

class Command(BaseCommand):
    help = 'Generate fake reports'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int)

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']

        status_choices = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
        categories = ['Jalan Rusak', 'Sampah', 'Lampu Mati', 'Drainase', 'Keamanan']

        for _ in range(num_records):
            Report.objects.create(
                title=f"Laporan {fake.street_name()}",
                category=random.choice(categories),
                description=fake.text(),
                location=fake.address(),
                status=random.choice(status_choices),
            )

        self.stdout.write(self.style.SUCCESS(f'{num_records} data berhasil dibuat!'))