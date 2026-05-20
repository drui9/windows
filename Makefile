src := boot.py
termux := termux.tar
turmoid := turmoid.tar
files := .nomedia .vimrc .vim .config/nvim .oh-my-zsh .zshrc .venv .git .gitconfig .gitignore .hushlogin LICENSE Makefile README.md requirements.txt projects src $(src) scripts turmoid.png startq

run: $(src)
	@clear;~/.venv/bin/python $< < $<

list:
	~/.venv/bin/pip list

export: $(termux) $(turmoid)
	mv $^ storage/documents/binaries/

$(termux):
	termux-backup $@

$(turmoid): $(files)
	tar -cf $@ $^

clean:
	rm -rf **/*__pycache__ .*history .local .cache .zcomp* .wget-hsts

