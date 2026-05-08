# src := script
src := grammer

run: $(src)
	@sha512sum $<|./$<

clean:
	rm -rf **/*__pycache__ transport
