%global debug_package %{nil}

Name: etcd
Epoch: 100
Version: 3.5.1
Release: 1%{?dist}
Summary: Highly-available key value store for configuration and service discovery
License: Apache-2.0
URL: https://github.com/etcd-io/etcd/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.18
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
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_docdir}/etcd
install -Dpm755 -d %{buildroot}%{_userunitdir}
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcd
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcdctl
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/etcdutl
install -Dpm644 -t %{buildroot}%{_docdir}/etcd etcd.conf.yml.sample
install -Dpm644 -t %{buildroot}%{_userunitdir} contrib/systemd/etcd.service

%files
%license LICENSE
%dir %{_docdir}/etcd
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_bindir}/etcdutl
%{_docdir}/etcd/etcd.conf.yml.sample
%{_userunitdir}/etcd.service

%changelog
