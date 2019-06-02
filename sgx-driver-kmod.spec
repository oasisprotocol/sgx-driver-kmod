# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod
%global debug_package %{nil}

%define repo rpmfusion

Name:           sgx-driver-kmod
Version:        2.5
Release:        2%{?dist}.1
Summary:        Intel SGX kernel module
Group:          System Environment/Kernel
License:        GPLv2
URL:            https://github.com/intel/linux-sgx-driver
%undefine _disable_source_fetch
Source0:        https://github.com/intel/linux-sgx-driver/archive/sgx_driver_2.5.tar.gz
%define         SHA256SUM0 4f0ee81eb1e8c1bda30a9adce0b5fffae38c0b246b7859a396c6df9af653e0e3
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{_bindir}/kmodtool
Packager:       Yawning Angel <yawning@schwanenlied.me>
Patch1:         0001-sgx_vma-return-unsigned-int-from-sgx_vma_fault.patch
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
pushd linux-sgx-driver-sgx_driver_%{version}
%patch1 -p1
popd

for kernel_version in %{?kernel_versions} ; do
    cp -a linux-sgx-driver-sgx_driver_%{version} _kmod_build_${kernel_version%%___*}
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
* Sun Jun 02 2019 Yawning Angel <yawning@schwanenlied.me> - 2.5-2
- Cherry pick changes to fix the build on kernel 5.1.x.
* Tue May 14 2019 Yawning Angel <yanwing@schwanenlied.me> - 2.5-1
- Initial RPM release.
