src := grammer
setup := grammer-setup
files := .bashrc .config .gitconfig .gitignore .gnupg .hushlogin exported .ssh LICENSE Makefile README.md grammer* requirements.txt src

run: $(src)
	@~/.venv/bin/python $< < $<

export:
	tar -cf grammer-01.tar $(files)

clean:
	rm -rf **/*__pycache__ transport .*history

