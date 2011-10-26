.PHONY: clean dev resources remotes test

RESOURCES_DIR=tiddlywebplugins/otw/resources
SOURCES_DIR=sources

clean:
	rm -rf $(RESOURCES_DIR) || true
	rm $(SOURCES_DIR)/*.js || true
	find . -name "*.pyc" -exec rm {} \; || true

dev:
	@(./otwinstance dev && \
	cd dev && \
	ln -s ../mangler.py && \
	ln -s ../tiddlywebplugins && \
	echo "import mangler" >> tiddlywebconfig.py && \
	twanager bag stuff </dev/null && \
	echo "start up the server and visit http://0.0.0.0:8080/bags/stuff/tiddlers.otw")

resources: remotes
	mkdir -p $(RESOURCES_DIR) || true
	cook $$PWD/lib/otw.recipe -d $$PWD/$(RESOURCES_DIR) -o otw.html
	cook $$PWD/lib/otw.js.recipe -d $$PWD/$(SOURCES_DIR) -o otw.js.js -j
	./cacher

remotes:
	wget https://raw.github.com/TiddlyWiki/tiddlywiki/master/jquery/jquery.js -O $(SOURCES_DIR)/jquery.js.js
	wget https://raw.github.com/TiddlyWiki/tiddlywiki/master/jquery/plugins/jQuery.twStylesheet.js -O $(SOURCES_DIR)/jQuery.twStylesheet.js.js

test:
	py.test -x test
