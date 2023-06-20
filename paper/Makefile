all:
	docker run --rm --volume $(PWD):/data --volume $(PWD)/../media:/media \
	--user $(id -u):$(id -g) --env JOURNAL=joss openjournals/inara
