#
# spec file for package re2
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global longver 2022-12-01
%global shortver %(echo %{longver}|sed 's|-||g')
%define libname libre2-10
Name:           re2
Version:        %{shortver}
Release:        50.1
Summary:        C++ fast alternative to backtracking RE engines
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
URL:            https://github.com/google/re2
Source0:        %{url}/archive/%{longver}/%{name}-%{longver}.tar.gz
BuildRequires:  cmake >= 3.10.2

%description
RE2 is a C++ library providing a fast, safe, thread-friendly alternative to
backtracking regular expression engines like those used in PCRE, Perl, and
Python.

Backtracking engines are typically full of features and convenient syntactic
sugar but can be forced into taking exponential amounts of time on even small
inputs.

In contrast, RE2 uses automata theory to guarantee that regular expression
searches run in time linear in the size of the input, at the expense of some
missing features (e.g. back references and generalized assertions).

%package -n %{libname}
Summary:        C++ fast alternative to backtracking RE engines
Group:          System/Libraries

%description -n %{libname}
RE2 is a C++ library providing a fast, safe, thread-friendly alternative to
backtracking regular expression engines like those used in PCRE, Perl, and
Python.

Backtracking engines are typically full of features and convenient syntactic
sugar but can be forced into taking exponential amounts of time on even small
inputs.

In contrast, RE2 uses automata theory to guarantee that regular expression
searches run in time linear in the size of the input, at the expense of some
missing features (e.g. back references and generalized assertions).

%package        devel
Summary:        C++ header files and library symbolic links for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{version}

%description    devel
This package contains the C++ header files and symbolic links to the shared
libraries for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -n %{name}-%{longver}

%build

mkdir cmake-build
cd cmake-build

export CXXFLAGS="-pthread -fno-extern-tls-init"
export LDFLAGS="-pthread"

# XXX: USEPCRE?
cmake .. \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=On
	#
#cmake_build
%make_build

%install

cd cmake-build
#cmake_install
%make_install

%check
# Test if created library is installed correctly
%make_build shared-testinstall DESTDIR=%{buildroot} includedir=%{_includedir} libdir=%{_libdir}
%if %{with test}
# Actual functionality tests
#export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}:LD_LIBRARY_PATH
%ctest --repeat until-pass:9
%endif

%files -n %{libname}
%defattr(-, qsys, *none)
%license LICENSE
%doc AUTHORS CONTRIBUTORS README
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-, qsys, *none)
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}

%changelog
* Wed Jan 18 2023 Calvin Buckley <calvin@seidengroup.com>
- port to IBM i
* Sun Dec  4 2022 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2022-12-01:
  * Update to Unicode 15.0.0 data
  * cmake install now installs the pkg-config file
* Wed Jun  1 2022 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2022-06-01:
  * switch to cxx_std_11 and other developer visible fixes
