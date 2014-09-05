all: addons

design/nautical.xmi: design/nautical.zargo
	-echo "REBUILD nautical.xmi from nautical.zargo. I cant do it"

addons: nautical

nautical: design/nautical.uml
	xmi2oerp -r -i $< -t addons -v 2
	mv addons/i18n addons/nautical/

clean:
	mv addons/nautical/i18n/ addons/
	sleep 1
	touch design/nautical.uml
