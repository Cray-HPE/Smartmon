# This spec file generates an RPM that installs the node_exporter binary
# scripts into the /opt/cray/cray-node-exporter directory.
# Copyright 2020-2021 Hewlett Packard Enterprise Development LP

%define etc_ceph_dir /etc/cray/ceph
%define node_exporter_dir /var/lib/node_exporter
%define unit_dir /etc/systemd/system

Name: smart-mon
Vendor: Hewlett Packard Enterprise Company
License: HPE Proprietary 
Summary: Install and configuration of smartmon
Version: %(cat .version) 
Release: %(echo ${BUILD_METADATA})
Source: %{name}-%{version}.tar.bz2

# helps when installing a program whose unit files makes use of a feature only available in a newer systemd version
# If the program is installed on its own, it will have to make do with the available features
# If a newer systemd package is planned to be installed in the same transaction as the program,
# it can be beneficial to have systemd installed first, so that the features have become available by the time program is installed and restarted
%{?systemd_ordering}

BuildArch: noarch
#BuildRequires: systemd-rpm-macros
#Requires(post): systemd
#Requires(preun): systemd

%description
This RPM when installed will install and configure the /usr/bin/node_exporter
binary and corresponding service.

%files
%defattr(755, root, root)
%dir %{etc_ceph_dir}
%dir %{node_exporter_dir}
%{_bindir}/smartmon.sh
%{unit_dir}/smart.service
#%{_unitdir}/smart.service
%{etc_ceph_dir}/node-exporter.yml

%prep
%setup -q

%build

%install
install -m 755 -d %{buildroot}%{_bindir}/
#install -m 755 -d %{buildroot}%{_unitdir}/
install -m 755 -d %{buildroot}%{unit_dir}/
install -m 755 -d %{buildroot}%{etc_ceph_dir}/
install -m 755 -d %{buildroot}%{node_exporter_dir}/
install -m 755 smartmon.sh %{buildroot}%{_bindir}
#install -m 644 smart.service %{buildroot}%{_unitdir}
install -m 644 smart.service %{buildroot}%{unit_dir}
install -m 755 node-exporter.yml %{buildroot}%{etc_ceph_dir}

%pre
%service_add_pre smart.service

%post
%service_add_post smart.service

%preun
%service_del_preun smart.service

%postun
%service_del_postun smart.service
