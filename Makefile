
PREFIX=/usr

all:
	@echo "If you wish to install it system wide, type 'sudo make install'"
	@echo "Uninstall with 'sudo make uninstall'"

install:
	rm -rf ${PREFIX}/share/screentime
	mkdir -p ${PREFIX}/share/screentime
	cp -av target ${PREFIX}/share/screentime/
	install -m 0644 src/main/icons/linux/512.png ${PREFIX}/share/pixmaps/screentime.png
	install -m 0644 -D -t ${PREFIX}/share/applications screentime.desktop
	@echo
	@echo "Install complete."

uninstall:
	rm -rf ${PREFIX}/share/screentime
	rm -rf ${PREFIX}/share/pixmaps/screentime.png
	rm -rf ${PREFIX}/share/applications/screentime.desktop
	@echo
	@echo "Uninstall complete."
