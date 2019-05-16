.PHONY: test

test:
	fswatch -e '.*' -i '\.py$$' -o . | xargs -n1 -I{} green -vv -r
