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
Release:	%mkrel 2
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


%changelog
* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 2.0.2-1mdv2011.0
+ Revision: 669169
- new version 2.0.2
- fix build with gcc 4.6

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-2mdv2011.0
+ Revision: 607171
- rebuild

* Thu Mar 25 2010 Emmanuel Andry <eandry@mandriva.org> 2.0.1-1mdv2010.1
+ Revision: 527549
- New version 2.0.1
- drop p0 (merged upstream)
- don't use bundled lzma

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-3mdv2010.1
+ Revision: 523630
- rebuilt for 2010.1

* Wed Jul 29 2009 Emmanuel Andry <eandry@mandriva.org> 2.0.0-2mdv2010.0
+ Revision: 403857
- fix 64 bits build
- New version 2.0.0
- p0 from mercurial to fix build
- update files list
- BR cmake

* Sun Mar 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1-6mdv2009.1
+ Revision: 355509
- rebuild for latest readline

* Sun Mar 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1-5mdv2009.1
+ Revision: 355333
- rebuild for latest readline

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.0.1-4mdv2009.0
+ Revision: 224917
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3mdv2008.1
+ Revision: 179235
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2008.1
+ Revision: 179215
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Jul 31 2007 Adam Williamson <awilliamson@mandriva.org> 1.0.1-1mdv2008.0
+ Revision: 56932
- rebuild for 2008
- no need to package installation instructions
- move docs to devel package to respect library policy
- new devel policy

  + Emmanuel Andry <eandry@mandriva.org>
    - Import physfs


 
* Thu Jul 20 2006 Emmanuel Andry <eandry@mandriva.org> 1.0.1-1mdv2007.0
- 1.0.1
- %%mkrel

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.0.0-2mdk
- rebuild for new readline
- fix summary-ended-with-dot

* Fri Jun 04 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.0.0-1mdk
- 1.0.0
- bump major
- cosmetics

* Tue Oct 07 2003 Charles A Edwards <eslrahc@bellsouth.net> 0.1.9-1mdk
- initial mdk pkg
