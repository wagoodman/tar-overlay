TAROVERLAY_VERSION  =  0.1
# $(shell date +%Y%m%d)
TAROVERLAY_BUILDID  = 0
# $(shell date +%H%M%S)
SPEC_FILE  = rpm/SPECS/tar-overlay.spec

.PHONY: all rpm clean

all: clean rpm

rpm: ;\
  rpmbuild -bb --define="Version $(TAROVERLAY_VERSION)"  --define="Release $(TAROVERLAY_BUILDID)"  $(SPEC_FILE) && \
  mv rpm/RPMS/noarch/*.rpm . ;

clean: ;\
  rm -f ./*.rpm ;
