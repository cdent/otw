
import os
import shutil
import wsgi_intercept
import httplib2

from wsgi_intercept import httplib2_intercept

from tiddlywebplugins.utils import get_store

from tiddlyweb.config import config
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag

def setup_module(module):
    from tiddlyweb.web import serve
    def app_fn():
        return serve.load_app()
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8000, app_fn)

    if os.path.exists('store'):
        shutil.rmtree('store')

    store = get_store(config)
    module.http = httplib2.Http()

    store.put(Bag('stuff'))
    module.store = store


def test_get_wiki():
    response, content = http.request(
            'http://0.0.0.0:8000/bags/stuff/tiddlers.wiki')

    assert response['status'] == '200'
    assert 'otw.js' not in content

    response, content = http.request(
            'http://0.0.0.0:8000/bags/stuff/tiddlers.otw')

    assert response['status'] == '200'
    assert 'otw.js' in content

    response, content = http.request(
            'http://0.0.0.0:8000/bags/stuff/tiddlers.otw?download=file.html')

    assert response['status'] == '200'
    assert 'otw.js' not in content

def test_tiddler_presence():
    tiddler = Tiddler('dogma', 'stuff')
    tiddler.text = 'Ran over'
    store.put(tiddler)

    response, content = http.request(
            'http://0.0.0.0:8000/bags/stuff/tiddlers.otw')
    assert response['status'] == '200'
    assert 'Ran over' not in content

    response, content = http.request(
            'http://0.0.0.0:8000/bags/stuff/tiddlers.otw?download=file.html')
    assert response['status'] == '200'
    assert 'Ran over' in content
