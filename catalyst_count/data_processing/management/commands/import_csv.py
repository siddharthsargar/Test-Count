import csv
from django.core.management.base import BaseCommand
from data_processing.models import Company

class Command(BaseCommand):
    help = 'Import CSV data into Company model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Company.objects.create(
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=self._parse_int(row['year_founded']),
                    industry=row['industry'],
                    size_range=row['size_range'],
                    locality=row['locality'],
                    country=row['country'],
                    linkedin_url=row['linkedin_url'],
                    current_employee_estimate=self._parse_int(row['current_employee_estimate']),
                    total_employee_estimate=self._parse_int(row['total_employee_estimate'])
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported CSV data'))

    def _parse_int(self, value):
        """Convert value to an integer or return None if value is empty or invalid."""
        if value.strip() == '':
            return None
        try:
            return int(value)
        except ValueError:
            return None
