Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 1.2.11
Release: 0seiden
License: LGPL-2.1-or-later AND GPL-2.0-or-later
URL: http://www.freetds.org/

Source0: ftp://ftp.freetds.org/pub/freetds/stable/freetds-%{version}.tar.bz2

# Use OpenSSL instead of gnutls
BuildRequires: unixODBC-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: libiconv-devel
#BuildRequires: gnutls-devel
#BuildRequires:  krb5-devel
#BuildRequires: libgcrypt-devel
BuildRequires: libtool
#BuildRequires: doxygen, docbook-style-dsssl

Requires:       libct4 = %{version}-%{release}
Requires:       libsybdb5 = %{version}-%{release}
Requires:       libtdsodbc0 = %{version}-%{release}	

%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.


# XXX: It appears that FreeTDS can operate without config?
# This provides the package for all the libraries either way;
# if they do need it, we'll just mark freetds-config as a dep on all
%package config
Summary:        A free re-implementation of the TDS (Tabular Data Stream) protocol
License:        LGPL-2.1-or-later
Obsoletes:      libfreetds < %{version}
Provides:       %{name} = %{version}
Provides:       libfreetds = %{version}
Obsoletes:      %{name} < %{version}

%description config
FreeTDS is a project to document and implement the TDS (Tabular Data Stream)
protocol. TDS is used by Sybase and Microsoft for client to database server
communications.

This subpackage contains default configuration files and documentation for
them.


%package -n libct4
Summary:        FreeTDS standalone driver with modern API
License:        LGPL-2.1-or-later

%description -n libct4
ct-lib refers to Sybase's second-generation API, which fixes a number
of implementation and conceptual gaps in db-lib (libsybdb). libct is
not the most complete implementation yet.

%package -n libsybdb5
Summary:        FreeTDS standalone driver with classic API
License:        LGPL-2.1-or-later

%description -n libsybdb5
db-lib is the oldest and simplest API, and the only API supported by
both vendors, which has some relevance when porting applications that
use the vendors' libraries. db-lib was the first API implemented by
FreeTDS, and is still the best one supported. Anything that can be
done in FreeTDS can be done through db-lib.

%package    -n libtdsodbc0
Summary:        FreeTDS ODBC Driver for unixODBC
License:        LGPL-2.1-or-later
Requires:       unixODBC
Requires(post): %{_bindir}/odbcinst
Requires(preun): %{_bindir}/odbcinst

%description -n libtdsodbc0
The ODBC drivers is the FreeTDS's project most recent addition. Its
chief advantage is that it makes FreeTDS servers look like other ODBC
servers, a big help to people who know ODBC and/or write applications
for several kinds of servers.


%package devel
Summary: Header files and development libraries for %{name}
Requires:       libct4 = %{version}-%{release}
Requires:       libsybdb5 = %{version}-%{release}
Requires:       libtdsodbc0 = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.


%package doc
Summary: Development documentation for %{name}
License:        LGPL-2.1-or-later AND GPL-2.0-or-later

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.


%prep 
%setup -q

#  correct perl path
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl

