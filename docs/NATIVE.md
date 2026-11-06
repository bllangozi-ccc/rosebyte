> Core implementation and its complete test harness are private. The encrypted release contains the owner/reviewer build; public readers can use the hosted translator and this specification.

# Python-independent RoseByte execution on Root94

RoseByte already runs on94. The new `rosebyte-native` is an experimental native Linux
compiler/runner: it executes RBL1 bytecode and the actual RB-written compiler
without Python, OpenAI, a model process or a network API. The compiler emits the
same bytecode as the independent reference implementation and self-compiles
through identical second/third stages.

This is its own language toolchain, with a **C runtime** and RB-written compiler.
It is not a claim that the C runtime, operating system, TLS or passkey libraries
are written in RoseByte. Maintained libc, json-c and OpenSSL libraries remain runtime
dependencies; their versions/security updates matter. No encryption algorithms
were reimplemented. Current tested platform: Ubuntu24.04, Linux x86-64. Source
porting to other operating systems/architectures remains to be qualified.

## Use on94

From your owner PuTTY session:

```sh
rosebyte-native --version
rosebyte-native bootstrap
rosebyte-native compile example.rbl.json example.rblb
rosebyte-native run example.rblb inputs.json
```

`inputs.json` is a JSON array of entry-function arguments, e.g. `[]` for no
arguments or `[[1,2,3]]` for one list argument. Compilation refuses an existing
output path. Inputs must be bounded regular files: symlinks/FIFOs are refused.

Run the bundled application from its installed share directory, choosing a new
output name each time:

```sh
cd /opt/rosebyte-native/releases/0.10.0a1/share
rosebyte-native compile examples/release-check.rbl.json /tmp/my-release-check.rblb
rosebyte-native run /tmp/my-release-check.rblb examples/release-inputs.json
# {"result":["ready",3]}
```

## Incoming scans without a Python adapter

The native incoming gate is a separate C process, managed by `rb-native-gate`.
It uses the existing private `/incoming` receipts area and ClamAV daemon. The
runtime's default local socket is `/run/rb-native-gate/gate.sock`. Every submitted
source, compiled output and execution input is scanned before use/release.
Receipts bind exact sizes and SHA-256 hashes; scanner failure/stale signatures
fail closed. This adds no public filesystem/SSH capability.

The scanner service has a dedicated namespace, no capabilities, no external
network access, bounded memory and finite socket/request timeouts. Only root
and the configured portal peer UID are admitted. Existing Root94 incoming
ownership uses the `rose-console` system user; this adapter does not start Rose,
load her profile or offer her tools. Hash-only scan logs rotate at2MiB, retaining
one previous segment; these are local scan receipts, not a permanent abuse ledger.

The native gate needs a maintained ClamAV installation and current signatures;
that security dependency is deliberate. No online AI account is required. The
existing web authentication/issuer/translation service remains separate and
continues using its qualified Python implementation. Native public guest
execution has **not** been enabled. Independent Architect review is pending.

## Build and independent tests

```sh
# Ubuntu build prerequisites, on a machine you administer:
sudo apt-get install build-essential libjson-c-dev libssl-dev
make -C native
./native/rb-native --version
python3 -m unittest discover -s tests -v
```

The test harness builds separate testing/sanitizer binaries. Those have an
explicit compile-time test scanner fixture; the installed release executable
has no test scanner bypass. Tests check that separation. On a clean reviewer
machine, the test binaries exercise the pure VM without a running scanner;
production commands require the configured incoming gate. The reference unit
in `native/rb-native-gate.service` requires local role/directory/ClamAV provisioning
and site-specific filesystem isolation before use. Do not blindly install it on
a machine with different identities or paths.

The VM has no guest filesystem, network, imports, shell, reflection or arbitrary
host-function lookup. It enforces the RBL1 fuel/type/buffer limits, a128MiB
allocation budget,256MiB process address-space cap,5CPU-second and15wall-second
process guards. Platform process limits can reject workloads before language
fuel is exhausted. Native/reference object keys reject NUL to avoid differing
JSON-library key truncation behaviour. Float values are outside RBL1.

These are research qualification results, not a security certification. A C VM
adds memory-safety risks; AddressSanitizer/UndefinedBehaviorSanitizer and malformed
bytecode tests reduce uncertainty but do not establish absence of vulnerabilities.
See [Architect's review checklist](ARCHITECT-REVIEW.md).
