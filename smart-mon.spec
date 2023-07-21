# This spec file generates an RPM that installs the node_exporter binary
# scripts into the /opt/cray/cray-node-exporter directory.
# Copyright 2020-2021 Hewlett Packard Enterprise Development LP

%define bin_dir /usr/bin
%define script_dir /opt/cray/smartmon
%define etc_ceph_dir /etc/cray/ceph
%define node_exporter_dir /var/lib/node_exporter
%define short_name smart
Name: %{short_name}-mon
Vendor: Hewlett Packard Enterprise Company
License: HPE Proprietary
Summary: Install and configuration of smartmon
Version: %(cat .version)
Release: %(echo ${BUILD_METADATA})
Source: %{name}-%{version}.tar.bz2

BuildArch: noarch

Requires: jq
Requires: python3-boto3

# helps when installing a program whose unit files makes use of a feature only available in a newer systemd version
# If the program is installed on its own, it will have to make do with the available features
# If a newer systemd package is planned to be installed in the same transaction as the program,
# it can be beneficial to have systemd installed first, so that the features have become available by the time program is installed and restarted
%{?systemd_ordering}

%description
This RPM when installed will install and configure the /usr/bin/node_exporter
binary and corresponding service.

%files
%defattr(755, root, root)
%dir %{bin_dir}
%dir %{script_dir}
%dir %{etc_ceph_dir}
%dir %{node_exporter_dir}
%{bin_dir}/%{short_name}mon.sh
%{etc_ceph_dir}/node-exporter.yml
%attr(644, root, root) %{_unitdir}/%{short_name}.service

%prep
%setup -q

%build

%install
install -m 755 -d %{buildroot}%{bin_dir}/
install -m 755 -d %{buildroot}%{script_dir}/
install -m 755 -d %{buildroot}%{etc_ceph_dir}/
install -m 200 -d %{buildroot}%{node_exporter_dir}
install -D -m 0644 -t %{buildroot}%{_unitdir} %{short_name}.service
install -m 755 %{short_name}mon.sh %{buildroot}%{bin_dir}
install -m 755 node-exporter.yml %{buildroot}%{etc_ceph_dir}

%pre
%service_add_pre %{short_name}.service

%post
%service_add_post %{short_name}.service

%preun
%service_del_preun %{short_name}.service

%postun
%service_del_postun %{short_name}.service
