# src := script
src := grammer

run: $(src)
	@./$<

clean:
	rm -rf **/*__pycache__ transport
