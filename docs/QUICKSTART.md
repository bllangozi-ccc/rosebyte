# Using Rosebyte

Start at https://jacknrose.co.uk/rosebyte. Register with a passkey, or use the
public agent API guide with your own persistent Ed25519 identity. Submitted
programs can be compiled or inspected; public arbitrary guest execution is disabled.
Use https://jacknrose.co.uk/ai-chat for questions.

The public repository contains language specifications, examples, an API client
and encrypted core releases. The implementation is private. An encrypted release
is not a source-access grant; approved reviewers need scoped owner access.

On94, your owner session can use the native toolchain:

```sh
rosebyte-native bootstrap
rosebyte-native compile example.rbl.json example.rblb
rosebyte-native run example.rblb inputs.json
```

See [native operation](NATIVE.md), [RBL1](STRUCTURED.md),
[public dictionary](DICTIONARY.md) and [implementation boundaries](IMPLEMENTATION.md).
Local build commands in the native guide apply to an authorised decrypted core
checkout, not to this public distribution checkout.
