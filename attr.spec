Summary:	Utility for managing filesystem extended attributes
Summary(pl.UTF-8):	Narzędzia do zarządzania rozszerzonymi atrybutami systemu plików
Name:		attr
Version:	2.4.47
Release:	1
License:	LGPL v2+ (library), GPL v2+ (utilities)
Group:		Applications/System
Source0:	http://git.savannah.gnu.org/cgit/attr.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	4ee36c16eb7e58a1b38345d4dbbddd88
Patch0:		%{name}-miscfix.patch
Patch1:		%{name}-lt.patch
Patch2:		%{name}-LDFLAGS.patch
URL:		http://savannah.nongnu.org/projects/attr/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.402
Obsoletes:	libattr
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_libdir		/%{_lib}
%define		_libexecdir	/usr/%{_lib}

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__rm} -f aclocal.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
install %{_datadir}/automake/config.* .
install include/install-sh .

%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags} -DENABLE_GETTEXT"

%{__make} \
	LLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libexecdir}

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

mv $RPM_BUILD_ROOT%{_libdir}/libattr.{la,a} \
	$RPM_BUILD_ROOT%{_libexecdir}

ln -sf %{_libdir}/$(basename $RPM_BUILD_ROOT%{_libdir}/libattr.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libexecdir}/libattr.so

%{__sed} -i "s|libdir='%{_libdir}'|libdir='%{_libexecdir}'|" \
	$RPM_BUILD_ROOT%{_libexecdir}/libattr.la

%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man2

%find_lang %{name}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# already in /usr
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libattr.so

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
%attr(755,root,root) %{_libdir}/libattr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libattr.so.1
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*
%{_mandir}/man5/attr.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/libattr.so
%{_libexecdir}/libattr.la
%{_includedir}/attr
%{_mandir}/man3/attr_*.3*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/libattr.a
