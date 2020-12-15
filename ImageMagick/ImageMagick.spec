%define maj            7
%define quantum_depth  16
%global VERSION  7.0.10
%global Patchlevel  46

%define clibver        8
%define cwandver       8
%define cxxlibver      4
%define libspec        -%{maj}_Q%{quantum_depth}HDRI

Name:           ImageMagick
Version:        %{VERSION}.%{Patchlevel}
Release:        1seiden
Summary:        Viewer and Converter for Images
Group:          Applications/Multimedia
License:        https://imagemagick.org/script/license.php
Url:            https://imagemagick.org/
Source0:        https://imagemagick.org/download/%{name}-%{VERSION}-%{Patchlevel}.tar.xz
Patch1:         ImageMagick-aix-dlname.patch
# Not needed until we decide to use a custom X.org
#Patch2:         ImageMagick-pase-x11-dir.patch

# Simplified dependency set from qseco.fr for ease of maintaining.
# Stick with what IBM packages or what we've brought in for needs.
# More can be added later.
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  coreutils-gnu
# Workaround for bugs in IBM fontconfig
BuildRequires:  expat-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc-cplusplus-aix
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libstdcplusplus-devel
BuildRequires:  libtiff-devel
BuildRequires:  libtool
BuildRequires:  libwebp-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzip-devel
BuildRequires:  libzstd-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
# Using stock PASE X11; don't know if that's a bad idea

# Programs it calls into, not libraries
BuildRequires:  ghostscript
BuildRequires:  zip
BuildRequires:  curl
Requires:       ghostscript
Requires:       zip
Requires:       curl

# XXX: To add at discretion:
# libheif, raqm (also for gd), gvc, fpx, flif, fftw, jbig, dps, brunsli,
# wmf, exr, lqr, raw_r, ddjvu, 7za, dejavu-fonts (for fontconfig)

Requires:       %{name}-libs = %{version}-%{release}

%description
ImageMagick® is a software suite to create, edit, compose, or convert bitmap images. It can read and write images in a variety of formats (over 200) including PNG, JPEG, JPEG-2000, GIF, TIFF, DPX, EXR, WebP, Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and Bézier curves.

