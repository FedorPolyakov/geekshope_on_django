from django.core.management.commands.dumpdata import Command as Dumpdata
import json
import codecs

class Command(Dumpdata):
    pass
    # def handle(self, *app_labels, **options):
    #     with codecs.open('', 'w', encoding='utf-8') as file:
    #         json.dump(data, file, indent=2, ensure_ascii=False)