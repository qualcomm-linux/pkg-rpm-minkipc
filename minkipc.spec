Name:		minkipc
Version:	1.2.9
Release:	1%{?dist}
Summary:	IPC framework for Qualcomm TEE

License:	BSD-3-Clause
URL:		https://github.com/qualcomm/minkipc
Source0:	https://github.com/qualcomm/minkipc/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:		minkipc-idlc-aarch64.patch

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	qcbor-devel
BuildRequires:	quic-teec-devel
BuildRequires:	systemd-rpm-macros

%description
MinkIPC is Qualcomm’s lightweight capability-based inter-process communication (IPC) framework.
It enables secure, synchronous message passing across different security domains—like Linux
user space to Trusted Execution Environment—using unforgeable object references and transport
mechanisms such as SMC, sockets, or TEE IOCTLs.


%package libs
Summary: Shared library for Qualcomm MinkIPC

%description libs
This package consists of the shared library libminkadaptor and libminkteec.


%package devel
Summary: Development files for Qualcomm MinkIPC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package consists of header files and unversioned linker symlinks for development
of MinkIPC


%package qteesupplicant
Summary: Support daemons and udev rules for Qualcomm MinkIPC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description qteesupplicant
This package consists of the qteesupplicant and sfsconfig systemd services along with
its necessary shared library internal to qteesupplicant. It includes udev rules as well
for qteesupplicant to access QTEE.


%package tools
Summary: Additional tools for Qualcomm MinkIPC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description tools
This package consists of tools such as rpmb_client.


%package tests
Summary: Test application for Qualcomm MinkIPC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description tests
This package provides test binaries for validating MinkIPC functionality,
including smcinvoke_client for SMC invocation testing and gp_test_client
for GlobalPlatform TEE API conformance testing.


%prep
%setup
%patch -P0 -p1


%build
%cmake \
  -DSYSTEMD_UNIT_DIR=/usr/lib/systemd/system \
  -DUDEV_DIR=/usr/lib/udev/rules.d \
  -DBUILD_UNITTEST=TRUE \
  -DDISTRO_USER=securemsm \
  -DDISTRO_GROUP=securemsm \
  -DBUILD_PKCS11=OFF
%cmake_build


%install
%cmake_install

# not installed
rm -f %{buildroot}%{_libdir}/libfsservice.so
rm -f %{buildroot}%{_libdir}/libgpfsservice.so
rm -f %{buildroot}%{_libdir}/librpmbservice.so
rm -f %{buildroot}%{_libdir}/libtaautoload.so
rm -f %{buildroot}%{_libdir}/libtimeservice.so

%files libs
%license LICENSE.txt
%doc README.md
%{_libdir}/libminkadaptor.so.*
%{_libdir}/libminkteec.so.*

%files devel
%{_libdir}/libminkadaptor.so
%{_libdir}/libminkteec.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files qteesupplicant
%{_bindir}/qtee_supplicant
%{_libexecdir}/sfs_config
%{_udevrulesdir}/99-qcomtee-udev.rules
%{_unitdir}/qteesupplicant.service
%{_unitdir}/sfsconfig.service
%{_libdir}/libfsservice.so.*
%{_libdir}/libgpfsservice.so.*
%{_libdir}/libtimeservice.so.*
%{_libdir}/libtaautoload.so.*
%{_libdir}/librpmbservice.so.*

%files tools
%{_bindir}/rpmb_client

%files tests
%{_bindir}/smcinvoke_client
%{_bindir}/gp_test_client


%pre qteesupplicant
if ! getent group securemsm > /dev/null 2>&1; then
    groupadd securemsm
fi
if ! getent passwd securemsm > /dev/null 2>&1; then
    useradd -s /usr/sbin/nologin -g securemsm securemsm
fi

%post qteesupplicant
%systemd_post sfsconfig.service
%systemd_post qteesupplicant.service

%preun qteesupplicant
%systemd_preun qteesupplicant.service
%systemd_preun sfsconfig.service

%postun qteesupplicant
%systemd_postun_with_restart qteesupplicant.service
%systemd_postun_with_restart sfsconfig.service


%changelog
* Wed Sep 02 2026 Abhinaba Rakshit <abhinaba.rakshit@oss.qualcomm.com> - 1.2.9-1
- Initial RPM package with upstream v1.2.9
