Summary:	FastCGI proxy that starts setuid FastCGI processes on demand
Name:		switchboard
Version:	2.0.16
Release:	0.1
License:	BSD
Group:		Applications
Source0:	https://confluence.toolserver.org/download/attachments/5931011/%{name}-%{version}.tar.gz?version=1
# Source0-md5:	4cb514bc04c6913d309cbb330362574d
Patch0:		%{name}-overquote.patch
URL:		https://confluence.toolserver.org/display/switchboard/Home
BuildRequires:	boost-call_traits-devel
BuildRequires:	boost-devel
BuildRequires:	boost-mem_fn-devel
BuildRequires:	boost-ref-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fcgi_path	/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin

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
%patch0 -p1

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
%ifarch %{x8664}
	--atomic=amd64_gcc \
%endif
%ifarch %{ix86}
	--atomic=i386_gcc \
%endif
%ifnarch %{ix86} %{x8664}
	--atomic=pthread \
%endif
	--safe-path="%{_fcgi_path}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
