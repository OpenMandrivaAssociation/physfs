%define	name	physfs
%define	version	2.0.2

%define	libname_orig 	lib%{name}
%define major		2
%define compat_major	1
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
 
Name:		%{name}
Summary:	A library to provide abstract access to various archives
Version:	%{version}
Release:	%mkrel 1
License:	zlib
Group:		System/Libraries
Source0:	http://www.icculus.org/physfs/downloads/%{name}-%{version}.tar.gz
Patch0:		physfs-2.0.2-fix-build.patch
URL:		http://www.icculus.org/physfs/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	liblzma-devel
BuildRequires:	cmake


%description
A library to provide abstract access to various archives. 
It is intended for use in video games. 
The programmer defines a "write directory" on the physical filesystem. 
No file writing done through the PhysicsFS API can leave that write directory.

%package -n	%{libname}
Summary:	Main library for physfs
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with physfs

%package -n	%{develname}
Summary:	Headers for developing programs that will use physfs
Group:		Development/C 
Requires:	%{libname} = %{version} zlib-devel
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname physfs 1.0 -d}

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use physfs

%prep
%setup -q
%patch0 -p0

# Ensure we use system zlib  
# don't use bundled lzma
rm -rf zlib123
rm -rf lzma

%build
%cmake -DPHYSFS_ARCHIVE_7Z=OFF
%make


%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.%{major}*
%{_libdir}/*.so.%{compat_major}

%files -n %{develname}
%defattr(-, root, root)
%doc %{_docdir}%{name}/*.txt
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.so
