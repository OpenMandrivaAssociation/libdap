%define lib_major       10
%define client_major 	3
%define server_major 	7
%define lib_name        %mklibname dap %{lib_major}
%define lib_name_d      %mklibname dap -d
%define lib_name_d_s    %mklibname dap -d -s

Name:           libdap
Summary:        C++ DAP2 library from OPeNDAP
Version:        3.9.3
Release:        6
Epoch:          0
URL:            http://www.opendap.org/
Source0:        http://www.opendap.org/pub/source/libdap-%{version}.tar.gz
Patch0:         libdap-3.9.2-gcc-4.4.patch
Patch1:         libdap-3.9.3-curl.patch
# The deflate program is covered by the W3C licence
License:        LGPL 2.1+
Group:          System/Libraries
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  cppunit-devel
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
# deflate depends directly on zlib
BuildRequires:  zlib-devel

%description
The libdap++ library contains an implementation of DAP2. This package
contains the library, dap-config, getdap and deflate. The script dap-config
simplifies using the library in other projects. The getdap utility is a
simple command-line tool to read from DAP2 servers. It is built using the
library and demonstrates simple uses of it. The deflate utility is used by
the library when it returns compressed responses.

%package -n %{lib_name}
Summary:        C++ DAP2 library from OPeNDAP
Group:          System/Libraries
Conflicts:	%{_lib}dap9 < 3.9.0

%description -n %{lib_name}
C++ DAP2 library from OPeNDAP.

%package -n %{lib_name_d}
Summary:        Development and header files from libdap
Group:          Development/C
Provides:       libdap-devel = %version
Requires:       %{lib_name} = %{epoch}:%{version}-%{release}
Requires:       libcurl-devel
Requires:       libxml2-devel
Requires:       pkgconfig
# for the /usr/share/aclocal directory ownership
Requires:       automake
Obsoletes:	%{_lib}dap0-devel

%description -n %{lib_name_d}
This package contains all the files needed to develop applications that
will use libdap.

%package -n %{lib_name_d_s}
Summary:        Static development files from libdap
Group:          Development/C
Provides:       %{name}-static-devel = %{epoch}:%{version}-%{release}
Requires:       %{lib_name_d} = %{epoch}:%{version}-%{release}
Obsoletes:	%{_lib}dap0-static-devel

%description -n %{lib_name_d_s}
This package contains all the files needed to develop applications that
will use libdap.

%package doc
Summary:        Documentation of the libdap library
Group:          Development/C
BuildArch: noarch

%description doc
Documentation of the libdap library.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
autoreconf -fiv
%configure2_5x --disable-dependency-tracking --with-system-zlib
%make

%install
%{makeinstall_std} INSTALL="%{__install} -p"

%{make} docs

%{__rm} -rf __mandriva_docs
cp -a docs __mandriva_docs
# those .map and .md5 are of dubious use, remove them
%{__rm} -f __mandriva_docs/html/*.map __mandriva_docs/html/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files 
# for all archs
/bin/touch -r ChangeLog __mandriva_docs/html/*

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING COPYRIGHT_URI README.AIS README.dodsrc
%doc COPYRIGHT_W3C
%{_bindir}/getdap
%{_sbindir}/deflate

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libdap.so.%{lib_major}
%{_libdir}/libdap.so.%{lib_major}.*
%{_libdir}/libdapclient.so.%{client_major}
%{_libdir}/libdapclient.so.%{client_major}.*
%{_libdir}/libdapserver.so.%{server_major}
%{_libdir}/libdapserver.so.%{server_major}.*

%files -n %{lib_name_d}
%defattr(-,root,root,-)
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_bindir}/dap-config-pkgconfig
%{_includedir}/libdap/
%{_datadir}/aclocal/*

%files -n %{lib_name_d_s}
%defattr(-,root,root,-)
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%doc __mandriva_docs/html/


%changelog
* Fri Jan 07 2011 Thierry Vignaud <tv@mandriva.org> 0:3.9.3-5mdv2011.0
+ Revision: 629719
- make doc subpackage noarch

* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:3.9.3-4mdv2011.0
+ Revision: 620088
- the mass rebuild of 2010.0 packages

* Thu Oct 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0:3.9.3-3mdv2010.0
+ Revision: 455885
- rebuild for new curl SSL backend

* Fri Aug 21 2009 Funda Wang <fwang@mandriva.org> 0:3.9.3-2mdv2010.0
+ Revision: 418900
- conflict with old lib

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 0:3.9.3-1mdv2010.0
+ Revision: 418589
- New version 3.9.3
- drop P0
- add patch to fix build with gcc44
- use autoreconf
- new majors

* Sun Aug 17 2008 David Walluck <walluck@mandriva.org> 0:3.8.2-1mdv2009.0
+ Revision: 272861
- fix build
- add libdap-3.8.2-link.patch

  + Emmanuel Andry <eandry@mandriva.org>
    - New version
    - protect majors

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Feb 08 2008 Helio Chissini de Castro <helio@mandriva.com> 0:3.7.7-5mdv2008.1
+ Revision: 164049
- Proper devel naming without soname

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 25 2007 David Walluck <walluck@mandriva.org> 0:3.7.7-4mdv2008.1
+ Revision: 101973
- remove incorrect lib provides
- remove versioned BuildRequires

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 0:3.7.7-3mdv2008.0
+ Revision: 36182
- rebuild with correct optflags

  + David Walluck <walluck@mandriva.org>
    - fix lib name
    - fix Group
    - Import libdap



* Wed Jun 06 2007 David Walluck <walluck@mandriva.org> 0:3.7.7-1mdv2008.0
- release
