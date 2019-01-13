# KeyRingo
A tiny macOS utility to ((securely)) prove account ownership in Ethereum without running a node

## Usage
`http://localhost:[PORT]/sign?[CHALLENGE]` - default port being `8001`

Name | Type | Description
--- | --- | ---
success | `boolean` | Matching query arguments
res | `string` | Signed challenge 
pub | `string` | Public key

## Verify
**Python 3**
```python
from ecdsa import VerifyingKey, SECP256k1
import binascii
...
key = VerifyingKey.from_string(binascii.unhexlify(pub), curve=SECP256k1)
vk.verify(binascii.unhexlify(res), '[CHALLENGE]'.encode())
```

## TODO
* Cross-platform
* Multiple accounts
* Security audit
