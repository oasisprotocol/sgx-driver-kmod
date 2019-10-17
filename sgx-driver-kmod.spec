# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod
%global debug_package %{nil}

%define repo rpmfusion

Name:           sgx-driver-kmod
Version:        2.6
Release:        1%{?dist}.1
Summary:        Intel SGX kernel module
Group:          System Environment/Kernel
License:        GPLv2
URL:            https://github.com/intel/linux-sgx-driver
%undefine _disable_source_fetch
Source0:        https://github.com/intel/linux-sgx-driver/archive/4f5bb63a99b785f03bb6a03dc5402e99691b849b.tar.gz
%define         SHA256SUM0 713e4fea8991fb3391b3c8d718776f6c3d2fe2821e9c358ac2448e1083fe5c53
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{_bindir}/kmodtool
Packager:       Yawning Angel <yawning@schwanenlied.me>

ExclusiveArch: i686 x86_64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
Intel(R) Software Guard Extensions (Intel(R) SGX) is an Intel technology for
application developers seeking to protect select code and data from disclosure
or modification.

The linux-sgx-driver project hosts the out-of-tree driver for the Linux
Intel(R) SGX software stack, which will be used until the driver upstreaming
process is complete.


%prep
echo "%SHA256SUM0 %SOURCE0" | sha256sum -c -
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pwd

for kernel_version in %{?kernel_versions} ; do
    # Fucking Intel bumped the version but didn't tag.
    # cp -a linux-sgx-driver-sgx_driver_%{version} _kmod_build_${kernel_version%%___*}
    cp -a linux-sgx-driver-4f5bb63a99b785f03bb6a03dc5402e99691b849b _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/isgx.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/isgx.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Oct 17 2019 Yawning Angel <yawning@schwanenlied.me> - 2.6-1
- Update to upstream release 2.6.
* Fri Jun 21 2019 Yawning Angel <yawning@schwanenlied.me> - 2.5-3
- Cherry pick bug fixes from upstream.
* Sun Jun 02 2019 Yawning Angel <yawning@schwanenlied.me> - 2.5-2
- Cherry pick changes to fix the build on kernel 5.1.x.
* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
