%global sover 2.3

%undefine _debuginfo_subpackages
%undefine _debugsource_packages

# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0

%global __brp_check_rpaths %{nil}

Name:           OpenImageIO
Version:        2.3.13.0
Release:        7%{?dist}
Summary:        Library for reading and writing images

License:        BSD
URL:            http://www.openimageio.org
Source0:        https://github.com/OpenImageIO/oiio/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake gcc-c++
BuildRequires:  txt2man
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  glew-devel
BuildRequires:  openexr-devel >= 3.1.1
BuildRequires:  imath-devel >= 3.1.2
BuildRequires:  Field3D-devel >= 1.7.3-15
BuildRequires:  python3-devel
BuildRequires:	pybind11-devel
BuildRequires:  libpng-devel libtiff-devel libjpeg-turbo-devel openjpeg2-devel
BuildRequires:  giflib-devel
BuildRequires:  libwebp-devel
BuildRequires:  hdf5-devel
BuildRequires:  dcmtk-devel
BuildRequires:  zlib-devel
BuildRequires:  jasper-devel
BuildRequires:  pugixml-devel
BuildRequires:  opencv-devel >= 4.5.5
BuildRequires:  LibRaw-devel
BuildRequires:  openssl-devel
BuildRequires:	freetype-devel
BuildRequires:	ffmpeg4-devel 
BuildRequires:	git
# new support
BuildRequires:	libsquish-devel
BuildRequires:	tbb-devel
BuildRequires:	openvdb-devel >= 8.1.0-6
BuildRequires:	libjpeg-turbo-devel 
#BuildRequires:  libheif-devel
%if 0%{?fedora} >= 34
BuildRequires:  ptex-devel >= 2.4.0
%else
BuildRequires:  ptex-devel 
%endif
BuildRequires:  vulkan-loader
# WARNING: OpenColorIO and OpenImageIO are cross dependent.
# If an ABI incompatible update is done in one, the other also needs to be
# rebuilt.
#BuildRequires:  OpenColorIO-devel >= 2.0.0


%description
OpenImageIO is a library for reading and writing images, and a bunch of related
classes, utilities, and applications. Main features include:
- Extremely simple but powerful ImageInput and ImageOutput APIs for reading and
  writing 2D images that is format agnostic.
- Format plugins for TIFF, JPEG/JFIF, OpenEXR, PNG, HDR/RGBE, Targa, JPEG-2000,
  DPX, Cineon, FITS, BMP, ICO, RMan Zfile, Softimage PIC, DDS, SGI,
  PNM/PPM/PGM/PBM, Field3d.
- An ImageCache class that transparently manages a cache so that it can access
  truly vast amounts of image data.


%package -n python3-openimageio
Summary:        Python 2 bindings for %{name}
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python3-openimageio
Python bindings for %{name}.


%package utils
Summary:        Command line utilities for %{name}
Requires:       %{name} = %{version}-%{release}

%description utils
Command-line tools to manipulate and get information on images using the
%{name} library.


%package iv
Summary:        %{name} based image viewer
Requires:       %{name} = %{version}-%{release}

%description iv
A really nice image viewer, iv, based on %{name} classes (and so will work
with any formats for which plugins are available).


%package devel
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for package %{name}


%prep
%autosetup -n oiio-%{version} -p1

# Remove bundled pugixml
rm -f src/include/OpenImageIO/pugixml.hpp \
      src/include/OpenImageIO/pugiconfig.hpp \
      src/libutil/OpenImageIO/pugixml.cpp 

# Remove bundled tbb
rm -rf src/include/tbb


# Try disabeling old CMP
sed -i "s/SET CMP0046 OLD/SET CMP0046 NEW/" CMakeLists.txt


%build

mkdir -p build

cmake -B build -DCMAKE_INSTALL_PREFIX="/usr" \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DCMAKE_INSTALL_FULL_LIBDIR=%{_lib} \
	-DCMAKE_CXX_STANDARD=14 \
	-DCMAKE_INSTALL_MANDIR:PATH=%{_mandir}/man1 \
	-DOIIO_BUILD_TESTS=OFF \
	-DSTOP_ON_WARNING=OFF \
	-DUSE_EXTERNAL_PUGIXML=ON \
	-DUSE_FFMPEG=ON \
	-DUSE_FIELD3D=ON \
	-DUSE_FREETYPE=ON \
	-DUSE_GIF=ON \
	-DUSE_JPEGTURBO=ON \
	-DUSE_LIBRAW=ON \
	-DUSE_NUKE=OFF \
	-DUSE_OCIO=ON \
	-DUSE_OPENCV=ON \
	-DUSE_OPENGL=ON \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DUSE_OPENJPEG=ON \
	-DUSE_OPENSSL=ON \
	-DPYTHON_VERSION=%{python3_version} \
	-DPYLIB_INSTALL_DIR:PATH=%{python3_sitearch} \
	-DINSTALL_FONTS:BOOL=FALSE \
	-DUSE_QT=ON \
	-Wno-dev 
	
	%make_build -C build


%install
%make_install -C build

