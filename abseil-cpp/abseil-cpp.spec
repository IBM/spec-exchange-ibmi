#
# spec file for package abseil-cpp
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


%define lname	libabsl2206_0_0
Name:           abseil-cpp
Version:        20220623.1
Release:        1.1
Summary:        C++11 libraries which augment the C++ stdlib
License:        Apache-2.0
URL:            https://abseil.io/
Source0:        https://github.com/abseil/abseil-cpp/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# PATCH-FIX-OPENSUSE options-{old,cxx17}.patch Ensure ABI stability regardless of compiler options
%if 0%{?suse_version} < 1550
#Patch0:         options-old.patch
%else
#Patch0:         options-cxx17.patch
%endif
# PATCH-FIX-UPSTREAM Fix-maes-msse41-leaking-into-pkgconfig.patch
#Patch1:         Fix-maes-msse41-leaking-into-pkgconfig.patch
Patch2:          fe6ec8efabe2ca1f6d68d6c14087cdd58ea07136.patch

%description
Abseil is a collection of C++11 libraries which augment the C++
standard library. It also provides features incorporated into C++14
and C++17 standards.

%package -n %{lname}
Summary:        C++11 libraries which augment the C++ stdlib
Obsoletes:      abseil-cpp < %{version}-%{release}
Provides:       abseil-cpp = %{version}-%{release}

%description -n %{lname}
Abseil is a collection of C++11 libraries which augment the C++
standard library. It also provides features incorporated into C++14
and C++17 standards.

%package devel
Summary:        Header files for Abseil
Requires:       %{lname} = %{version}

%description devel
Abseil is a collection of C++11 libraries which augment the C++
standard library.
This package contains headers and build system files for it.

%prep
%autosetup -p1

%build

mkdir cmake-build
cd cmake-build

# absl/status/status.cc needs _LINUX_SOURCE_COMPAT
export CXXFLAGS="-pthread -fno-extern-tls-init -D_LINUX_SOURCE_COMPAT"
export LDFLAGS="-pthread"

# XXX: USEPCRE?
cmake .. \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=On \
	-DCMAKE_CXX_STANDARD=11 \
	#
%make_build

%install

cd cmake-build
%make_install

%files -n %{lname}
%defattr(-, qsys, *none)
%license LICENSE
%{_libdir}/libabsl_*.so.*

%files devel
%defattr(-, qsys, *none)
%doc README.md
%{_includedir}/absl
%{_libdir}/cmake/absl
%{_libdir}/libabsl_*.so
%{_libdir}/pkgconfig/absl_*.pc

%changelog
* Wed Jan 18 2023 Calvin Buckley <calvin@seidengroup.com>
- port to IBM i
* Sat Sep 24 2022 Dirk Müller <dmueller@suse.com>
- update to 20220623.1:
  * minor warning fix
* Mon Jul 11 2022 Bruno Pitrus <brunopitrus@hotmail.com>
- Add Fix-maes-msse41-leaking-into-pkgconfig.patch
  * Do not make programs compiled with abseil require new-ish CPUs.
* Sun Jul  3 2022 Matthias Eliasson <elimat@opensuse.org>
- Update to version 20220623.0
  What's New:
  * Added absl::AnyInvocable, a move-only function type.
  * Added absl::CordBuffer, a type for buffering data for eventual inclusion an
    absl::Cord, which is useful for writing zero-copy code.
  * Added support for command-line flags of type absl::optional<T>.
  Breaking Changes:
  * CMake builds now use the flag ABSL_BUILD_TESTING (default: OFF) to control
    whether or not unit tests are built.
  * The ABSL_DEPRECATED macro now works with the GCC compiler. GCC users that
    are experiencing new warnings can use -Wno-deprecated-declatations silence
  the warnings or use -Wno-error=deprecated-declarations to see warnings but
  not fail the build.
  * ABSL_CONST_INIT uses the C++20 keyword constinit when available. Some
    compilers are more strict about where this keyword must appear compared to
  the pre-C++20 implementation.
  * Bazel builds now depend on the bazelbuild/bazel-skylib repository.
    See Abseil's WORKSPACE file for an example of how to add this dependency.
  Other:
  * This will be the last release to support C++11. Future releases will require at least C++14.
