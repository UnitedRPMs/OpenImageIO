%global sover 1.8

Name:           OpenImageIO
Version:        1.8.16
Release:        7%{?dist}
Summary:        Library for reading and writing images

License:        BSD
URL:            http://www.openimageio.org
Source0:        https://github.com/OpenImageIO/oiio/archive/Release-%{version}/%{name}-%{version}.tar.gz
# Images for test suite
#Source1:        oiio-images.tar.gz

Patch0:         OpenImageIO-man.patch

BuildRequires:  cmake gcc-c++
BuildRequires:  txt2man
BuildRequires:  qt5-devel
BuildRequires:  boost-devel
%if 0%{?fedora} > 28
BuildRequires:  boost-python2-devel
%else
BuildRequires:  boost-python2-devel
%endif
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif
BuildRequires:  glew-devel
BuildRequires:  OpenEXR-devel ilmbase-devel
BuildRequires:  python2-devel
BuildRequires:  libpng-devel libtiff-devel libjpeg-turbo-devel openjpeg2-devel
BuildRequires:  giflib-devel
BuildRequires:  libwebp-devel
BuildRequires:  Field3D-devel
BuildRequires:  hdf5-devel
BuildRequires:  dcmtk-devel
BuildRequires:  zlib-devel
BuildRequires:  jasper-devel
BuildRequires:  pugixml-devel
BuildRequires:  opencv-devel >= 4.1.0
BuildRequires:  LibRaw-devel
BuildRequires:  openssl-devel

# WARNING: OpenColorIO and OpenImageIO are cross dependent.
# If an ABI incompatible update is done in one, the other also needs to be
# rebuilt.
BuildRequires:  OpenColorIO-devel


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


%package -n python2-openimageio
Summary:        Python 2 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-openimageio
Python bindings for %{name}.


%package utils
Summary:        Command line utilities for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Command-line tools to manipulate and get information on images using the
%{name} library.


%package iv
Summary:        %{name} based image viewer
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description iv
A really nice image viewer, iv, based on %{name} classes (and so will work
with any formats for which plugins are available).


%package devel
Summary:        Documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for package %{name}


%prep
%autosetup -p1 -n oiio-Release-%{version}

# Remove bundled pugixml
rm -f src/include/OpenImageIO/pugixml.hpp \
      src/include/OpenImageIO/pugiconfig.hpp \
      src/libutil/OpenImageIO/pugixml.cpp 

# Remove bundled tbb
rm -rf src/include/tbb

# Install test images
#rm -rf ../oiio-images && mkdir ../oiio-images && pushd ../oiio-images
#tar --strip-components=1 -xzf %{SOURCE1}

# Try disabeling old CMP
sed -i "s/SET CMP0046 OLD/SET CMP0046 NEW/" CMakeLists.txt


%build

rm -rf build/linux && mkdir -p build/linux && pushd build/linux
# CMAKE_SKIP_RPATH is OK here because it is set to FALSE internally and causes
# CMAKE_INSTALL_RPATH to be cleared, which is the desiered result.
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_SKIP_RPATH:BOOL=TRUE \
       -DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
       -DPYTHON_VERSION=2.7
       -DPYLIB_INSTALL_DIR:PATH=%{python2_sitearch} \
       -DBUILD_DOCS:BOOL=TRUE \
       -DINSTALL_DOCS:BOOL=FALSE \
       -DINSTALL_FONTS:BOOL=FALSE \
       -DUSE_EXTERNAL_PUGIXML:BOOL=TRUE \
       -DUSE_OPENSSL:BOOL=TRUE \
       -DSTOP_ON_WARNING:BOOL=FALSE \
       -DUSE_CPP:STRING=14 \
%ifarch ppc ppc64
       -DNOTHREADS:BOOL=FALSE \
%endif
       -DJPEG_INCLUDE_DIR=%{_includedir} \
       -DOPENJPEG_INCLUDE_DIR=$(pkgconf --variable=includedir libopenjp2) \
       -DOpenGL_GL_PREFERENCE=GLVND \
       -DVERBOSE=TRUE \
       ../../

%make_build


%install
pushd build/linux
%make_install

# Move man pages to the right directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -a src/doc/*.1 %{buildroot}%{_mandir}/man1


%check
# Not all tests pass on linux
#pushd build/linux && make test


%files
%doc CHANGES.md README.md
%license LICENSE
%{_libdir}/libOpenImageIO.so.%{sover}*
%{_libdir}/libOpenImageIO_Util.so.%{sover}*

%files -n python2-openimageio
%{python2_sitearch}/OpenImageIO.so

%files utils
%exclude %{_bindir}/iv
%{_bindir}/*
%exclude %{_mandir}/man1/iv.1.gz
%{_mandir}/man1/*.1.gz

%files iv
%{_bindir}/iv
%{_mandir}/man1/iv.1.gz

%files devel
%doc src/doc/*.pdf
%{_libdir}/libOpenImageIO.so
%{_libdir}/libOpenImageIO_Util.so
%{_includedir}/*


%changelog

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
