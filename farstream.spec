#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Audio/Video Communications Framework
Summary(pl.UTF-8):	Szkielet komunikacji Audio/Video
Name:		farstream
Version:	0.2.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://freedesktop.org/software/farstream/releases/farstream/%{name}-%{version}.tar.gz
# Source0-md5:	efedec4a885170d350b5cc43c933f1c0
URL:		http://www.freedesktop.org/wiki/Software/Farstream
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 0.10.1
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gupnp-igd-devel >= 0.2
BuildRequires:	libnice-devel >= 0.1.3
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.32.0
Requires:	gstreamer >= 1.0.0
Requires:	gstreamer-plugins-base >= 1.0.0
Requires:	libnice >= 0.1.3
Obsoletes:	farsight2 < 0.0.32
Obsoletes:	python-farsight2 < 0.0.32
Obsoletes:	python-farstream < 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Farstream (formerly Farsight) project is an effort to create a
framework to deal with all known audio/video conferencing protocols.
On one side it offers a generic API that makes it possible to write
plugins for different streaming protocols, on the other side it offers
an API for clients to use those plugins.

The main target clients for Farstream are Instant Messaging
applications. These applications should be able to use Farstream for
all their Audio/Video conferencing needs without having to worry about
any of the lower level streaming and NAT traversal issues.

%description -l pl.UTF-8
Projekt Farstream (dawniej Farsight) to próba stworzenia szkieletu
obsługującego wszystkie znane protokoły konferencji audio/video. Z
jednej strony oferuje ogólne API umożliwiające pisanie wtyczek dla
różnych protokołów strumieniowych, z drugiej strony oferuje API dla
klientów, pozwalającyce im używać tych wtyczek.

Głównymi klientami szkieletu Farstream mają być aplikacje
komunikatorów (IM). Powinny być w stanie używać Farstreama do potrzeb
konferencji audio/video bez konieczności obsługi niskopoziomowych
poziomów strumieni i omijania NAT-u.

%package devel
Summary:	Header files for Farstream library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Farstream
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	gstreamer-devel >= 1.0.0
Requires:	gstreamer-plugins-base-devel >= 1.0.0
Obsoletes:	farsight2-devel < 0.0.32

%description devel
Header files for Farstream library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Farstream.

%package static
Summary:	Static Farstream library
Summary(pl.UTF-8):	Statyczna biblioteka Farstream
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	farsight2-static < 0.0.32

%description static
Static Farstream library.

%description static -l pl.UTF-8
Statyczna biblioteka Farstream.

%package apidocs
Summary:	Farstream API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Farstream
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	farsight2-apidocs < 0.0.32

%description apidocs
API documentation for Farstream library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Farstream.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{farstream-0.2,gstreamer-1.0}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libfarstream-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfarstream-0.2.so.2
%{_libdir}/girepository-1.0/Farstream-0.2.typelib
%dir %{_libdir}/farstream-0.2
%attr(755,root,root) %{_libdir}/farstream-0.2/libmulticast-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.2/libnice-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.2/librawudp-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.2/libshm-transmitter.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libfsmsnconference.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libfsrawconference.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libfsrtcpfilter.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libfsrtpconference.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libfsvideoanyrate.so
%{_datadir}/farstream

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfarstream-0.2.so
%{_datadir}/gir-1.0/Farstream-0.2.gir
%{_includedir}/farstream-0.2
%{_pkgconfigdir}/farstream-0.2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfarstream-0.2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/farstream-libs-1.0
%{_gtkdocdir}/farstream-plugins-0.2
%endif
