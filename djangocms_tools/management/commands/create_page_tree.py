from __future__ import unicode_literals
import re
import random

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from cms.models import Page


class Command(BaseCommand):
    path_regex = re.compile('.{4}')

    def add_arguments(self, parser):
        parser.add_argument('--site-id', action='store', dest='site_id', default=1)
        parser.add_argument('--base-id', action='store', dest='base_id', default=None)
        parser.add_argument('--root-id', action='store', dest='root_id', default=None)
        parser.add_argument('--max-count', action='store', dest='max_count', default=200)
        parser.add_argument('--max-count-children', action='store', dest='max_count_children', default=4)
        parser.add_argument('--max-depth', action='store', dest='max_depth', default=10)
        parser.add_argument(
            '--language',
            action='store',
            dest='languages',
            default=[settings.LANGUAGE_CODE],
            nargs='+',
        )

    def handle(self, *args, **options):
        if options['base_id']:
            self.base_page = Page.objects.get(pk=options['base_id'])
        else:
            self.base_page = None

        if options['root_id']:
            root_page = Page.objects.get(pk=options['root_id'])
        else:
            root_page = None

        if 'all' in options['languages']:
            self.languages = [lang[0] for lang in settings.LANGUAGES]
        else:
            self.languages = options['languages']

        self.site = Site.objects.get(pk=options['site_id'])
        self.max_count_children = int(options['max_count_children'])
        self.max_depth = int(options['max_depth'])
        self.add_tree(
            count=int(options['max_count']),
            root=root_page,
            depth=1,
        )

    def add_tree(self, count, root=None, depth=1):
        CMS_GTE_35 = hasattr(Page, 'node')

        for node in range(0, count):
            new_page = Page(
                created_by='script',
                changed_by='script',
                in_navigation=True,
                template='INHERIT',
            )

            if CMS_GTE_35:
                parent_node = root.node if root else None
                new_page.set_tree_node(site=self.site, target=parent_node, position='last-child')
                new_page.save()
            else:
                new_page.site = self.site
                new_page.parent_id = getattr(root, 'pk', None)
                # This saves the page
                new_page = Page.add_root(instance=new_page)

                if root:
                    new_page = new_page.move(target=root.reload(), pos='last-child')

            try:
                node_path = new_page.node.path
            except AttributeError:
                node_path = new_page.path

            for language in self.languages:
                new_page.title_set.create(
                    language=language,
                    title=node_path,
                    slug=node_path,
                    path='/'.join(self.path_regex.findall(node_path)),
                )
            new_page.update_languages(self.languages)

            if self.base_page:
                for ph in self.base_page.placeholders.all():
                    new_ph = new_page.placeholders.create(slot=ph.slot)

                    for language in self.languages:
                        plugins = ph.get_plugins_list(language)

                        if plugins:
                            ph.copy_plugins(new_ph, language)
            else:
                new_page.rescan_placeholders()

            self.stdout.write("Created page %s" % node_path)

            if depth <= self.max_depth and bool(random.getrandbits(1)):
                self.add_tree(count=self.max_count_children, root=new_page, depth=depth + 1)
