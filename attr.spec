Summary:	Utility for managing filesystem extended attributes
Summary(pl):	Narzędzia do zarządzania rozszerzonymi atrybutami fs
Name:		attr
Version:	2.0.8
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfsprogs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
An experimental attr command to manipulate extended attributes under
Linux.

%description -l pl
Eksperymentalne wersja polecenia attr to zarządzania rozszerzonymi
atrybutami pod systemem Linux.

%package devel
Summary:	Header files and libraries to use extended attributes
Summary(pl):	Pliki nagłówkowe i biblioteki
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and libraries to develop software which manipulate
extended attributes.

%description devel -l pl
Pliki nagłówkowe i biblioteki potrzebne do rozwoju oprogramowania
manipulującego rozszerzonymi atrybutami.

%package static
Summary:	Static libraries for extended attributes
Summary(pl):	Biblioteki statyczne attr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libraries for extended attributes.

%description static -l pl
Biblioteki statyczne attr.

%prep
%setup  -q
%patch0 -p1

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB

%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
%{__make} install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_getf,attr_listf}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_multif,attr_removef,attr_setf}.3

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -sf /lib/libattr.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libattr.so

echo ".so attr_get.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_getf.3
echo ".so attr_list.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_listf.3
echo ".so attr_multi.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_multif.3
echo ".so attr_remove.3" > $RPM_BUILD_ROOT%{_mandir}/man3/attr_removef.3
echo ".so attr_set.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_setf.3

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/CHANGES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /lib/lib*.so.*.*
%{_mandir}/man[18]/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/attr
%{_mandir}/man[23]/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