- run spec-cleaner
* Wed Jun 29 2022 Fabian Vogt <fvogt@suse.com>
- Remove obsolete 0%%{suse_version} < 1500 conditions
* Wed Jun 29 2022 Bruno Pitrus <brunopitrus@hotmail.com>
- Add options-old.patch, options-cxx17.patch
  * Ensure ABI stability regardless of compiler settings per instruction in the header.
* Mon Apr  4 2022 Jan Engelhardt <jengelh@inai.de>
- Implement shlib packaging policy
* Fri Mar  4 2022 Danilo Spinella <danilo.spinella@suse.com>
- Fix build on SLE-12-SP5
* Tue Jan  4 2022 Dirk Müller <dmueller@suse.com>
- update to 20211102.0:
  * absl::Cord is now implemented as a b-tree. The new implementation offers
    improved performance in most workloads.
  * absl::SimpleHexAtoi() has been added to strings library for parsing
    hexadecimal strings
* Wed Jun 30 2021 Ferdinand Thiessen <rpm@fthiessen.de>
- Update to version 20210324.2 (LTS):
  * No user visible changes, only build system related
* Sun Apr 25 2021 Ferdinand Thiessen <rpm@fthiessen.de>
- Update to LTS version 20210324.1
  * Fixed missing absl::Cleanup
  * Fixed pkgconfig install path
- Dropped upstream merged Correctly-install-pkgconfig.patch
* Tue Apr 13 2021 Ferdinand Thiessen <rpm@fthiessen.de>
- Update to LTS version 20210324.0
  * Breaking: The empty absl::container target has been removed from
    the CMake build. This target had no effect and references to
    this target in user code can safely be removed.
  * New: The cleanup library has been released. This library contains
    the control-flow-construct-like type absl::Cleanup which is used
    for executing a callback on scope exit.
  * New: The numeric library now includes bits.h, a polyfill header
    containing implementations of C++20's bitwise math functions.
  * New: Abseil now installs pkg-config files to make it easier to
    use Abseil with some other build systems.
  * New: Abseil now respects the default CMake installation paths.
    Standard CMake variables like CMAKE_INSTALL_PREFIX can be used
    to change the installation path.
- Added Correctly-install-pkgconfig.patch from upstream to fix
  installation of pkgconfig files
- Call ldconfig on post and postun
* Tue Dec 29 2020 Matthias Eliasson <elimat@opensuse.org>
- Update to version 20200923.2
  What's New:
  * absl::StatusOr<T> has been released. See our blog
    post for more information.
  * Abseil Flags reflection interfaces have been released.
  * Abseil Flags memory usage has been significantly optimized.
  * Abseil now supports a "hardened" build mode. This build mode enables
    runtime checks that guard against programming errors that may lead
    to security vulnerabilities.
  Notable Fixes:
  * Sanitizer dynamic annotations like AnnotateRWLockCreate that are
    also defined by the compiler sanitizer implementation are no longer
    also defined by Abseil.
  * Sanitizer macros are now prefixed with ABSL_ to avoid naming collisions.
  * Sanitizer usage is now automatically detected and no longer requires
    macros like ADDRESS_SANITIZER to be defined on the command line.
  Breaking Changes:
  * Abseil no longer contains a dynamic_annotations library. Users
    using a supported build system (Bazel or CMake) are unaffected by
    this, but users manually specifying link libraries may get an error
    about a missing linker input.
* Fri Nov  6 2020 Fabian Vogt <fvogt@suse.com>
- Drop source package, was only used by grpc which was switched
  over to use the shared library
