Summary:	Utility for managing filesystem extended attributes
Summary(pl):	Narzêdzia do zarz±dzania rozszerzonymi atrybutami fs
Name:		attr
Version:	2.4.7
Release:	1
# most part is on LGPL v2.1, but the rest enforces GPL
License:	GPL
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
# Source0-md5:	56e67402f5075ce47b5657b4336ff563
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfsprogs-devel >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_libdir		/lib
%define		_libexecdir	/usr/lib

%description
An experimental attr command to manipulate extended attributes under
Linux.

%description -l pl
Eksperymentalna wersja polecenia attr to zarz±dzania rozszerzonymi
atrybutami pod systemem Linux.

%package devel
Summary:	Header files and libraries to use extended attributes
Summary(pl):	Pliki nag³ówkowe i biblioteki
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files to develop software which manipulate extended attributes.

%description devel -l pl
Pliki nag³ówkowe potrzebne do tworzenia oprogramowania manipuluj±cego
rozszerzonymi atrybutami.

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
%setup -q
%patch0 -p1

%build
rm -f aclocal.m4
%{__aclocal} -I m4
%{__autoconf}
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT=$RPM_BUILD_ROOT
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB

%{__make} install \
	DIST_MANIFEST=$DIST_INSTALL
%{__make} install-dev \
	DIST_MANIFEST=$DIST_INSTALL_DEV
%{__make} install-lib \
	DIST_MANIFEST=$DIST_INSTALL_LIB

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_getf,attr_listf}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_multif,attr_removef,attr_setf}.3
rm -rf	$RPM_BUILD_ROOT%{_mandir}/man2

ln -sf %{_libdir}/$(cd $RPM_BUILD_ROOT%{_libdir} ; echo libattr.so.*.*.*) \
	 $RPM_BUILD_ROOT%{_libexecdir}/libattr.so

echo ".so attr_get.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_getf.3
echo ".so attr_list.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_listf.3
echo ".so attr_multi.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_multif.3
echo ".so attr_remove.3" > $RPM_BUILD_ROOT%{_mandir}/man3/attr_removef.3
echo ".so attr_set.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_setf.3

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/CHANGES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man[158]/*

%files devel
%defattr(644,root,root,755)
%{_libexecdir}/lib*.la
%attr(755,root,root) %{_libexecdir}/lib*.so
%{_includedir}/attr
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/lib*.a
