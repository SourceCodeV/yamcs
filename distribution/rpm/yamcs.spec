Name: yamcs
Version: @@VERSION@@
Release: @@RELEASE@@

Group: Unspecified
Summary: Yamcs Mission Control

Vendor: Space Applications Services
Packager: Yamcs Team <yamcs@spaceapplications.com>
License: Affero GPL v3
URL: https://yamcs.org
Prefix: /opt/yamcs
BuildArch: x86_64

Requires: socat


%description
Yamcs Mission Control


%define debug_package %{nil}
%define __arch_install_post %{nil}
%define __os_install_post %{nil}


%install
cd %{name}-%{version}-%{release}

mkdir -p %{buildroot}
cp -r opt %{buildroot}
cp -r usr %{buildroot}


%pre
if [ "$1" = 1 -o "$1" = install ] ; then
    groupadd -r yamcs >/dev/null 2>&1 || :
    useradd -M -r -d %{prefix} -g yamcs -s /bin/false -c "Yamcs daemon" yamcs >/dev/null 2>&1 || :
fi


%post
systemctl daemon-reload


%preun
if [ "$1" == 0 ]; then
    systemctl unmask yamcs.service
    systemctl stop yamcs.service
    systemctl disable yamcs.service
fi


%postun
if [ "$1" = 0 -o "$1" = remove ]; then
    userdel yamcs >/dev/null 2>&1 || :
    groupdel yamcs >/dev/null 2>&1 || :
    systemctl daemon-reload
    systemctl reset-failed
fi


%files
%defattr(-,root,root)

%dir %{prefix}
%config %{prefix}/mdb
%config %{prefix}/etc
%{prefix}/lib
/usr/lib/systemd/system/*

%dir %{prefix}/bin
%attr(755, root, root) %{prefix}/bin/*

%attr(-,yamcs,yamcs) %{prefix}/cache
%attr(-,yamcs,yamcs) %{prefix}/log
