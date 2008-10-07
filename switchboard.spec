Summary:	FastCGI proxy that starts setuid FastCGI processes on demand
Name:		switchboard
Version:	2.0.17
Release:	0.1
License:	BSD
Group:		Applications
Source0:	http://www.flyingparchment.org.uk/dump/%{name}-%{version}.tar.gz
# Source0-md5:	6f32beb6b6942c67a187f8f19155731e
URL:		https://confluence.toolserver.org/display/switchboard/Home
BuildRequires:	boost-devel
BuildRequires:	rpm >= 4.4.9-56
%if "%{pld_release}" == "ac"
BuildRequires:	boost-call_traits-devel
BuildRequires:	boost-mem_fn-devel
BuildRequires:	boost-ref-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fcgi_path	/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin
%define		_libdir		%{_prefix}/lib

%description
switchboard is a FastCGI proxy that starts setuid FastCGI processes on
demand, in a similar manner to Apache suexec. switchboard allows mass
web hosting environments to improve security by running FastCGI
scripts as the script owner instead of the web server user, without
the extra overhead that suexec adds. Its PHP support allows PHP
scripts to run as FastCGI processes transparently, without the
overhead of other solutions like mod_suphp.

%prep
%setup -q

%build
# not autoconf configure
CC="%{__cc}" \
CXX="%{__cxx}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
./configure \
	--prefix=%{_prefix} \
	--confdir=%{_sysconfdir} \
	--log-exec=/var/log/%{name}/suexec.log \
	--uid-min=50 \
	--gid-min=50 \
	--user=http \
	--group=http \
	--safe-path="%{_fcgi_path}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	MANDIR=%{_mandir} \
	BINDIR=%{_sbindir} \
	ROOTUSER=%(id -un) \
	ROOTGROUP=%(id -gn) \
	SB_GROUP=%(id -gn) \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/switchboard.conf{.example,}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/switchboard.conf
%attr(755,root,root) %{_sbindir}/switchboard
%attr(755,root,root) %{_sbindir}/switchstats

%dir %{_libdir}/switchboard
%attr(755,root,root) %{_libdir}/switchboard/switchboard-bin
%attr(4710,root,root) %{_libdir}/switchboard/swexec
%attr(4710,root,root) %{_libdir}/switchboard/swkill

%{_datadir}/switchboard/errors/general.html
%{_mandir}/man1/switchstats.1*
%{_mandir}/man4/switchboard.conf.4*
%{_mandir}/man8/switchboard.8*
