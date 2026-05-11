# src := script
src := grammer

run: $(src)
	@python $< < $<

clean:
	rm -rf **/*__pycache__ transport