* Tue Oct 27 2020 Jan Engelhardt <jengelh@inai.de>
- Build shared libraries of abseil for use by grpc
  (related to https://github.com/grpc/grpc/issues/24476)
* Sat Sep  5 2020 Jan Engelhardt <jengelh@inai.de>
- Switch the package to noarch.
* Fri Jul 24 2020 Matthias Eliasson <elimat@opensuse.org>
- Update to version 20200225.2
  * This release fixes the list of dependencies of absl::Cord in the CMake build.
  * bug fix for absl::Status::ErasePayload
* Thu Jan 16 2020 Michał Rostecki <mrostecki@opensuse.org>
- Remove all packages except source.
* Tue Jan 14 2020 Dominique Leuenberger <dimstar@opensuse.org>
- Set ExcludeArch: %%ix86: bazel is required to build which in turn
  is not supported on ix86.
* Wed Dec 18 2019 Swaminathan Vasudevan <svasudevan@suse.com>
- Update to version 20190808
* Sat Nov 23 2019 Bernhard Wiedemann <bwiedemann@suse.com>
- Sort find output to make build reproducible (boo#1041090)
* Thu Oct 17 2019 Richard Brown <rbrown@suse.com>
- Remove obsolete Groups tag (fate#326485)
* Mon Sep 23 2019 mrostecki@opensuse.org
- Update to version 20190605:
  * avoid use of undefined ABSL_HAVE_ELF_MEM_IMAGE
  * Avoid undefined behavior when nullptr is passed to memcpy with size 0
  * CMake: Set correct flags for clang-cl
  * Adding linking of CoreFoundation to CMakeLists in absl/time as
    time_zone_lookup.cc includes CoreFoundation
  * Implement Span::first and Span::last from C++20
  * Changed HTTP URLs to HTTPS where possible
  * Fix GCC8 warnings
  * Fix library order for Conan package
  * _umul128 is not available on Windows ARM64
  * Add note at top that this is supported best-effort
  * Update Conan author
  * Add Conan topics
  * Remove cctz as external dependency
  * Add Conan recipe
* Thu Sep 19 2019 Michał Rostecki <mrostecki@opensuse.org>
- Add source package.
* Wed Jul 24 2019 Michał Rostecki <mrostecki@opensuse.org>
- Use bazel0.19 as build fails with the latest bazel (0.26)
* Thu Mar  7 2019 Michal Rostecki <mrostecki@opensuse.org>
- Add soname to all *.so* files.
* Thu Feb 28 2019 Michał Rostecki <mrostecki@opensuse.org>
- Fix build with Bazel 0.22.0.
- Add optflags.
* Fri Jan 18 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Fix aarch64 and ppc64 builds
* Wed Dec 12 2018 Jan Engelhardt <jengelh@inai.de>
- Trim redundancies from description.
* Thu Nov 29 2018 Michał Rostecki <mrostecki@suse.de>
- Update to version 20181127:
  * Export of internal Abseil changes. -- 15d7bcf28220750db46930f4d8c090b54e3ae5fe by Jon Cohen <cohenjon@google.com>:
  * Export of internal Abseil changes. -- 5278e56bd7d322ecf161eaf29fd7fa3941d7431b by Greg Falcon <gfalcon@google.com>:
- Switch from CMake to Bazel
* Mon Nov 19 2018 Michał Rostecki <mrostecki@suse.de>
- Update to version 20181116:
  * Export of internal Abseil changes. -- da04b8cd21f6225d71397471474d34a77df0efd6 by Jon Cohen <cohenjon@google.com>:
  * Export of internal Abseil changes. -- 5f1ab09522226336830d9ea6ef7276d37f536ac5 by Abseil Team <absl-team@google.com>:
  * Export of internal Abseil changes. -- 07575526242a8e1275ac4223a3d2822795f46569 by CJ Johnson <johnsoncj@google.com>:
  * Export of internal Abseil changes. -- 178e7a9a76fc8fcd6df6335b59139cbe644a16b9 by Jon Cohen <cohenjon@google.com>:
  * Export of internal Abseil changes. -- ee19e203eca970ff88e8f25ce4e19c32e143b988 by Jon Cohen <cohenjon@google.com>:
  * Export of internal Abseil changes. -- 4e224c85c3730398919fc5195cb1fc7a752e6e4f by Mark Barolak <mbar@google.com>:
  * Export of internal Abseil changes. -- 9e8aa654630015ea8221703b0ea10dd1a47a848f by Abseil Team <absl-team@google.com>:
  * Export of internal Abseil changes. -- ba4dd47492748bd630462eb68b7959037fc6a11a by Abseil Team <absl-team@google.com>:
  * Fix compilation of generic byteswap routines
  * Fix absl::container on VS2017 v15.8 (#192)
