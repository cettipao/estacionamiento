
all:
	@(cd sipgen; $(MAKE))
	@(cd siplib; $(MAKE))

install:
	@(cd sipgen; $(MAKE) install)
	@(cd siplib; $(MAKE) install)
	@test -d $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages || mkdir -p $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages
	cp -f sipconfig.py $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages/sipconfig.py
	cp -f "/home/cetti/colegio/Programacion I/EjerciciosQt/Estacionamiento Final/data/build/sip-4.18.1/sipdistutils.py" $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages/sipdistutils.py

clean:
	@(cd sipgen; $(MAKE) clean)
	@(cd siplib; $(MAKE) clean)