The functionality of ImageMagick is typically utilized from the command-line or you can use the features from programs written in your favorite language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand (C), ChMagick (Ch), ImageMagickObject (COM+), Magick++ (C++), JMagick (Java), L-Magick (Lisp), Lua (LuaJIT), NMagick (Neko/haXe), Magick.NET (.NET), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP (PHP), IMagick (PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a language interface, use ImageMagick to modify or create images dynamically and automagically.

ImageMagick utilizes multiple computational threads to increase performance and can read, process, or write mega-, giga-, or tera-pixel image sizes.

ImageMagick is free software delivered as a ready-to-run binary distribution or as source code that you may use, copy, modify, and distribute in both open and proprietary applications. It is distributed under the Apache 2.0 license.

The ImageMagick development process ensures a stable API and ABI. Before each ImageMagick release, we perform a comprehensive security assessment that includes memory error and thread data race detection to prevent security vulnerabilities.

The authoritative ImageMagick web site is https://imagemagick.org. The authoritative source code repository is http://git.imagemagick.org/repos/ImageMagick. We maintain a source code mirror at GitHub.

%package devel
Summary: Library links and header files for ImageMagick application development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# Requires: ghostscript-devel
Requires: bzip2-devel, freetype-devel, libtiff-devel, libjpeg-turbo-devel, libpng-devel
Requires: libwebp-devel, pkg-config, xz-devel, fontconfig-devel, zlib-devel, libxml2-devel

Requires: libMagickCore%{libspec}%{clibver} = %{version}-%{release}
Requires: libMagickWand%{libspec}%{cwandver} = %{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package -n libMagickCore%{libspec}%{clibver}
Summary:        C runtime library for ImageMagick
Group:          Applications/Multimedia

Provides: ImageMagick-libs = %{version}-%{release}
Obsoletes: ImageMagick-libs

%description -n libMagickCore%{libspec}%{clibver}
ImageMagick is a robust collection of tools and libraries to read,
write, and manipulate an image in many image formats, including popular
formats like TIFF, JPEG, PNG, PDF, PhotoCD, and GIF. With ImageMagick,
you can create images dynamically, making it suitable for Web
applications. You can also resize, rotate, sharpen, color-reduce, or
add special effects to an image and save your completed work in many
different image formats. Image processing operations are available from
the command line as well as through C, C++, and Perl-based programming
interfaces.


%package -n libMagickWand%{libspec}%{cwandver}
Summary:        C runtime library for ImageMagick
Group:          Applications/Multimedia

Provides: ImageMagick-libs = %{version}-%{release}
Obsoletes: ImageMagick-libs

%description -n libMagickWand%{libspec}%{cwandver}
ImageMagick is a robust collection of tools and libraries to read,
write, and manipulate an image in many image formats, including popular
formats like TIFF, JPEG, PNG, PDF, PhotoCD, and GIF. With ImageMagick,
you can create images dynamically, making it suitable for Web
applications. You can also resize, rotate, sharpen, color-reduce, or
add special effects to an image and save your completed work in many
different image formats. Image processing operations are available from
the command line as well as through C, C++, and Perl-based programming
interfaces.


%package doc
Summary: ImageMagick HTML documentation
Group: Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in HTML format.
Note this documentation can also be found on the ImageMagick website:
https://imagemagick.org/.


%package -n libMagick++%{libspec}%{cxxlibver}
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries

Provides: ImageMagick-c++ = %{version}-%{release}
Obsoletes: ImageMagick-c++

Requires: %{name}-libs = %{version}-%{release}

%description -n libMagick++%{libspec}%{cxxlibver}
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install libMagick++%{libspec}%{cxxlibver}if you want to use any applications that use Magick++.


%package -n libMagick++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: libMagick++%{libspec}%{cxxlibver} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

Provides: ImageMagick-c++-devel = %{version}-%{release}
Obsoletes: ImageMagick-c++-devel

%description -n libMagick++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install libMagick++-devel, ImageMagick-devel and
ImageMagick.

You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n %{name}-%{VERSION}-%{Patchlevel}
%patch1 -p1
#%patch2 -p0

# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build

export LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib"

autoreconf -fiv .
# openmp hangs reported, don't do it
# https://github.com/Imagick/imagick#openmp
%configure \
        --enable-shared \
        --disable-static \
        --with-modules \
        --with-x \
        --with-threads \
        --with-magick_plus_plus \
        --with-xml \
        --without-gcc-arch \
        --with-lzma=yes \
        --with-zstd=yes \
        --with-zlib=yes \
        --with-bzlib=yes \
        --with-lcms=no \
        --with-pango=no \
        --with-fontconfig=yes \
        --with-freetype=yes \
        --with-openjp2=no \
        --with-tiff=yes \
        --with-webp=yes \
        --with-png=yes \
        --with-jpeg=yes \
        --disable-openmp \
        --with-aix-soname=svr4

# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
# XXX: Is this still true?
gmake

%check
# Some tests will fail due to font stuff
( gmake -k check || true )

%install

%make_install
cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{VERSION}
rm %{buildroot}%{_libdir}/*.la
/usr/bin/strip %{buildroot}%{_bindir}/magick

%files
%defattr(-, qsys, *none)
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/ImageMagick.1*

%files -n libMagickCore%{libspec}%{clibver}
%defattr(-, qsys, *none)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickCore-7.Q16HDRI.so.%{clibver}*
%{_libdir}/%{name}-%{VERSION}
%{_datadir}/%{name}-7
%dir %{_sysconfdir}/%{name}-7
%config(noreplace) %{_sysconfdir}/%{name}-7/*.xml

%files -n libMagickWand%{libspec}%{cwandver}
%defattr(-, qsys, *none)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickWand-7.Q16HDRI.so.%{cwandver}*

%files devel
%defattr(-, qsys, *none)
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/libMagickCore-7.Q16HDRI.so
%{_libdir}/libMagickWand-7.Q16HDRI.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-7.Q16HDRI.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-7.Q16HDRI.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-7.Q16HDRI.pc
%dir %{_includedir}/%{name}-7
%{_includedir}/%{name}-7/MagickCore
%{_includedir}/%{name}-7/MagickWand
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/MagickWand-config.*

%files doc
%defattr(-, qsys, *none)
%doc %{_datadir}/doc/%{name}-7
%doc %{_datadir}/doc/%{name}-%{VERSION}
%doc LICENSE

%files -n libMagick++%{libspec}%{cxxlibver}
%defattr(-, qsys, *none)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-7.Q16HDRI.so.%{cxxlibver}*

%files -n libMagick++-devel
%defattr(-, qsys, *none)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}-7/Magick++
%{_includedir}/%{name}-7/Magick++.h
%{_libdir}/libMagick++-7.Q16HDRI.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-7.Q16HDRI.pc
%{_mandir}/man1/Magick++-config.*

%changelog
* Wed Dec 9 2020 Calvin Buckley <calvin@seidengroup.com> - 7.0.10.46-1seiden
- Bump
- Change library scheme to be like SUSE (more resistant to soname bump), since
  we've been burned on this before

* Tue Nov 17 2020 Calvin Buckley <calvin@seidengroup.com> - 7.0.10-38-1seiden
- Bump
- Clean up dep list and add more deps

* Mon Jun 29 2020 Calvin Buckley <calvin@seidengroup.com> - 7.0.10.22-1seiden
- Bump
- Clean up commented up stuff
- Reduced dependency set for support reasons

* Thu Jan 30 2020 Calvin Buckley <calvin@cmpct.info> - 7.0.9.20-1qsecofr
- Bump
- Disable OpenMP

* Wed Jan 1 2020 Calvin Buckley <calvin@cmpct.info> - 7.0.9.13-2qsecofr
- Enable some desirable stuff

* Tue Dec 31 2019 Calvin Buckley <calvin@cmpct.info> - 7.0.9.13-1qsecofr
- Port to IBM i

* Tue Sep 24 2019 Ayappan P <ayappap2@in.ibm.com> - 7.0.8.61-2
- Add proper dependency on freetype2-devel
- Enable libwebp support

* Tue Aug 20 2019 Ayappan P <ayappap2@in.ibm.com> - 7.0.8.61-1
- Port to AIX Toolbox
