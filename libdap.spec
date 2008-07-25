%define lib_major       0
%define lib_name        %{mklibname dap %{lib_major}}
%define lib_name_d      %{mklibname dap -d}
%define lib_name_d_s    %{mklibname dap -d -s}

Name:           libdap
Summary:        C++ DAP2 library from OPeNDAP
Version:        3.7.7
Release:        %mkrel 7
Epoch:          0
URL:            http://www.opendap.org/
Source0:        http://www.opendap.org/pub/source/libdap-%{version}.tar.gz
# The deflate program is covered by the W3C licence
License:        LGPL
Group:          System/Libraries
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
# deflate depends directly on zlib
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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

%description doc
Documentation of the libdap library.

%prep
%setup -q

%build
%{configure2_5x} --disable-dependency-tracking
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std} INSTALL="%{__install} -p"

%{make} docs

%{__rm} -rf __mandriva_docs
%{__cp} -a docs __mandriva_docs
# those .map and .md5 are of dubious use, remove them
%{__rm} -f __mandriva_docs/html/*.map __mandriva_docs/html/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files 
# for all archs
/bin/touch -r ChangeLog __mandriva_docs/html/*

%clean
%{__rm} -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING COPYRIGHT_URI README.AIS README.dodsrc
%doc COPYRIGHT_W3C
%{_bindir}/getdap
%{_sbindir}/deflate

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libdap.so.*
%{_libdir}/libdapclient.so.*
%{_libdir}/libdapserver.so.*

%files -n %{lib_name_d}
%defattr(-,root,root,-)
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/*.la
#%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_includedir}/libdap/
%{_datadir}/aclocal/*

%files -n %{lib_name_d_s}
%defattr(-,root,root,-)
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%doc __mandriva_docs/html/
