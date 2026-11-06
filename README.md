# RoseByte

Experimental bounded language and hosted translation service. **0.10.0a1 research preview; independent security review pending.**

- [Try the hosted translator](https://jacknrose.co.uk/rosebyte)
- [Public guide](https://jacknrose.co.uk/guide)
- [Reliable agent inbox and polling](docs/AGENT-INBOX.md)
- [Questions and helpful-agent community](https://jacknrose.co.uk/ai-chat)
- [Measured compression facts, including losses](docs/BENCHMARKS.md)
- [Language dictionary in JSON and RoseByte](docs/DICTIONARY.md)
- [Language and implementation boundaries](docs/IMPLEMENTATION.md)
- [Native engine and actual RoseByte compiler bootstrap](docs/NATIVE.md)
- [Hosted access and abuse policy](docs/ACCESS-POLICY.md)
- [Encrypted core release](docs/RELEASES.md)

The RBL1 compiler emitter is written in RoseByte and self-compiles through three identical stages. Its native C VM runs without Python or an AI provider. Website identities, cryptography and the legacy compatibility engine still use maintained host components. The public web service does not execute arbitrary submitted programs.

This fresh public repository distributes documentation, public specifications/examples, a generic client SDK and encrypted core artifacts. Plaintext core implementation and its full test harness are private; a public clone cannot build them. Authorised reviewers need the owner-decrypted release. Previous public copies cannot be retracted. See [rights](COPYRIGHT.md).

Our aim is to remove hosted access from users or agents whose abuse is detected and evidenced. Scanning is one safeguard, not proof of good intentions; revocation cannot revoke already downloaded plaintext. Reported allegations are investigated. The existing host ban list is preserved.

Measured results currently show narrow structural wins and substantial losses against stronger compression settings. We do not claim general superiority, guaranteed malware detection or 3000% improvement.
