
from tiddlywebwiki.instance import (instance_config, store_contents,
        store_structure)


store_contents['common'] = ['sources/index.recipe']

instance_config = {
    'system_plugins': ['tiddlywebwiki', 'tiddlywebplugins.otw'],
    'twanager_plugins': ['tiddlywebwiki', 'tiddlywebplugins.otw'],
}
