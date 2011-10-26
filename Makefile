
RESOURCES_DIR=tiddlywebplugins/otw/resources
SOURCES_DIR=sources

clean:
	rm -rf $(RESOURCES_DIR)/* || true
	rm $(SOURCES_DIR)/*.js || true
	find . -name "*.pyc" -exec rm {} \; || true

resources: remotes
	cook $$PWD/lib/otw.recipe -d $$PWD/$(RESOURCES_DIR) -o otw.html
	cook $$PWD/lib/otw.js.recipe -d $$PWD/$(SOURCES_DIR) -o otw.js.js -j
	./cacher

remotes:
	wget https://raw.github.com/TiddlyWiki/tiddlywiki/master/jquery/jquery.js -O $(SOURCES_DIR)/jquery.js.js
	wget https://raw.github.com/TiddlyWiki/tiddlywiki/master/jquery/plugins/jQuery.twStylesheet.js -O $(SOURCES_DIR)/jQuery.twStylesheet.js.js