* Sun May  1 2022 Callum Farmer <gmbr3@opensuse.org>
- Use Release config so O3 is used
* Thu Apr 28 2022 Callum Farmer <gmbr3@opensuse.org>
- Avoid sporadic failures by setting until-pass on CTest
* Wed Apr 27 2022 Callum Farmer <gmbr3@opensuse.org>
- Disable tests on ARMv6
* Tue Apr 26 2022 Callum Farmer <gmbr3@opensuse.org>
- Disable tests on ZSystems and RISCV
* Sun Apr 24 2022 Stefan Brüns <stefan.bruens@rwth-aachen.de>
- Switch build to CMake, otherwise CMake config is not installed.
  Required for Apache ORC and arrow, and google-or-tools.
  (https://github.com/google/re2/issues/304)
- Run some real tests via CTest
* Fri Apr  1 2022 Andreas Stieger <andreas.stieger@gmx.de>
- Update to 2022-04-01:
  * Improve performance slightly
  * Prog::Fangout() is no longer experimental
* Fri Feb  4 2022 Callum Farmer <gmbr3@opensuse.org>
- Update to 2022-02-01:
  * Address a `-Wunused-but-set-variable' warning from Clang 13.x
  * Don't specify the -std flag in Makefile or re2.pc
  * Remove a redundant map access
* Sun Dec  5 2021 Callum Farmer <gmbr3@opensuse.org>
- Use newer libs and GCC on Leap 15.3 & 15.4
* Fri Nov  5 2021 Callum Farmer <gmbr3@opensuse.org>
- Update to 2021-11-01:
  * Update Unicode data to 14.0.0
  * Address a `-Wshadow' warning
* Wed Sep  1 2021 Callum Farmer <gmbr3@opensuse.org>
- Update to 2021-09-01:
  * Permit Unicode characters beyond ASCII in capture names
* Fri Aug  6 2021 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2021-08-01:
  * case-insensitive prefix acceleration
* Sat Jun 12 2021 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2021-06-01:
  * Fix (|a)* matching more text than (|a)+
  * build system tweaks and developer visible fixes
* Thu Apr 15 2021 Andreas Stieger <andreas.stieger@gmx.de>
- Update to 2021-04-01:
  * Make cached benchmarks actually use cached objects
  * Address some -Wmissing-field-initializers warnings
  * Make it easier to swap in a scalable reaer-writer mutex
  * In the shared library, set compatibility version and
    current version
* Thu Feb  4 2021 Callum Farmer <gmbr3@opensuse.org>
- Update to version 2021-02-02:
  * Address `-Wnull-dereference' warnings from GCC 10.x.
* Thu Nov  5 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Update to version 2020-11-01:
  * Refactoring and fixes
* Sat Oct 10 2020 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2020-10-01:
  * build system updates and compiler warnings fixes
* Tue Aug 11 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 2020-08-01:
  * Various internal changes
* Sun Jun  7 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 2020-06-01:
  * Various internal changes
* Fri May 29 2020 Martin Pluskal <mpluskal@suse.com>
- Enable PGO during build
* Wed May 20 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 2020-05-03:
  * Internal fixes and optimisations
  * Remove deprecated APIs, SONAME change
- Build tests with optflags
- Disable tests for 32 bit architectures
* Sun Apr  5 2020 Andreas Stieger <andreas.stieger@gmx.de>
- Updat to version 2020-04-01:
  * Update Unicode data to 13.0.0
  * Include the pattern length in "DFA out of memory" errorrs
* Fri Mar 20 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 2020-03-03:
  * various developer visible changes
* Thu Feb 13 2020 Martin Pluskal <mpluskal@suse.com>
- Small spec file update
* Wed Jan  8 2020 Tomáš Chvátal <tchvatal@suse.com>
- Update to 2020-01-01:
  * various developer visible changes
* Fri Dec  6 2019 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2019-12-01:
  * fix latent bugs and undefined behavior
* Sat Nov 16 2019 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2019-11-01:
  * new benchmark API
* Thu Sep 12 2019 Andreas Stieger <andreas.stieger@gmx.de>
- update to 2019-09-01:
  * build system fixes
* Fri Aug  2 2019 Andreas Stieger <andreas.stieger@gmx.de>
- Update to 2019-08-01:
  * Update Unicode data to 12.1.0
  * Various developer visible changes
* Mon Jul 22 2019 Martin Pluskal <mpluskal@suse.com>
- Fix download url
* Wed Jul 17 2019 Andreas Stieger <andreas.stieger@gmx.de>
- Update to 2019-07-01:
  * developer visible changes
* Wed Mar 13 2019 Tomáš Chvátal <tchvatal@suse.com>
- Update to 2019-03-01:
  * developer visible changes only
* Fri Jan  4 2019 astieger@suse.com
- update to 2019-01-01:
  * developer visible changes, performance tweaks and bug fixes
* Wed Oct 17 2018 Martin Pluskal <mpluskal@suse.com>
- update to 2018-10-01:
  * developer visible changes only
* Wed Sep  5 2018 astieger@suse.com
- update to 2018-09-01:
  * developer visible changes only
* Thu Aug 23 2018 astieger@suse.com
- update to 2018-08-01:
  * Fix the "DFA out of memory" error for the reverse Prog
* Fri Jul 20 2018 mpluskal@suse.com
- Simplify spec file a bit
* Fri Jul 20 2018 astieger@suse.com
- update to 2018-07-01:
  * Fix a "DFA out of memory" error
  * Update Unicode data to 11.0.0
  * Fix `-Wclass-memaccess' warnings and fallthrough macros
  * Use the standard first-byte analysis for the DFA too
* Fri Apr  6 2018 mpluskal@suse.com
- Update to version 2018-04-01
  * developer visible changes only
* Wed Mar 21 2018 astieger@suse.com
- update to 2018-03-01:
  * no longer linking against librd and libm
  * other developer visible changes
* Fri Feb  2 2018 astieger@suse.com
- update to 2018-02-01:
  * developer visible changes only
* Wed Jan  3 2018 mpluskal@suse.com
- Update to version 2018-01-01
  * No upstream changelog available
* Wed Jan  3 2018 dimstar@opensuse.org
- Add baselibs.conf: create libre2-0-32bit, dependency to
  libqt5-qtwebengine-32bit.
* Mon Dec 18 2017 mpluskal@suse.com
- Update to version 2017-12-01
  * No upstream changelog available
* Fri Nov  3 2017 mpluskal@suse.com
- Update to version 2017-11-01
  * No upstream changelog available
* Mon Sep  4 2017 mpluskal@suse.com
- Update to version 2017-07-01
  * No upstream changelog available
* Sat Jul 29 2017 mpluskal@suse.com
- Update to version 2017-07-01
  * No upstream changelog available
* Sun Jun 11 2017 mpluskal@suse.com
- Update to version 2017-06-01
  * No upstream changelog available
* Fri May 19 2017 vsistek@suse.com
- Update to version 2017-05-01
  * No upstream changelog available
* Thu Apr 13 2017 mpluskal@suse.com
- Update to version 2017-04-01
  * No upstream changelog available
* Thu Mar 16 2017 mpluskal@suse.com
- Update to version 2017-03-01
  * No upstream changelog available
* Sat Jan 14 2017 mpluskal@suse.com
- Update to version 2017-01-01
  * No upstream changelog available
* Sat Dec  3 2016 mpluskal@suse.com
- Update to version 2016-11-01:
  * No upstream changelog available
- Drop no longer needed re2-gcc61.patch
* Sat Oct 22 2016 jengelh@inai.de
- Fixup group and avoid rm indirection
* Thu Sep  8 2016 mpluskal@suse.com
- Drop releasenumber
* Wed Sep  7 2016 tchvatal@suse.com
- Version update to 2016-09-01 version
  * Various changes based on google needs, long changelog in upstream
    github repo
- Rebase spec on Fedora package
- Add patch to build with gcc 6.1:
  * re2-gcc61.patch
* Fri Dec 21 2012 aplanas@novell.com
- Initial package version.
