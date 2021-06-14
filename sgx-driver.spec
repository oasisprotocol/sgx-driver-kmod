Name: sgx-driver
Version: 2.6
Release: 2%{?dist}
Summary: Intel SGX kernel module
License: GPLv2

URL: https://github.com/intel/linux-sgx-driver
Source0: https://github.com/intel/linux-sgx-driver/archive/sgx_driver_%{version}.tar.gz

ExclusiveArch: i686 x86_64
Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

%description
Intel SGX kernel moduule common files.

%prep
# Nothing to prepare.

%build
# Nothing to build.

%install
# Nothing to install.

%files

%changelog
* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.6-2
- Refactor and modernize the SPEC file.

* Thu Oct 17 2019 Yawning Angel <yawning@schwanenlied.me> - 2.6-1
- Update to upstream release 2.6.

* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
