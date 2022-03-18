%define major	3
%define compat_major	1
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	A library to provide abstract access to various archives
Name:		physfs
Version:	3.0.2
Release:	2
License:	zlib
Group:		System/Libraries
Url:		http://www.icculus.org/physfs/
Source0:	http://www.icculus.org/physfs/downloads/%{name}-%{version}.tar.bz2
Source100:	physfs.rpmlintrc
BuildRequires:	cmake
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(zlib)

%description
A library to provide abstract access to various archives. 
It is intended for use in video games. 
The programmer defines a "write directory" on the physical filesystem. 
No file writing done through the PhysicsFS API can leave that write directory.

%package -n	%{libname}
Summary:	Main library for physfs
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with physfs

%package -n	%{devname}
Summary:	Headers for developing programs that will use physfs
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use physfs

%prep
%setup -q
#patch0 -p0

# Ensure we use system zlib  
# don't use bundled lzma
rm -rf zlib123
rm -rf lzma

%build
%cmake -DPHYSFS_ARCHIVE_7Z=OFF
%make

%install
# fix 64 bits lib path 
%ifarch x86_64
cd build
sed -i -e 's,lib",lib64",g' cmake_install.cmake
cd ..
%endif

%makeinstall_std -C build

install -d %{buildroot}%{_docdir}%{name}
install *.txt %{buildroot}%{_docdir}%{name}/

rm -rf %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%{_libdir}/libphysfs.so.%{major}*
%{_libdir}/libphysfs.so.%{compat_major}

%files -n %{devname}
%doc %{_docdir}%{name}/*.txt
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
