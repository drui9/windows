src := grammer
setup := grammer-setup

run: $(src)
	@~/.venv/bin/python $< < $<

clean:
	rm -rf **/*__pycache__ transport
