Name:		  sgx-driver
Version:	2.5
Release:	0%{?dist}.1
Summary:	Intel SGX kernel module

License:	GPLv2
URL:		  https://github.com/intel/linux-sgx-driver
#Source0:	https://github.com/intel/linux-sgx-driver/archive/sgx_driver_2.5.tar.gz

ExclusiveArch: i686 x86_64
Provides:      %{name}-kmod-common = %{version}
Requires:      %{name}-kmod >= %{version}

%description
Intel SGX kernel moduule common files.

%prep
#setup -q -c

%build
# Nothing to build.

%install
#Nothing to install.

%files

%changelog
* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