chmod -x samples/*.sh


%build 

autoreconf -fiv .
%configure \
	LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
	--with-aix-soname=svr4 \
	--enable-shared \
	--disable-static \
	--with-tdsver="auto" \
	--with-unixodbc="%{_prefix}" \
	--enable-msdblib \
	--enable-sybase-compat \
	--with-openssl="%{_prefix}" \
	--with-libiconv-prefix="%{_prefix}" \
	--disable-krb5

%make_build


%install 

%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
chmod -x $RPM_BUILD_ROOT%{_sysconfdir}/*

rm -f samples/Makefile* samples/*.in samples/README

mv -f samples/unixodbc.freetds.driver.template \
	samples/unixodbc.freetds.driver.template-%{bits}

mkdir samples-odbc
mv -f samples/*odbc* samples-odbc

#  deinstall it for our own way...
mv -f $RPM_BUILD_ROOT%{_docdir}/%{name} docdir
find docdir -type f -print0 | xargs -0 chmod -x


# Integrate FreeTDS into unixODBC
%post -n libtdsodbc0
# appearantly you have to specify the full path, bizarre
echo "[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | %{_bindir}/odbcinst -i -d -r || true
echo "[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | %{_bindir}/odbcinst -i -d -r || true

%preun -n libtdsodbc0
%{_bindir}/odbcinst -u -d -n 'FreeTDS'
%{_bindir}/odbcinst -u -d -n 'SQL Server'


%files
%defattr(-, qsys, *none)
%{_bindir}/*
%doc AUTHORS.md BUGS.md COPYING.txt NEWS.md README.md TODO.md doc/*.html
%doc doc/userguide doc/images
%{_mandir}/man1/*


%files config
%defattr(-, qsys, *none)
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man5/*


%files -n libct4
%defattr(-, qsys, *none)
%license COPYING*
%{_libdir}/libct.so.4*


%files -n libsybdb5
%defattr(-, qsys, *none)
%license COPYING*
%{_libdir}/libsybdb.so.5*


%files -n libtdsodbc0
%defattr(-, qsys, *none)
%license COPYING*
%doc samples-odbc
%{_libdir}/libtdsodbc.so.*

 
%files devel 
%defattr(-, qsys, *none)
%doc samples
%{_libdir}/*.so
%exclude %{_libdir}/libtdsodbc.so
%{_includedir}/*


%files doc
%defattr(-, qsys, *none)
%doc doc/reference
 

%changelog
* Thu Nov 19 2020 Calvin Buckley <calvin@seidengroup.com> - 1.2.11-0seiden
- Port to PASE
- Bump
- This is a chimera of the Fedora 33 and openSUSE Tumbleweed package, but is
  mostly Fedora with the openSUSE libraries, SPDX, and ODBC, but Fedora main
  package name and documentation conventions.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov  7 2019 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.1.20-1
- update to 1.1.20

* Tue Jul  9 2019 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.1.11-1
- Upgrade to 1.1.11 (#1728191)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.00.38-8
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.00.38-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.00.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.00.38-1
- Update to 1.00.38
- split freetds-libs package (for multiarch support)
- change default tds vesrion to auto
- move odbc plugin from devel to libs package (#1449881)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.95.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.95.81-2
- Rebuild for readline 7.x

* Wed Feb 10 2016 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.95.81-1
- update to 0.95.81
- use proper rpm macros to determine 64 bit arches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.95.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.95.19-1
- Upgrade to 0.95.19

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-16.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-15.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-14.git0a42888
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tomáš Mráz <tmraz@redhat.com> - 0.91-13.git0a42888
- Rebuild for new libgcrypt

* Fri Jan 10 2014 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-12.git0a42888
- add ppc64le to the list of 64bit arches (#1051199)

* Tue Dec  3 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-11.git0a42888
- update to the latest git source for 0_91 branch
- fix format-security issue (#1037071)

* Thu Aug 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-10.git748aa26
- update to the latest git source for 0_91 branch
- fix #999696

* Wed Aug  7 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-9.gitb760a89
- update to the latest git source for 0_91 branch
- fix #992295, #993762

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-7.gitf3ae29d
- add aarch64 to the list of 64bit arches (#966129)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-5.gitf3ae29d
- update to the latest git source for 0_91 branch
- fix #870483

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-3
- Enable Kerberos support (#797276)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-1
- Upgrade to 0.91
- Drop shared-libtds support

* Wed Mar  9 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.3.20110306dev
- update to the latest stable snapshot 0.82.1.dev.20110306
- make build with shared-libtds conditional
- disable shared-libtds patch by default (seems noone uses it for now)

* Mon Feb 14 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.2.20100810dev
- fix again shared-libtds patch to provide increased library version

* Thu Feb 10 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.1.20100810dev
- update to the latest stable snapshot 0.82.1.dev.20100810
- fix shared-libtds patch to provide properly library names

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-5
- add upstream patch cspublic.BLK_VERSION_150.patch (#492393)

* Tue Feb 24 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-4
- fix autoconf data for libtool2 (patch by Tom Lane <tgl@redhat.com>)

* Fri Jan 30 2009 Karsten Hopp <karsten@redhat.com> 0.82-3
- add s390x to 64 bit archs

* Sun Jan 11 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-3
- Use gnutls for SSL (#479148)

* Tue Jun 17 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-2
- Continue to provide an internal libtds library as public
  (patch from Hans de Goede, #451021). This shared library is needed
  for some existing applications (libgda etc.), which still use it directly.

* Mon Jun  9 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-1
- Upgrade to 0.82

* Tue Feb 26 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-11
- fix "64 or 32 bit" test (#434975)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.64-10
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-9
- drop "Obsoletes:" from -doc subpackage to avoid extra complexity.

* Fri Jan 25 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-8
- resolve multiarch conflicts (#341181):
  - split references to separate freetds-doc subpackage
  - add arch-specific suffixes for arch-specific filenames in -devel
  - add wrapper for tds_sysdep_public.h
- add readline support (#430196)

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.64-7
- Rebuild for selinux ppc32 issue.

* Thu Aug 16 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to "LGPLv2+ and GPLv2+"

* Fri Jun 15 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-6 
- bump release to provide update path over Livna

* Wed Jun 13 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-5
- spec file cleanups
- allowed for Fedora (no patent issues exist), clarification by
  James K. Lowden <jklowden [AT] freetds.org>
- approved for Fedora (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Wed Aug  2 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- approved for Livna (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Tue Aug  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- add patch to fix sed scripts in the doc/ Makefile
- avoid using rpath in binaries
- cleanup in samples/ dir

* Thu Jul 27 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-3
- rebuild userguide too.
- move reference docs to -devel

* Mon Jul 24 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-2
- Properly clear extra executable bit in source
- Regenerate docs using doxygen

* Thu Jul 20 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-1
- Upgrade to 0.64
- Some spec file and distro cleanups

* Tue Sep 20 2005 V.C.G.Yeah <VCGYeah@iname.com> - 0.63-1
- Upgrade to 0.63
- spec file cleanups
- build static libs conditional

* Thu Sep  2 2004 V.C.G.Yeah <VCGYeah@iname.com> - 0.62.4-1Y
- Updated to release 0.62.4.
- Leave includes in system default include dir (needed for php-mssql build)

* Mon May 17 2004 Dag Wieers <dag@wieers.com> - 0.62.3-1
- Updated to release 0.62.3.

* Wed Feb 04 2004 Dag Wieers <dag@wieers.com> - 0.61.2-0
- Added --enable-msdblib configure option. (Dean Mumby)
- Updated to release 0.61.2.

* Fri Jun 13 2003 Dag Wieers <dag@wieers.com> - 0.61-0
- Initial package. (using DAR)
