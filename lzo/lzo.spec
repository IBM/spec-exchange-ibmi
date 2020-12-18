Summary: A real-time data compression library.
Name: lzo
Version: 2.10
Release: 2
Group: System Environment/Libraries
License: GPL
Source0: http://www.oberhumer.com/opensource/%{name}/download/%{name}-%{version}.tar.gz
Patch0: lzo-pase-compatibility.diff
URL: http://www.oberhumer.com/opensource/%{name}/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
LZO is a portable lossless data compression library written in ANSI C.
It implements a number of algorithms with the following features:
- Decompression is simple and *very* fast.
- Requires no memory for decompression.
- Compression is pretty fast.
- Requires 64 kB of memory for compression.
- Allows you to dial up extra compression at a speed cost in the
  compressor. The speed of the decompressor is not reduced.
- Includes compression levels for generating pre-compressed data which
  achieve a quite competitive compression ratio.
- There is also a compression level which needs only 8 kB for
  compression.
- Supports overlapping compression and in-place decompression.
- Algorithm is thread safe.
- Algorithm is lossless.


%package devel
Summary: Development files for the lzo compression library.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It implements a number of algorithms with many features.

Install the package if you need to build programs that will use the lzo
compression library.


%prep
%setup -q

%patch0 -p1

%build

autoreconf -fiv
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS BUGS NEWS README THANKS doc/LZO.FAQ
%{_libdir}/liblzo2.so.2
# XXX: redundant docs, like tiff?
%{_datadir}/doc/lzo/AUTHORS
%{_datadir}/doc/lzo/COPYING
%{_datadir}/doc/lzo/LZO.FAQ
%{_datadir}/doc/lzo/NEWS
%{_datadir}/doc/lzo/THANKS

%files devel
%defattr(-, qsys, *none)
%doc doc/LZO.TXT doc/LZOAPI.TXT
%{_includedir}/lzo/*.h
%{_libdir}/liblzo2.so
%{_libdir}/pkgconfig/lzo2.pc
%{_datadir}/doc/lzo/LZOAPI.TXT
%{_datadir}/doc/lzo/LZO.TXT

%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 2.10-2
- De-AIX package, use Rochester conventions
- Include patch for PASE

* Fri Dec 15 2017 Michael Perzl <michael@perzl.org> - 2.10-1
- updated to version 2.10

* Thu Apr 02 2015 Michael Perzl <michael@perzl.org> - 2.09-1
- updated to version 2.09

* Mon Oct 13 2014 Michael Perzl <michael@perzl.org> - 2.08-1
- updated to version 2.08

* Tue Aug 23 2011 Michael Perzl <michael@perzl.org> - 2.06-1
- updated to version 2.06

* Sat Apr 23 2011 Michael Perzl <michael@perzl.org> - 2.05-1
- updated to version 2.05

* Mon Nov 08 2010 Michael Perzl <michael@perzl.org> - 2.04-1
- updated to version 2.04

* Fri May 16 2008 Michael Perzl <michael@perzl.org> - 2.03-1
- updated to version 2.03

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 2.02-3
- corrected some SPEC file errors

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 2.02-2
- included both 32-bit and 64-bit shared objects

* Tue Jan 03 2006 Michael Perzl <michael@perzl.org> - 2.02-1
- first version for AIX V5.1 and higher

