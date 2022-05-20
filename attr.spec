Summary:	Utility for managing filesystem extended attributes
Summary(pl.UTF-8):	Narzędzia do zarządzania rozszerzonymi atrybutami systemu plików
Name:		attr
Version:	2.5.1
Release:	1
License:	LGPL v2+ (library), GPL v2+ (utilities)
Group:		Applications/System
Source0:	http://download.savannah.nongnu.org/releases/attr/%{name}-%{version}.tar.xz
# Source0-md5:	e459262266bbd82b3dd348fc8cc68a6d
URL:		http://savannah.nongnu.org/projects/attr/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.18.2
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.402
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	libattr < 2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
An experimental attr command to manipulate extended attributes under
Linux.

%description -l pl.UTF-8
Eksperymentalna wersja polecenia attr to zarządzania rozszerzonymi
atrybutami pod systemem Linux.

%package devel
Summary:	Header files and libraries to use extended attributes
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki do korzystania z rozszerzonych atrybutów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files to develop software which manipulate extended attributes.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do tworzenia oprogramowania manipulującego
rozszerzonymi atrybutami.

%package static
Summary:	Static libraries for extended attributes
Summary(pl.UTF-8):	Biblioteki statyczne do korzystania z rozszerzonych atrybutów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for extended attributes.

%description static -l pl.UTF-8
Biblioteki statyczne do korzystania z rozszerzonych atrybutów.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libattr.so.* \
	$RPM_BUILD_ROOT/%{_lib}

ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libattr.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libattr.so

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/CHANGES
%attr(755,root,root) %{_bindir}/attr
%attr(755,root,root) %{_bindir}/getfattr
%attr(755,root,root) %{_bindir}/setfattr
%attr(755,root,root) /%{_lib}/libattr.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libattr.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xattr.conf
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libattr.so
%{_libdir}/libattr.la
%{_includedir}/attr
%{_pkgconfigdir}/libattr.pc
%{_mandir}/man3/attr_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libattr.a
