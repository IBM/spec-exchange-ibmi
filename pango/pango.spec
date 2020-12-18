# Dependencies versions, last updated for pango 1.40.1
%define glib2_version 2.33.12
%define harfbuzz_version 0.9.30
%define fontconfig_version 2.10.91
%define freetype_version 2.1.5
%define xft_version 2.0.0
%define cairo_version 1.12.10

Summary: System for layout and rendering of internationalized text
Name: pango
# XXX: Not bumping up to >1.40 just yet due to test fails in 1.42 and FT removal in 1.44
Version: 1.40.14
Release: 0
License: GNU LGPL 2.1
Url: 	 http://www.pango.org
Source0: http://ftp.gnome.org/pub/GNOME/sources/pango/1.40/%{name}-%{version}.tar.xz
# This is taken from gtk-docs 1.30, which is licensed under the GPL.
# When gtk-doc is packaged, remove this hack.
Patch0: gtk-doc.m4.diff
Group:   System Environment/Libraries

BuildRequires: pkg-config
# We need glib2 binaries for the GObject cruft
BuildRequires: glib2, glib2-devel >= %{glib2_version}
BuildRequires: libXrender-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: harfbuzz-devel >= %{harfbuzz_version}
BuildRequires: libXft-devel >= %{xft_version}
BuildRequires: libX11-devel
# XXX: Next bump we need fribidi

# let rpm wire up lib deps
Requires: glib2 >= %{glib2_version}

%description 
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package devel
Summary: System for layout and rendering of internationalized text
Group: Development/Libraries
Requires: pango = %{version}-%{release}

%description devel
The pango-devel package includes the header files and developer docs
for the pango package.

%prep
%setup -q
# stupid hack to work around having to install the entire gtk-doc dist
%patch0 -p1

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -I. -fiv .
# all source for struct tms
%configure \
  CPPFLAGS="-D_ALL_SOURCE" \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --with-xft \
  --enable-shared --disable-static

%make_build

# gmake check || true

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc README AUTHORS COPYING NEWS
%{_mandir}/man1/*
%{_bindir}/pango*
%{_libdir}/libpango*.so.0

%files devel
%defattr(-, qsys, *none)
%doc %{_datadir}/gtk-doc/html/pango/*
%{_includedir}/pango-1.0/pango/*.h
%{_libdir}/libpango*.so
%{_libdir}/pkgconfig/pango*.pc

%changelog
* Mon Aug 05 2019 Calvin Buckley <calvin@cmpct.info> - 1.40.14-1
- Bump
- PASE

* Mon Apr 25 2016 Matthieu Sarter <matthieu.sarter@atos.net> - 1.40.1-1
- Update to version 1.40.1

* Mon Oct 07 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.30.1-2
- Rebuild due to libX11 issue

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.30.1-1
- Update to version 1.30.1

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.28.3-4
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.28.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 8 2011 Gerard Visiedo <gerard.visiedo@bull.fnet> 1.28.3-2
- Add libraries 64-bit

* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.28.3-1
- update to version 1.28.3

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.10.0

*  Wed Aug 10 2005  BULL
 - Release  3

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 1.8.1
 - Fix Xscreensaver-demo core at initialisation on AIX

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 1.6.0

*  Wed Jul 28 2004  BULL
 - Release  2
 - fix bug causing the generation of a core file

