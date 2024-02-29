# Supported targets: el8, el9

Name: microsocks
Version: 1.0.4
Release: 1%{?dist}.zenetys
Summary: Tiny, portable SOCKS5 server with very moderate resource usage
Group: Applications/Communications
License: MIT
URL: https://github.com/rofl0r/microsocks

Source0: https://github.com/rofl0r/microsocks/archive/refs/tags/v%{version}.tar.gz
Source1: microsocks.sysconfig
Source2: microsocks.service

BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd

%description
MicroSocks is a multithreaded, small, efficient SOCKS5 server.

%prep
%setup

%build
make 'CFLAGS=%{build_cflags}' 'LFLAGS=%{build_ldflags}' %{?_smp_mflags}

%install
install -D -m 0755 microsocks %{buildroot}/%{_sbindir}/microsocks
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/microsocks
install -D -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/microsocks.service
install -d -m 0750 %{buildroot}/%{_localstatedir}/lib/microsocks

%pre
if ! getent group microsocks >/dev/null; then
    groupadd -r microsocks
fi
if ! getent passwd microsocks >/dev/null; then
    useradd -r -g microsocks -d %{_localstatedir}/lib/microsocks -s /sbin/nologin microsocks
fi

%post
%systemd_post microsocks.service

%preun
%systemd_preun microsocks.service

%postun
%systemd_postun_with_restart microsocks.service

%files
%doc README.md
%license COPYING
%{_sbindir}/microsocks
%config(noreplace) %{_sysconfdir}/sysconfig/microsocks
%{_unitdir}/microsocks.service
%attr(-, microsocks, microsocks) %dir %{_localstatedir}/lib/microsocks
