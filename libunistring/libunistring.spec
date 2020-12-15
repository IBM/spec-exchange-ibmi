Version:	0.9.10
Release: 9seiden
Name: libunistring
Summary: GNU Unicode string library
License: GPLV2+ or LGPLv3+
Url: http://www.gnu.org/software/libunistring/
Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
Provides: bundled(gnulib)
BuildRequires: libiconv-devel

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package devel
Summary: GNU Unicode string library - development files
Requires: %{name} = %{version}-%{release}

%description devel
Development files for programs using libunistring.

%prep
%setup -q

%build

autoreconf -fiv .
%configure \
	LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
	--with-libiconv-prefix=%{_prefix} \
	--disable-static --enable-shared --with-aix-soname=svr4
%make_build

%install

%make_install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias
# Move staged docs so not picked up by %%doc in main package
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} __doc

%files
%defattr(-, qsys, *none)
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-, qsys, *none)
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc __doc/*
%{_infodir}/%{name}.info*
%{_libdir}/%{name}.so
%{_includedir}/unistring
%{_includedir}/*.h

%changelog
* Thu May 14 2020 Calvin Buckley <calvin@seidengroup.com> - 0.9.10-9seiden
- Seiden rebuild

* Thu May 14 2020 Calvin Buckley <calvin@cmpct.info> - 0.9.10-8qsecofr
- PASE conversion

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.9.10-4
- Rebuild with fixed binutils

* Sat Jul 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.10-3
- Replace obsolete scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Daiki Ueno <dueno@redhat.com> - 0.9.10-1
- Update to upstream 0.9.10 release

* Thu Mar 01 2018 Daiki Ueno <dueno@redhat.com> - 0.9.9-1
- Update to upstream 0.9.9 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.8-2
- Switch to %%ldconfig_scriptlets

* Sat Dec  2 2017 Daiki Ueno <dueno@redhat.com> - 0.9.8-1
- Update to 0.9.8

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Daiki Ueno <dueno@redhat.com> - 0.9.7-1
- Update to 0.9.7
- Update license to "GPLv2+ or LGPLv2+"

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.9.4-4
- Add missing %%license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 02 2014 Pádraig Brady <pbrady@redhat.com> - 0.9.4-1
- Latest upstream

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 29 2013 Pádraig Brady <P@draigBrady.com> 0.9.3-9
- Adjust to avoid duplicate docs caused by %%doc macro changes in Fedora 20

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Akira TAGOH <tagoh@redhat.com> - 0.9.3-5
- Fix a typo in %%preun. (#737638)

* Tue May 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.3-4
- Add bundled(gnulib) provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 23 2010 Pádraig Brady <P@draigBrady.com> 0.9.3-1
- Update to 0.9.3

* Thu Nov 19 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-3
- Remove glibc-devel and texinfo build deps

* Thu Nov 19 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-2
- Changes as per initial review by panemade@gmail.com

* Tue Nov 17 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-1
- Initial version
