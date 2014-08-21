all: addons

design/nautical.xmi: design/nautical.zargo
	-echo "REBUILD nautical.xmi from nautical.zargo. I cant do it"

addons: nautical

nautical: design/nautical.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/nautical/*
	sleep 1
	touch design/nautical.uml
