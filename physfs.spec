%define	name	physfs
%define	version	1.0.1
%define	release	%mkrel 1

%define	libname_orig 	lib%{name}
%define major		1.0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
 
Name:		%{name}
Summary:	A library to provide abstract access to various archives
Version:	%{version}
Release:	%{release}
License:	zlib
Group:		System/Libraries
Source0:	%{name}-%{version}.tar.bz2
URL:		http://www.icculus.org/physfs/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ncurses-devel readline-devel zlib-devel


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

%build
%configure2_5x 

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{name}.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-, root, root)
%doc CHANGELOG CREDITS LICENSE TODO
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so
