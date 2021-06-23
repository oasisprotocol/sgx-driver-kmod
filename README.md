# Fedora Package for the Legacy Intel SGX Linux Driver

| Package         | Copr build status                                                              |
|:---------------:|:------------------------------------------------------------------------------:|
| sgx-driver-kmod | [![sgx-driver-kmod build status][sgx-driver-kmod-badge]][sgx-driver-kmod-link] |
| sgx-driver      | [![sgx-driver build status][sgx-driver-badge]][sgx-driver-link]                |

This repository provides [Fedora] kernel module packages for the legacy
(out-of-tree) [Intel SGX Linux Driver].

After many years of work, the Intel SGX support was [merged into the mainline
Linux kernel in version 5.11][upstream-5.11].
However, the ABI of the mainline SGX kernel support has diverged from the legacy
(out-of-tree) driver, so it will take applications some time to migrate. Hence,
the need for the legacy driver to be packaged.

The kernel module package follows the [Kmods2 standard].

## Installation

First, enable usage of [tadej/sgx-driver-kmod Copr repository][copr-repo]:

```
sudo dnf copr enable tadej/sgx-driver-kmod
```

Then install the driver with:

```
sudo dnf install sgx-driver
```

This will pull in 2 packages

- `sgx-driver`: userland package (documentation, license),
- `akmods-sgx-driver`: kernel module package that automatically builds the
  driver for the currently used kernel during system's boot.

## Validating Installation

To verify that the Intel SGX Linux driver has been properly installed and is
working, you can use the `sgx-detect` tool from the [sgxs-tools] Rust package.

There are no pre-built packages for it, so you will need to compile it yourself.

_NOTE: The sgxs-tools package must be compiled with a nightly version of the
Rust toolchain since they use the `#![feature]` macro._

### Install Dependencies

Make sure you have the following installed on your system:

- [GCC].
- [Protobuf] compiler.
- [pkg-config].
- [OpenSSL] development package.

You can install them by running:

```
sudo dnf install gcc protobuf-compiler pkg-config openssl-devel
```

### Install Rust Nightly

The current [recommended way to install Rust nightly on Fedora][
fedora-rust-nightly] is to use the [rustup] tool.

_NOTE: rustup cannot be installed alongside a distribution packaged Rust
version. You will need to remove it (if it's present) before you can start using
rustup._

Install it by running:

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

_NOTE: If you want to avoid directly executing a shell script fetched the
internet, you can also [download `rustup-init` executable for your platform][
rustup-init-download] and run it manually. This will run `rustup-init` which
will download and install the latest stable version of Rust on your system._

Install the nightly version of the Rust toolchain with:

```
rustup install nightly
```

### Build and Install sgxs-tools

```
cargo +nightly install sgxs-tools
```

### Run sgx-detect Tool

After the installation completes, run the `sgx-detect` tool to make sure
everything is set up correctly.

When the SGX driver is properly installed, you should see the green ✔ for the
`SGX kernel device (/dev/isgx)` line.

[sgx-driver-kmod-badge]:
  https://copr.fedorainfracloud.org/coprs/tadej/sgx-driver-kmod/package/sgx-driver-kmod/status_image/last_build.png
[sgx-driver-kmod-link]:
  https://copr.fedorainfracloud.org/coprs/tadej/sgx-driver-kmod/package/sgx-driver-kmod/
[sgx-driver-badge]:
  https://copr.fedorainfracloud.org/coprs/tadej/sgx-driver-kmod/package/sgx-driver/status_image/last_build.png
[sgx-driver-link]:
  https://copr.fedorainfracloud.org/coprs/tadej/sgx-driver-kmod/package/sgx-driver/
[Fedora]: https://getfedora.org/
[Intel SGX Linux Driver]: https://github.com/intel/linux-sgx-driver
[upstream-5.11]:
  https://www.phoronix.com/scan.php?page=news_item&px=Intel-SGX-Linux-5.11
[Kmods2 standard]: https://rpmfusion.org/Packaging/KernelModules/Kmods2
[copr-repo]: https://copr.fedorainfracloud.org/coprs/tadej/sgx-driver-kmod/
[sgxs-tools]: https://lib.rs/crates/sgxs-tools
[GCC]: http://gcc.gnu.org/
[Protobuf]: https://github.com/protocolbuffers/protobuf
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config
[OpenSSL]: https://www.openssl.org/
[fedora-rust-nightly]:
  https://github.com/developer-portal/content/blob/master/tech/languages/rust/further-reading.md#other-useful-links
[rustup]: https://rustup.rs/
[rustup-init-download]:
  https://rust-lang.github.io/rustup/installation/other.html
