
from tiddlywebplugins.instancer.util import get_tiddler_locations
from tiddlywebplugins.otw.instance import store_contents

try:
    from pkg_resources import resource_filename
except ImportError:
    from tiddlywebplugins.utils import resource_filename

PACKAGE_NAME = 'tiddlywebplugins.otw'
BASE_OTW = resource_filename(PACKAGE_NAME, 'resources/otw.html')

config = {
        'instance_tiddlers': get_tiddler_locations(store_contents, PACKAGE_NAME),
        'base_otw': BASE_OTW,
        'extension_types': {
            'otw': 'text/x-otw',
            },
        'serializers': {
            'text/x-otw': ['tiddlywebplugins.otw.serialization',
                'text/html; charset=UTF-8'],
            },
        }
