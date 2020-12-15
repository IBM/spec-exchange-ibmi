%define icu_maj 67
%define icu_min 1

Name: icu
Version: %{icu_maj}.%{icu_min}
Release: 2seiden
Summary: International Components for Unicode
License: MIT and UCD and Public Domain
URL: http://site.icu-project.org/

BuildRequires: gcc-cplusplus-aix, libstdcplusplus-devel
BuildRequires: python3

Source0: https://github.com/unicode-org/icu/releases/download/release-%{icu_maj}-%{icu_min}/icu4c-%{icu_maj}_%{icu_min}-src.tgz

%description
ICU is a set of C and C++ libraries that provides robust and full-featured
Unicode and locale support. The library provides calendar support, conversions
for many character sets, language sensitive collation, date
and time formatting, support for many locales, message catalogs
and resources, message formatting, normalization, number and currency
formatting, time zones support, transliteration, word, line and
sentence breaking, etc.

This package contains ICU tools.

%package -n libicu%{icu_maj}
Summary: International Components for Unicode (libraries)
Group: Development/Libraries
%description -n libicu%{icu_maj}
ICU is a set of C and C++ libraries that provides robust and full-featured
Unicode support. This package contains the runtime libraries for ICU, and
locales are built into ICU as a library.

%package -n libicu-devel
Summary: International Components for Unicode (development files)
Group: Development/Libraries
Requires: pkg-config
Requires: libicu%{icu_maj} = %{version}-%{release}
%description -n libicu-devel
ICU is a set of C and C++ libraries that provides robust and full-featured
Unicode support. This package contains the development files for ICU.

%prep
# ICU likes to break the rules
%setup -q -n icu

%build

# Pretend to be AIX, it tries an ILE build (!) otherwise
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

# It tries to use just "python"
export PYTHON=python3
# Working threads/mutexes (C++1X MP code won't be exposed otherwise)
# fPIC is also required for ICU to work with dlopen, because otherwise
# it uses the initial-exec TLS model which isn't compatible:
#
# 0509-185 Thread-local variable %1$s (number %2$s)
#   is imported from a dynamically-loaded dependent
#   module %3$s, but
#   the initial-exec model was used.
export CPPFLAGS="-fPIC -pthread"
# Working threads, rpath
export LDFLAGS="-fPIC -pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib"

cd source
# XXX: Switch from AIX to Linuxy convention (mh-...)
# We enable icu-config in case the ICU 4 one from PASE LPP is on PATH
%configure \
	--enable-shared \
	--disable-static \
	--enable-icu-config \
	--disable-samples \
	--with-data-packaging=library
%make_build

%install

cd source
%make_install

# XXX: Because of library symlink resolution (the lack thereof), things
# get linked against libicuwhateverMAJ, not MAJ.MIN. The unversioned libs
# are probably not useful, but we'll keep them around. This is made easier
# by the fact we only deal with one version of ICU installed, so just swap
# the MAJ.MIN library to just MAJ and clobber all the links. Since pkgconf
# and icu-config all point to that library....
rm $RPM_BUILD_ROOT/%{_libdir}/lib*%{icu_maj}.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicudata.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicui18n.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicuio.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicutest.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicutu.a
rm $RPM_BUILD_ROOT/%{_libdir}/libicuuc.a
cd $RPM_BUILD_ROOT/%{_libdir}
mv libicudata%{icu_maj}.%{icu_min}.a libicudata%{icu_maj}.a
mv libicui18n%{icu_maj}.%{icu_min}.a libicui18n%{icu_maj}.a
mv libicuio%{icu_maj}.%{icu_min}.a libicuio%{icu_maj}.a
mv libicutest%{icu_maj}.%{icu_min}.a libicutest%{icu_maj}.a
mv libicutu%{icu_maj}.%{icu_min}.a libicutu%{icu_maj}.a
mv libicuuc%{icu_maj}.%{icu_min}.a libicuuc%{icu_maj}.a

%files
%defattr(-, qsys, *none)
%doc readme.html
%license LICENSE license.html

%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/gendict
%{_bindir}/genrb
%{_bindir}/icuinfo
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv

%{_sbindir}/escapesrc
%{_sbindir}/genccode
%{_sbindir}/gencmn
%{_sbindir}/gennorm2
%{_sbindir}/gensprep
%{_sbindir}/icupkg

%{_mandir}/man1/derb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/gencfu.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/gendict.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/genccode.8*
%{_mandir}/man8/gencmn.8*
%{_mandir}/man8/gensprep.8*
%{_mandir}/man8/icupkg.8*

%files -n libicu%{icu_maj}
%defattr(-, qsys, *none)
%{_libdir}/libicudata%{icu_maj}.a
%{_libdir}/libicui18n%{icu_maj}.a
%{_libdir}/libicuio%{icu_maj}.a
%{_libdir}/libicutest%{icu_maj}.a
%{_libdir}/libicutu%{icu_maj}.a
%{_libdir}/libicuuc%{icu_maj}.a

%files -n libicu-devel
%defattr(-, qsys, *none)
%{_bindir}/icu-config

%{_mandir}/man1/icu-config.1*

%{_libdir}/pkgconfig/*.pc
%{_libdir}/icu

%{_includedir}/unicode

%{_datadir}/icu/%{version}/LICENSE
%{_datadir}/icu/%{version}/mkinstalldirs
%{_datadir}/icu/%{version}/config
%{_datadir}/icu/%{version}/install-sh
