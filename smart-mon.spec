# This spec file generates an RPM that installs the node_exporter binary
# scripts into the /opt/cray/cray-node-exporter directory.
# Copyright 2020-2021 Hewlett Packard Enterprise Development LP

%define bin_dir /usr/bin
%define script_dir /opt/cray/smartmon

Name: smart-mon
Vendor: Hewlett Packard Enterprise Company
License: HPE Proprietary 
Summary: Install and configuration of smartmon
Version: %(cat .version) 
Release: %(echo ${BUILD_METADATA})
Source: %{name}-%{version}.tar.bz2

# Compiling not currently required:
# BuildArchitectures: noarch

Requires: jq
Requires: python3-boto3

%description
This RPM when installed will install and configure the /usr/bin/node_exporter
binary and corresponding service.

%files
%defattr(755, root, root)
%dir %{bin_dir}
%dir %{script_dir}
%{bin_dir}/smartmon.sh
%{script_dir}/script.sh
# %dir %attr(755,root,root) /var/lib/node_exporter

%prep
%setup -q

%build

%install
# mkdir -p /var/lib/node_exporter
install -m 755 -d %{buildroot}%{bin_dir}/
install -m 755 -d %{buildroot}%{script_dir}/
install -m 755 smartmon.sh %{buildroot}%{bin_dir}
install -m 755 script.sh %{buildroot}%{script_dir}

%post
%{script_dir}/script.sh

