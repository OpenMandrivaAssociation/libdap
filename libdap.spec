%define major 11
%define cmajor 3
%define smajor 7
%define libname %mklibname dap %{major}
%define libclient %mklibname dapclient %{cmajor}
%define libserver %mklibname dapserver %{smajor}
%define devname %mklibname dap -d

Summary:	C++ DAP2 library from OPeNDAP
Name:		libdap
Version:	3.12.1
Release:	4
# The deflate program is covered by the W3C licence
License:	LGPLv2.1+
Group:		System/Libraries
Url:		https://www.opendap.org/
Source0:	http://www.opendap.org/pub/source/libdap-%{version}.tar.gz
Patch0:		libdap-3.12.0-tirpc.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	groff
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(uuid)

%description
The libdap++ library contains an implementation of DAP2. This package
contains the library, dap-config, getdap and deflate. The script dap-config
simplifies using the library in other projects. The getdap utility is a
simple command-line tool to read from DAP2 servers. It is built using the
library and demonstrates simple uses of it. The deflate utility is used by
the library when it returns compressed responses.

%files
%doc README NEWS COPYING COPYRIGHT_URI README.dodsrc COPYRIGHT_W3C
%{_bindir}/getdap
%{_mandir}/man1/getdap.1*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	C++ DAP2 library from OPeNDAP
Group:		System/Libraries

%description -n %{libname}
C++ DAP2 library from OPeNDAP.

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libdap.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libclient}
Summary:	C++ DAP2 library from OPeNDAP
Group:		System/Libraries
Conflicts:	%{_lib}dap10 < 3.12.0

%description -n %{libclient}
C++ DAP2 library from OPeNDAP.

%files -n %{libclient}
%defattr(-, root, root)
%{_libdir}/libdapclient.so.%{cmajor}*

#----------------------------------------------------------------------------

%package -n %{libserver}
Summary:	C++ DAP2 library from OPeNDAP
Group:		System/Libraries
Conflicts:	%{_lib}dap10 < 3.12.0

%description -n %{libserver}
C++ DAP2 library from OPeNDAP.

%files -n %{libserver}
%defattr(-, root, root)
%{_libdir}/libdapserver.so.%{smajor}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development and header files from libdap
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Requires:	%{libclient} = %{EVRD}
Requires:	%{libserver} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}dap-static-devel < 3.12.0

%description -n %{devname}
This package contains all the files needed to develop applications that
will use libdap.

%files -n %{devname}
%defattr(-, root, root)
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_bindir}/dap-config-pkgconfig
%{_includedir}/libdap/
%{_datadir}/aclocal/*
%{_mandir}/man1/dap-config.1*

#----------------------------------------------------------------------------

%package doc
Summary:	Documentation of the libdap library
Group:		Development/C
BuildArch:	noarch

%description doc
Documentation of the libdap library.

%files doc
%doc __mandriva_docs/html/

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

%build
autoreconf -fiv
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

%make docs

rm -rf __mandriva_docs
cp -a docs __mandriva_docs
# those .map and .md5 are of dubious use, remove them
rm -f __mandriva_docs/html/*.map __mandriva_docs/html/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files
# for all archs
touch -r ChangeLog __mandriva_docs/html/*

rm -f %{buildroot}%{_libdir}/*.a

