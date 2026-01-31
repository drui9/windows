env := .venv
src := main.py
deps := requirements.txt
targ_name := decoded-binary
targ_dir := decoded

encode:
	./$(src) encode main.py image.png cipher.png

check:
	./$(src) encode main.py image.png cipher.png --capacity

decode: $(targ_dir)
	./$(src) decode cipher.png $(targ_dir)/$(targ_name)

run: $(src)
	@$(env)/bin/python $<

$(env):
	python3 -m venv .venv

install: $(deps) $(env)
	$(env)/bin/pip install -r $<

$(targ_dir):
	mkdir $@

clean:
	rm -rf cipher* decoded

