#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
%include	/usr/lib/rpm/macros.gstreamer
Summary:	Audio/Video Communications Framework
Summary(pl.UTF-8):	Szkielet komunikacji Audio/Video
Name:		farstream
Version:	0.1.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://freedesktop.org/software/farstream/releases/farstream/%{name}-%{version}.tar.gz
# Source0-md5:	5d6e561b3688d0d0c8906fec4f356df3
URL:		http://www.freedesktop.org/wiki/Software/Farstream
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gobject-introspection-devel >= 0.10.1
BuildRequires:	gstreamer-devel >= 0.10.33
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.33
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gupnp-igd-devel
BuildRequires:	libnice-devel >= 0.1.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-gstreamer-devel >= 0.10.10
BuildRequires:	python-pygobject-devel >= 2.16.0
Requires:	glib2 >= 1:2.30.0
Requires:	gstreamer >= 0.10.33
Requires:	gstreamer-plugins-base >= 0.10.33
Requires:	libnice >= 0.1.0
Obsoletes:	farsight2 < 0.0.32
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
Requires:	glib2-devel >= 1:2.30.0
Requires:	gstreamer-devel >= 0.10.33
Requires:	gstreamer-plugins-base-devel >= 0.10.33
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

%package -n python-farstream
Summary:	Farstream Python bindings
Summary(pl.UTF-8):	Wiązania języka Python do biblioteki Farstream
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-gstreamer >= 0.10.10
Requires:	python-pygobject >= 2.16.0
Obsoletes:	python-farsight2 < 0.0.32

%description -n python-farstream
Farstream Python bindings.

%description -n python-farstream -l pl.UTF-8
Wiązania języka Python do biblioteki Farstream.

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{farstream-0.1,gstreamer-0.10}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libfarstream-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfarstream-0.1.so.0
%{_libdir}/girepository-1.0/Farstream-0.1.typelib
%dir %{_libdir}/farstream-0.1
%attr(755,root,root) %{_libdir}/farstream-0.1/libmulticast-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.1/libnice-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.1/librawudp-transmitter.so
%attr(755,root,root) %{_libdir}/farstream-0.1/libshm-transmitter.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsfunnel.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsmsnconference.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsrawconference.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsrtcpfilter.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsrtpconference.so
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libfsvideoanyrate.so
%{_datadir}/farstream

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfarstream-0.1.so
%{_datadir}/gir-1.0/Farstream-0.1.gir
%{_includedir}/farstream-0.1
%{_pkgconfigdir}/farstream-0.1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfarstream-0.1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/farstream-libs-0.10
%{_gtkdocdir}/farstream-plugins-0.1
%endif

%files -n python-farstream
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/farstream.so
