Name:           harfbuzz
Version:        2.6.0
Release:        1
Summary:        Text shaping library
License:        MIT
URL:            http://freedesktop.org/wiki/Software/HarfBuzz
Source0:        http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%{version}.tar.xz
Group:		System Environment/Libraries
Patch0:         harfbuzz-pase.diff

# XXX: We need for a better functioning harfbuzz:
#   - ICU (AIX LPP shipped with PASE is decrepit and requires oodles of patch)
#   - Graphite2 (option but assists fonts)
#   - GObject introspection
#   - Some tests would like a Cairo built with RSVG, but optional as of 2.5.3
BuildRequires:  freetype-devel, fontconfig-devel
BuildRequires:  cairo-devel
BuildRequires:  glib2-devel
BuildRequires:  libstdcplusplus-devel, automake, autoconf, gcc-cplusplus-aix
BuildRequires:  pkg-config >= 0.20

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Group:          Development/Libraries

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep

%setup -q
# TODO: Package ICU
if [ ! -d /QOpenSys/usr/icu4c/include/unicode/ ]; then
  echo "The version of ICU bundled with PASE is missing?"
  exit 1
fi
%patch0 -p1

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export ICU_LIBS="-L/usr/icu4c/lib -licui18n -licuuc -licudata"
export ICU_CFLAGS="-I/usr/icu4c/include"

# -Wno-attributes because otherwise it spams output

autoreconf -fiv .
%configure  \
        LDFLAGS="-pthread -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
        CPPFLAGS="-Wno-attributes" \
        --with-aix-soname=svr4 \
	--with-glib=yes --with-gobject=yes \
	--with-freetype=yes \
        --disable-silent-rules \
        --enable-shared  --disable-static

gmake %{?_smp_mflags}

# Seems to work except for symbol tests
#( gmake -k check || true )

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc COPYING NEWS AUTHORS README
%{_libdir}/libharfbuzz*.so.*

%files devel
%defattr(-, qsys, *none)
%doc %{_datadir}/gtk-doc
%{_bindir}/hb-*
%{_includedir}/harfbuzz/*.h
%{_libdir}/libharfbuzz*.so
%{_libdir}/pkgconfig/harfbuzz*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
* Mon Aug 19 2019 Calvin Buckley <calvin@cmpct.info> - 2.6.0-1
- Bump to 2.6.0
- Enable GObject (but not introspection, as that is a seperate package)

* Mon Aug 05 2019 Calvin Buckley <calvin@cmpct.info> - 2.5.3-1
- Bump to a modern version
- Update for PASE

* Fri Apr 22 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.2.6-1
- Update to 1.2.6
- Initial port to AIX

* Thu Oct 01 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.4-1
- Update to 1.0.4

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3
- Use license macro for COPYING

* Mon Aug 24 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.2-1
- Update to 1.0.2

* Wed Jul 29 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.1-1
- Update to 1.0.1

* Fri Jun 19 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.41-1
- Update to 0.9.41 upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.40-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.40-1
- Update to 0.9.40 upstream release

* Fri Mar 06 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.39-1
- Update to 0.9.39 upstream release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.9.38-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.9.38-3
- Bump for rebuild.

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.38-2
- Rebuild for libicu soname bump

* Tue Jan 27 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.38-1
- Update to 0.9.38 upstream release

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 0.9.37-2
- rebuild for ICU 54.1

* Tue Dec 23 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.37-1
- Update to 0.9.37 upstream release

* Tue Nov 25 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.36-1
- Update to 0.9.36 upstream release

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.9.35-3
- rebuild for ICU 53.1

* Mon Aug 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.35-1
- Update to 0.9.35 upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.34-1
- Update to 0.9.34 upstream release

* Tue Jul 29 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.33-1
- Update to 0.9.33 upstream release

* Fri Jul 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.32-1
- Update to 0.9.32 (have all the recent releases on koji)

* Thu Jul 17 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.31-1
- Update to 0.9.31 (have all the recent releases on koji)

* Fri Jul 11 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.30-1
- Update to 0.9.30 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.29-1
- Update to 0.9.29 upstream release

* Tue Apr 29 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.28-1
- Update to 0.9.28 upstream release

* Thu Mar 20 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.27-1
- Update to 0.9.27 upstream release

* Wed Feb 12 2014 Nils Philippsen <nils@redhat.com> - 0.9.26-3
- rebuild for new libicu

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 0.9.26-2
- Rebuilding for icu soname bump.

* Fri Jan 31 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.26-1
- Update to 0.9.26 upstream release

* Thu Dec 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.25-1
- Update to 0.9.25 upstream release

* Fri Nov 15 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.24-1
- Update to 0.9.24 upstream release

* Wed Oct 30 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.23-1
- Update to 0.9.23 upstream release

* Tue Oct 08 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.22-1
- Update to 0.9.22 upstream release

* Tue Sep 17 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.21-1
- Update to 0.9.21 upstream release

* Fri Aug 30 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.20-1
- Update to 0.9.20 upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.19-1
- Update to 0.9.19 upstream release

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.18-3
- Don't ship a (humongous) ChangeLog

* Fri Jun 07 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-2
- Resolves:rh#971795:Merge -icu-devel subpackage into -devel subpackage

* Wed Jun 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-1
- Update to 0.9.18 upstream release

* Tue May 21 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.17-1
- Update to 0.9.17 upstream release

* Sat Apr 20 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.16-1
- Update to 0.9.16 upstream release

* Fri Mar 22 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.14-1
- Update to 0.9.14 upstream release

* Tue Feb 26 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.13-1
- Update to 0.9.13 upstream release

* Wed Jan 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-6
- Kill icu-config hack and rebuild against new icu again

* Tue Jan 29 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-5
- Resolves:rh#905334 - Please rebuild harfbuzz for new graphite-1.2.0

* Sun Jan 27 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-4
- Resolves:rh#904700-Enable additional shaper graphite2

* Sat Jan 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-3
- Add "icu-config --cppflags" to compiler flags to fix build

* Fri Jan 25 2013 Orion Poplawski <orion@cora.nwra.com> - 0.9.12-2
- Rebuild for libicu 50

* Sun Jan 20 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-1
- Update to 0.9.12 upstream release

* Fri Jan 11 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.11-1
- Update to 0.9.11 upstream release

* Thu Jan 03 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.10-1
- Update to 0.9.10 upstream release

* Thu Dec 06 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.9-1
- Update to 0.9.9 upstream release

* Wed Dec 05 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.8-1
- Update to 0.9.8 upstream release

* Wed Nov 21 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.7-1
- Update to 0.9.7 upstream release

* Wed Nov 14 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.6-1
- Update to 0.9.6 upstream release

* Mon Oct 15 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.5-1
- Update to 0.9.5 upstream release

* Mon Sep 10 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.4-1
- Update to 0.9.4 upstream release

* Sun Aug 19 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.3-1
- Update to 0.9.3 upstream release

* Mon Aug 13 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.2-1
- Update to 0.9.2 upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.0-6
- Rebuilt for libicu 49

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.0-4
- Rebuild for new libpng

* Sat Sep 10 2011 Kalev Lember <kalevlember@gmail.com> - 0.6.0-3
- Rebuilt for libicu 4.8

* Thu Jun 16 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-2
- Moved hb-view to -devel subpackage (#713126)

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-1
- Initial RPM release

