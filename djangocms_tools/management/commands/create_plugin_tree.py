from django.core.management import BaseCommand

from cms.models import CMSPlugin, Page


def create_plugins(page, count=5):
    placeholders = page.placeholders.all()

    for placeholder in placeholders:
        for language in page.get_languages():
            data = {
                'language': language,
                'plugin_type': 'CMSToolsNode',
                'placeholder': placeholder,
            }

            for i in range(0, count):
                # Depth 1
                parent = CMSPlugin.add_root(position=i, **data)
                # Depth 2
                child = parent.add_child(position=i, parent=parent, **data)
                # Depth 3
                child.add_child(position=i, parent=child, **data)


class Command(BaseCommand):
    help = 'Creates plugins for all pages in the db'

    # TODO
    # Add configurable plugin count
    # Add option to publish page afterwards

    def handle(self, *args, **options):
        for page in Page.objects.drafts():
            try:
                node_path = page.node.path
            except AttributeError:
                node_path = page.path
            create_plugins(page)
            self.stdout.write("Created plugins for page %s" % node_path)
        self.stdout.write('Plugins created\n')