# Move man pages to the right directory
mkdir -p %{buildroot}%{_mandir}/man1
#cp -a src/doc/*.1 %{buildroot}%{_mandir}/man1

%check
# Not all tests pass on linux
#pushd build && make test

%define _legacy_common_support 1


%files
%license LICENSE.md
%{_libdir}/libOpenImageIO.so.%{sover}*
%{_libdir}/libOpenImageIO_Util.so.%{sover}*
%{_docdir}/OpenImageIO/

%files -n python3-openimageio
%{python3_sitearch}/OpenImageIO.cpython-*.so

%files utils
%exclude %{_bindir}/iv
%{_bindir}/*
%exclude %{_mandir}/man1/iv.1.gz
%{_mandir}/man1/*.1.gz

%files iv
%{_bindir}/iv
%{_mandir}/man1/iv.1.gz

%files devel
%{_libdir}/libOpenImageIO.so
%{_libdir}/libOpenImageIO_Util.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/OpenImageIO.pc
#%{_datadir}/cmake/Modules/FindOpenImageIO.cmake
%{_libdir}/cmake/OpenImageIO/

%changelog

* Wed Jun 01 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.3.13.0-7
- Updated to 2.3.13.0

* Fri Feb 04 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.3.12.0-7
- Updated to 2.3.12.0

* Sat Dec 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.3.10.1-7
- Updated to 2.3.10.1

* Wed Nov 17 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.3.9.1-7
- Updated to 2.3.9.1

* Mon Oct 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.3.8.0-7
- Updated to 2.3.8.0

* Sun Aug 01 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.16.0-7
- Updated to 2.2.16.0

* Fri Jun 18 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.15.1-8
- Rebuilt for openvdb

* Mon Jun 07 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.15.1-7
- Updated to 2.2.15.1

* Mon May 03 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.14.0-7
- Updated to 2.2.14.0

* Wed Apr 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.13.1-7
- Updated to 2.2.13.1

* Sat Mar 27 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.12.0-7
- Updated to 2.2.12.0

* Wed Jan 27 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.10.0-7
- Updated to 2.2.10.0

* Fri Nov 27 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.8.0-7
- Updated to 2.2.8.0

* Thu Nov 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.7.0-8
- Rebuilt for opencv 

* Sun Oct 04 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.7.0-7
- Updated to 2.2.7.0

* Mon Sep 14 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.2.6.1-7
- Updated to 2.2.6.1

* Tue Aug 11 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.18.1-7
- Updated to 2.1.18.1

* Wed Jul 08 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.17.0-7
- Updated to 2.1.17.0

* Wed Jun 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.16.0-8
- Updated to 2.1.16.0

* Sun May 31 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.15.0-8
- Rebuilt for python3.9

* Mon May 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.15.0-7
- Updated to 2.1.15.0

* Thu May 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.14.0-7
- Updated to 2.1.14.0

* Tue Apr 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.1.13.0-7
- Updated to 2.1.13.0

* Sun Dec 29 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.13-8
- Rebuilt for opencv

* Sun Dec 08 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.13-7
- Updated to 2.0.13

* Mon Nov 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.12-7
- Updated to 2.0.12

* Tue Nov 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.10-9
- Rebuilt for OpenColorIO

* Thu Sep 05 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.10-8
- Rebuilt

* Thu Aug 08 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.10-7
- Updated to 2.0.10

* Thu Jul 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.9-7
- Updated to 2.0.9

* Wed May 29 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.0.8-7
- Updated to 2.0.8

* Mon May 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.16-7
- Rebuilt for opencv

* Fri Nov 02 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.16-1
- Update to 1.8.16.

* Tue Oct 02 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.15-1
- Update to 1.8.15.

* Mon Sep 03 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.14-1
- Update to 1.8.14.

* Wed Jul 18 2018 Simone Caronni <negativo17@gmail.com> - 1.8.12-3
- Rebuild for LibRaw update.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.12-1
- Update to 1.8.12.

* Mon Apr 02 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.10-1
- Update to 1.8.10.

* Fri Mar 02 2018 Adam Williamson <awilliam@redhat.com> - 1.8.9-2
- Rebuild for opencv 3.4.1

* Thu Mar 01 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.9-1
- Update to 1.8.9

* Fri Feb 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.8-3
- Rebuild

* Tue Feb 13 2018 Sandro Mani <manisandro@gmail.com> - 1.8.8-2
- Rebuild (giflib)

* Fri Feb 02 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.8-1
- Update to 1.8.8.

* Thu Jan 18 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.7-3
- Add openjpeg2 to build dependencies.
- Re-enable dcmtk for 32bit arches.

* Sat Jan 13 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.7-2
- Rebuild for OpenColorIO 1.1.0.

* Wed Jan 03 2018 Richard Shaw <hobbes1069@gmail.com> - 1.8.7-1
- Update to latest upstream release.
- Disable building with dcmtk until fixed, see:
  https://github.com/OpenImageIO/oiio/issues/1841

* Thu Nov 02 2017 Richard Shaw <hobbes1069@gmail.com> - 1.8.6-1
- Update to latest upstream release.
- Add dcmtk to build to enable DICOM plugin.
