# Uncomment the following to use a pre-release.
#global git_date 20210420
#global git_commit 2d2b795890c01069aab21d4cdfd1226f7f65b971
%{?git_commit:%global git_commit_hash %(c=%{git_commit}; echo ${c:0:7})}

%if 0%{?git_date}
%global git_tag %{git_commit_hash}
%else
%global git_tag sgx_driver_%{version}
%endif

Name: sgx-driver
Version: 2.11
Release: 1%{?git_date:.%{git_date}git%{git_commit_hash}}%{?dist}
Summary: Intel SGX kernel module
License: GPLv2

URL: https://github.com/intel/linux-sgx-driver
Source0: https://github.com/intel/linux-sgx-driver/archive/%{git_tag}.tar.gz

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
* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.11-1
- Add support for packaging pre-releases (i.e. arbitrary git commits)

* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.11-1
- Update to upstream release 2.11.

* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.6-2
- Refactor and modernize the SPEC file.

* Thu Oct 17 2019 Yawning Angel <yawning@schwanenlied.me> - 2.6-1
- Update to upstream release 2.6.

* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
