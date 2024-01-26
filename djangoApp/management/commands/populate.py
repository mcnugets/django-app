from django.core.management.base import BaseCommand, CommandError
import json
"""

Description: This file contains custom django-admin command for populating json file with relevant data
"""

class Command(BaseCommand):
    help = 'Lil bro tryna fill the database up if ya know what I mean'

    def add_arguments(self, parser):
        parser.add_argument('load', nargs='+', help="populate your fixture file")

    def create_data(self, model_name, pk, fields):
        return {
            'model': model_name,
            'pk': pk,
            'fields': fields
        }

    def handle(self, *args, **options):
        tag = 'djangoApp.tag'
        tags = [self.create_data(tag, 1,
                                 {'tag_name': 'fullhd'}),
                self.create_data(tag, 2,
                                 {'tag_name': 'm3'})]

        cat = self.create_data('djangoApp.Category', 1,
                               {'cat_name': 'phone'})
        prod = self.create_data('djangoApp.Product', 1,
                                {'p_name': 'iphone 20',
                                 'product_tag': [1, 2],
                                 'cat': 1})

        with open('djangoApp/fixtures/test_data.json', 'wt', ) as file:
            json.dump([tags[0], tags[1], cat, prod], file, indent=2)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully saved the file in {file}')
            )
