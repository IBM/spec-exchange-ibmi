Name:           pixman
Version:        0.38.4
Release:        1
Summary:        Pixel manipulation library
Group:          System Environment/Libraries
License:        MIT
URL:            http://pixman.org/
Source0:        https://www.x.org/archive/individual/lib/%{name}-%{version}.tar.gz
BuildRequires:  pkg-config, gcc-aix, automake, autoconf, libpng-devel

%description
Pixman is a pixel manipulation library for X and cairo.


%package devel
Summary: Pixel manipulation library development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
Development library for %{name}.


%prep
%setup -q

%build

autoreconf -fiv
%configure \
    CPPFLAGS="-pthread" \
    LDFLAGS="-pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --disable-gtk
#    --disable-gcc-inline-asm \
#    --disable-timers

%make_build

# (gmake check || true)

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%{_libdir}/libpixman-1.so.0

%files devel
%defattr(-, qsys, *none)
%{_includedir}/pixman-1/pixman-version.h
%{_includedir}/pixman-1/pixman.h
%{_libdir}/libpixman-1.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Tue Jul 30 2019 Calvin Buckley <calvin@cmpct.info> - 0.38.4-1
- Bump version
- Fix source path and website URL
- Fix threads and dep chain

* Mon Mar 25 2019 Calvin Buckley <calvin@cmpct.info> - 0.38.0-1
- Update to latest pixman.
- De-AIXify package for PASE. This uses Rochester conventions now.

* Fri Feb 22 2013 Michael Perzl <michael@perzl.org> - 0.28.2-1
- updated to version 0.28.2

* Tue Nov 27 2012 Michael Perzl <michael@perzl.org> - 0.28.0-1
- updated to version 0.28.0

* Mon Aug 20 2012 Michael Perzl <michael@perzl.org> - 0.26.2-1
- updated to version 0.26.2

* Sun Jun 03 2012 Michael Perzl <michael@perzl.org> - 0.26.0-1
- updated to version 0.26.0

* Thu Feb 23 2012 Michael Perzl <michael@perzl.org> - 0.24.4-1
- updated to version 0.24.4

* Thu Oct 06 2011 Michael Perzl <michael@perzl.org> - 0.22.2-1
- updated to version 0.22.2

* Wed Jan 12 2011 Michael Perzl <michael@perzl.org> - 0.21.2-1
- updated to version 0.21.2

* Wed Nov 03 2010 Michael Perzl <michael@perzl.org> - 0.20.0-1
- updated to version 0.20.0

* Tue Sep 07 2010 Michael Perzl <michael@perzl.org> - 0.19.2-1
- updated to version 0.19.2

* Tue Sep 07 2010 Michael Perzl <michael@perzl.org> - 0.18.4-1
- updated to version 0.18.4

* Tue Sep 07 2010 Michael Perzl <michael@perzl.org> - 0.17.14-1
- updated to version 0.17.14

* Fri Feb 26 2010 Michael Perzl <michael@perzl.org> - 0.17.8-1
- updated to version 0.17.8

* Thu Feb 25 2010 Michael Perzl <michael@perzl.org> - 0.17.6-1
- updated to version 0.17.6

* Thu Nov 26 2009 Michael Perzl <michael@perzl.org> - 0.17.2-1
- updated to version 0.17.2

* Mon Nov 16 2009 Michael Perzl <michael@perzl.org> - 0.16.2-1
- updated to version 0.16.2

* Wed Sep 23 2009 Michael Perzl <michael@perzl.org> - 0.16.0-1
- updated to version 0.16.0

* Wed Jun 24 2009 Michael Perzl <michael@perzl.org> - 0.15.12-1
- updated to version 0.15.12

* Fri Sep 26 2008 Michael Perzl <michael@perzl.org> - 0.12.0-1
- updated to version 0.12.0

* Fri Jun 20 2008 Michael Perzl <michael@perzl.org> - 0.11.4-1
- updated to version 0.11.4

* Tue Jun 17 2008 Michael Perzl <michael@perzl.org> - 0.11.2-1
- updated to version 0.11.2

* Wed May 21 2008 Michael Perzl <michael@perzl.org> - 0.10.0-1
- first version for AIX V5.1 and higher

