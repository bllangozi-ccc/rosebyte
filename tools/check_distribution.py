"""Public distribution integrity only; not execution of the encrypted core."""
import base64,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'releases/manifest-0.10.0a1.json').read_bytes())
p=root/'releases'/m['encrypted_artifact'];raw=p.read_bytes();packet=json.loads(raw)
assert len(raw)==m['ciphertext_bytes'] and hashlib.sha256(raw).hexdigest()==m['ciphertext_sha256']
assert packet['header']['recipient']==m['recipient_fingerprint'] and packet['header']['format']=='RB-SEALED-RELEASE-1'
assert len(base64.b64decode(packet['ciphertext'],validate=True))>16
assert not any((root/n).exists() for n in ['rosebyte','native','kernel','private-recipient.json','.env'])
d=json.loads((root/'spec/dictionary-manifest.json').read_bytes())
for name,expected in d['sha256'].items():
 assert hashlib.sha256((root/'spec'/name).read_bytes()).hexdigest()==expected
results=json.loads((root/'benchmarks/results-20261106.json').read_bytes())
assert results['summary']['all_lossless'] and len(results['fixtures'])==12
for f in results['fixtures']:
 data=(root/'benchmarks/fixtures'/(f['name']+'.bin')).read_bytes()
 assert hashlib.sha256(data).hexdigest()==f['sha256'] and len(data)==f['source_bytes']
 assert len(f['results'])==10 and all(r['lossless_verified'] for r in f['results'])
print('Public encrypted distribution and benchmark fixture integrity passed; core execution and owner decryption are separate checks.')
