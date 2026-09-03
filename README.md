<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# Package branch — CentOS 10 Stream (`c10s`)

**This is the branch you work on.** It holds the `minkipc.spec` RPM's spec file and
`sources` pointer, plus the CI workflows that build and publish them.

## minkipc RPM package

This RPM packages [`qualcomm/minkipc`](https://github.com/qualcomm/minkipc)
—  MinkIPC is Qualcomm’s lightweight capability-based inter-process communication (IPC) framework.
It enables secure, synchronous message passing across different security domains—like Linux
user space to Trusted Execution Environment—using unforgeable object references and transport
mechanisms such as SMC, sockets, or TEE IOCTLs.

## Package contents

| File | Purpose |
|---|---|
| [`minkipc.spec`](minkipc.spec) | RPM spec for `minkipc.spec`. Builds via autotools (`cmake` + `%cmake_build`), installs the `libminkadaptor`, `libminkteec` shared library + `qteesupplicant`, `sfsconfig` daemons with udev rules + `rpmb_client` cli tool + `smcinvoke_client` and `gp_test_client` test binaries generated inline in `%install`. |
| [`sources`](sources) | dist-git checksum pointer for the upstream `v1.2.9` release tarball (SHA512). The tarball itself is never committed — see [`docs/workflows.md`](docs/workflows.md) for the lookaside-cache model. |
| [`.github/workflows/`](.github/workflows) | build-on-pr.yml, pkg-release.yml CI workflow files. |

## Getting started

### Update the version

Two edits, every time:

1. Bump `Version:` in [`minkipc.spec`](minkipc.spec) (and the
   `Source0:` URL if the upstream release layout changed).
2. Recompute the checksum:
   ```bash
   sha512sum --tag minkipc-<newversion>.tar.gz > sources
   ```

Commit both, open a PR against this branch, merge, then run **Release**. The
first release fetches the new upstream tarball, verifies it, and caches it back
automatically.

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
