import logging

from csv import DictReader
from django.core.management import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    """
    Скрипт загружает тестовые данные из csv файлов в БД.

    Для использования воспользуйтесь командой:
    python manage.py load_csv
    """

    def handle(self, *args, **options):

        try:
            logging.debug('Данные импортируются...')

            for row in DictReader(open('static/data/ingredients.csv',
                                       encoding='utf8')):
                ingredients = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']
                )
                ingredients.save()

            logging.debug('Данные из ingredients.csv импортированы.')

            logging.debug('Все данные импортированы!')

        except Exception as error:
            logging.error(f'Произошла ошибка {error}.\n' 
                          'Данные не импортированы!')
