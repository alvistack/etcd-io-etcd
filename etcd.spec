# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: etcd
Epoch: 100
Version: 3.6.0
Release: 1%{?dist}
Summary: Highly-available key value store for configuration and service discovery
License: Apache-2.0
URL: https://github.com/etcd-io/etcd/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.24
BuildRequires: glibc-static

%description
etcd is a distributed, consistent key-value store for shared
configuration and service discovery, with a focus on being:
  - Simple: well-defined, user-facing API (gRPC)
  - Secure: automatic TLS with optional client cert authentication
  - Fast: benchmarked 10,000 writes/sec
  - Reliable: properly distributed using Raft

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    pushd ./server && \
        go build \
            -mod vendor -buildmode pie -v \
            -ldflags "-s -w" \
            -buildmode pie \
            -o ../bin/etcd . && \
    popd && \
    pushd ./etcdctl && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -buildmode pie \
        -o ../bin/etcdctl . && \
    popd && \
    pushd ./etcdutl && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -buildmode pie \
        -o ../bin/etcdutl .

%install
install -Dpm755 -d %{buildroot}%{_sysconfdir}/default
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_docdir}/etcd
install -Dpm755 -d %{buildroot}%{_unitdir}
install -Dpm644 -T etcd.default %{buildroot}%{_sysconfdir}/default/etcd
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcd
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcdctl
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcdutl
install -Dpm644 -t %{buildroot}%{_docdir}/etcd etcd.conf.yml.sample
install -Dpm644 -t %{buildroot}%{_unitdir} contrib/systemd/etcd.service

%files
%license LICENSE
%dir %{_docdir}/etcd
%dir %{_sysconfdir}/default
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_bindir}/etcdutl
%{_docdir}/etcd/etcd.conf.yml.sample
%{_sysconfdir}/default/etcd
%{_unitdir}/etcd.service

%changelog
