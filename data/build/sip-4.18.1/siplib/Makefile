TARGET = sip.so
OFILES = siplib.o apiversions.o descriptors.o qtlib.o threads.o objmap.o voidptr.o array.o bool.o
HFILES = sip.h sipint.h array.h 

CC = gcc
CXX = g++
LINK = g++
CPPFLAGS = -DNDEBUG -I. -I/usr/include/python2.7
CFLAGS = -pipe -fPIC -O2 -Wall -W
CXXFLAGS = -pipe -fPIC -O2 -Wall -W
LFLAGS = -shared -Wl,--version-script=sip.exp
LIBS = 
.SUFFIXES: .c .o .cpp .cc .cxx .C


.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cc.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cxx.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.C.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.c.o:
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(TARGET)

$(OFILES): $(HFILES)

$(TARGET): $(OFILES)
	@echo '{ global: initsip; local: *; };' > sip.exp
	$(LINK) $(LFLAGS) -o $(TARGET) $(OFILES) $(LIBS)

install: $(TARGET)
	@test -d $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages || mkdir -p $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages
	cp -f $(TARGET) $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages/$(TARGET)
	strip $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages/$(TARGET)
	@test -d $(DESTDIR)/home/cetti/.virtualenvs/nostalg/include/python2.7 || mkdir -p $(DESTDIR)/home/cetti/.virtualenvs/nostalg/include/python2.7
	cp -f "/home/cetti/colegio/Programacion I/EjerciciosQt/Estacionamiento Final/data/build/sip-4.18.1/siplib/sip.h" $(DESTDIR)/home/cetti/.virtualenvs/nostalg/include/python2.7/sip.h
	@test -d $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages || mkdir -p $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages
	cp -f "/home/cetti/colegio/Programacion I/EjerciciosQt/Estacionamiento Final/data/build/sip-4.18.1/sip.pyi" $(DESTDIR)/home/cetti/.virtualenvs/nostalg/lib/python2.7/site-packages/sip.pyi

clean:
	-rm -f $(TARGET)
	-rm -f siplib.o
	-rm -f apiversions.o
	-rm -f descriptors.o
	-rm -f qtlib.o
	-rm -f threads.o
	-rm -f objmap.o
	-rm -f voidptr.o
	-rm -f array.o
	-rm -f bool.o
	-rm -f sip.exp
