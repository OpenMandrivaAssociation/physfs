%define	name	physfs
%define	version	1.0.1
%define	release	%mkrel 1
%define	lib_name_orig 	lib%{name}
%define lib_major	1.0
%define lib_name	%mklibname %{name} %{lib_major}
 
Name:		%{name}
Summary:	A library to provide abstract access to various archives
Version:	%{version}
Release:	%{release}
License:	zlib License 
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

%package -n	%{lib_name}
Summary:	Main library for physfs
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with physfs

%package -n	%{lib_name}-devel
Summary:	Headers for developing programs that will use physfs
Group:		Development/C 
Requires:	%{lib_name} = %{version} zlib-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
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

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-, root, root)
%doc CHANGELOG CREDITS INSTALL LICENSE TODO
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so
