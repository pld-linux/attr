Summary:	Utility for managing filesystem extended attributes
Summary(pl):	Narzêdzia do zarz±dzania rozszerzonymi atrybutami fs
Name:		attr
Version:	1.1.3
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfsprogs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
An *experimental* command (attr) to manipulate extended attributes
under Linux.

%description -l pl
*Eksperymentalna* komenda (attr) to zarz±dzania rozszerzonymi
atrybutami pod systemem Linux.

%package devel
Summary:	Header files and libraries to use extended attributes
Summary(pl):	Pliki nag³ówkowe i biblioteki
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki

%description devel
Header files and libraries to develop software which manipulate
extended attributes.

%description -l pl devel
Pliki nag³ówkowe i biblioteki potrzebne do rozwoju oprogramowania
manipuluj±cego rozszerzonymi atrybutami.

%prep
%setup  -q
%patch0 -p1

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
autoconf
%configure 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV 
%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_getf,attr_listf}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{attr_multif,attr_removef,attr_setf}.3

echo ".so man3/attr_get.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_getf.3
echo ".so man3/attr_list.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_listf.3
echo ".so man3/attr_multi.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_multif.3
echo ".so man3/attr_remove.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_removef.3
echo ".so man3/attr_set.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/attr_setf.3

gzip -9nf doc/CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man[18]/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/attr
%{_mandir}/man[23]/*
