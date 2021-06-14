# Kernel-module package for the legacy out-of-tree Intel SGX driver.
#
# Packaging based on Kmods2 from RPM Fusion:
# https://rpmfusion.org/Packaging/KernelModules/Kmods2.

# Uncomment one of the next lines to build for the newest, or all current
# kernels, or to build kmod on the machine itself (during boot).
#global buildforkernels newest
#global buildforkernels current
%global buildforkernels akmod
%global debug_package %{nil}

# Uncomment the following to use a pre-release.
#global git_date 20210420
#global git_commit 2d2b795890c01069aab21d4cdfd1226f7f65b971
%{?git_commit:%global git_commit_hash %(c=%{git_commit}; echo ${c:0:7})}

%if 0%{?git_date}
%global git_tag %{git_commit_hash}
%else
%global git_tag sgx_driver_%{version}
%endif

# SHA256sum of Source0.
%global SHA256SUM0 806778a1d5fe408dc520330c7eae185e0b67f313c32f594816f16063ac49d5b6

Name: sgx-driver-kmod
Version: 2.11
Release: 1%{?git_date:.%{git_date}git%{git_commit_hash}}%{?dist}
Summary: Intel SGX kernel module
License: GPLv2

URL: https://github.com/intel/linux-sgx-driver
Source0: https://github.com/intel/linux-sgx-driver/archive/%{git_tag}.tar.gz

ExclusiveArch: i686 x86_64

BuildRequires: %{_bindir}/kmodtool
%{!?kernels:BuildRequires: gcc, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
Intel(R) Software Guard Extensions (Intel(R) SGX) is an Intel technology for
application developers seeking to protect select code and data from disclosure
or modification.

The linux-sgx-driver project hosts the out-of-tree driver for the Linux
Intel(R) SGX software stack, which will be used until the driver upstreaming
process is complete.

This package contains the kmod module for Intel SGX.


%prep
# Ensure downloaded source matches SHA256 checksum.
echo "%SHA256SUM0 %SOURCE0" | sha256sum -c -

# Error out if there was something wrong with kmodtool.
%{?kmodtool_check}

# Print kmodtool output for debugging purposes.
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c -T -a 0
for kernel_version in %{?kernel_versions} ; do
    cp -a linux-sgx-driver-%{git_commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} KDIR="${kernel_version##*___}" -C "${kernel_version##*___}" M="${PWD}/_kmod_build_${kernel_version%%___*}" modules
done


%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/isgx.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/isgx.ko
done
%{?akmod_install}


%changelog
* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.11-1
- Add support for packaging pre-releases (i.e. arbitrary git commits)

* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.11-1
- Update to upstream release 2.11.

* Mon Jun 14 2021 Tadej Janež <tadej.j@nez.si> - 2.6-3
- Refactor and modernize the SPEC file.

* Fri Jun 12 2020 Yawning Angel <yawning@schwanenlied.me> - 2.6-2
- Use the real upstream 2.6 release.
- Cherry pick changes to fix the build on kernel 5.6.x.

* Thu Oct 17 2019 Yawning Angel <yawning@schwanenlied.me> - 2.6-1
- Update to upstream release 2.6.

* Fri Jun 21 2019 Yawning Angel <yawning@schwanenlied.me> - 2.5-3
- Cherry pick bug fixes from upstream.

* Sun Jun 02 2019 Yawning Angel <yawning@schwanenlied.me> - 2.5-2
- Cherry pick changes to fix the build on kernel 5.1.x.

* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
