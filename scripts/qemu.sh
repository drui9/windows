#!/bin/bash
if [ -d alpine ]; then
	qemu-system-x86_64 -machine q35 -m 1024 -smp cpus=3 -cpu qemu64 -drive if=pflash,format=raw,read-only=on,file=$PREFIX/share/qemu/edk2-x86_64-code.fd -netdev user,id=n1,dns=8.8.8.8,hostfwd=tcp::2222-:22 -device virtio-net,netdev=n1 -nographic alpine/alpine.img
else
	echo 'press RETURN to install alpine linux in qemu'
	echo 'press Ctrl+q to quit'
	read
	pkg update && pkg upgrade;
	pkg install qemu-utils qemu-common qemu-system-x86_64-headless wget -y
	git clone https://github.com/drui9/docker-in-termux;
	echo 'read docker-in-termux/README.md to complete alpine in qemu setup'
fi

