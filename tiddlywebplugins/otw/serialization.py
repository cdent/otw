"""
Serialize into a tiddlywiki wiki, leaving out most of the tiddlers
so they can be loaded later by something else.

The missing tiddlers are placed in a tiddler called LazyTiddlers.
"""

from tiddlywebwiki.serialization import (
        Serialization as CoreSerialization)
from tiddlywebplugins.lazy.serialization import (
        Serialization as WikiSerialization)
from tiddlyweb.web.util import tiddler_etag, get_route_value, server_base_url
import simplejson

WIKI = ''

class Serialization(WikiSerialization):

    def _create_tiddlers(self, title, tiddlers):
        download = self.environ['tiddlyweb.query'].get('download', [None])[0]
        if download:
            return CoreSerialization._create_tiddlers(self, title, tiddlers)
        else:
            return WikiSerialization._create_tiddlers(self, title, tiddlers)

    def _get_container(self):
        routing_args = self.environ.get('wsgiorg.routing_args', ([], {}))[1]
        container_name = False
        container_type = 'bags'
        if routing_args:
            if 'recipe_name' in routing_args:
                container_name = get_route_value(self.environ, 'recipe_name')
                container_type = 'recipes'
            elif 'bag_name' in routing_args:
                container_name = get_route_value(self.environ, 'bag_name')
        if container_name:
            return "%s/%s" % (container_type, container_name)
        else:
            return ""

    def _get_config(self):
        json = {"workspace": self._get_container(),
                "host": server_base_url(self.environ)}
        return '''\
<script id="tiddlywikiconfig" type="application/json">
%s
</script>
''' % (simplejson.dumps(json))

    def _get_wiki(self):
        """
        Read base_tiddlywiki from its location.
        """
        download = self.environ['tiddlyweb.query'].get('download', [None])[0]
        if download:
            return CoreSerialization._get_wiki(self)

        global WIKI
        if not WIKI:
            base_tiddlywiki = open(
                self.environ['tiddlyweb.config']['base_otw'])
            wiki = base_tiddlywiki.read()
            base_tiddlywiki.close()
            wiki = wiki.replace('@@bagpath@@',
                    '%s/bags/common/tiddlers' % server_base_url(self.environ))
            wiki = unicode(wiki, 'utf-8')
            WIKI = wiki
        return WIKI.replace('@@otwconfig@@', self._get_config())
