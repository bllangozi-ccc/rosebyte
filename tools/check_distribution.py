"""Public distribution integrity only; not execution of the encrypted core."""
import base64,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
allowed_roots={'README.md','SECURITY.md','COPYRIGHT.md','AGENTS.md'}
allowed_dirs={'docs','examples','spec','benchmarks','sdk','tools','releases','.github'}
for item in root.rglob('*'):
 rel=item.relative_to(root)
 if rel.parts[0]=='.git' or '__pycache__' in rel.parts:continue
 assert not item.is_symlink(),str(rel)
 if not item.is_file():continue
 assert (len(rel.parts)==1 and item.name in allowed_roots) or (len(rel.parts)>1 and rel.parts[0] in allowed_dirs),str(rel)
 assert item.name not in {'private-recipient.json','service-keys.json','hosts.yml','.env'},str(rel)
 assert item.suffix not in {'.c','.h','.so','.key','.pem','.db','.sqlite','.sqlite3'},str(rel)
 if rel.parts[0]=='sdk':assert str(rel)=='sdk/agent_client.py'
 if rel.parts[0]=='tools':assert str(rel)=='tools/check_distribution.py'
 if rel.parts[0]=='releases':assert item.name in {'rosebyte-core-0.10.0a1.rbenc','manifest-0.10.0a1.json','rosebyte-inbox-update-20261106.rbenc','manifest-inbox-20261106.json','rosebyte-inbox-update-20261106-r2.rbenc','manifest-inbox-20261106-r2.json','rosebyte-private-transfer-20261106.rbenc','manifest-private-transfer-20261106.json','rosebyte-reference-fix-0.10.1a1.rbenc','manifest-reference-0.10.1a1.json','rosebyte-native-fix-0.10.2a1.rbenc','manifest-native-0.10.2a1.json','SHA256SUMS'}
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

patch=json.loads((root/'releases/manifest-inbox-20261106.json').read_bytes())
blob=(root/'releases'/patch['encrypted_artifact']).read_bytes()
assert len(blob)==patch['ciphertext_bytes'] and hashlib.sha256(blob).hexdigest()==patch['ciphertext_sha256']
assert json.loads(blob)['header']['recipient']==m['recipient_fingerprint']==patch['recipient_fingerprint']

revision=json.loads((root/'releases/manifest-inbox-20261106-r2.json').read_bytes())
blob=(root/'releases'/revision['encrypted_artifact']).read_bytes()
assert len(blob)==revision['ciphertext_bytes'] and hashlib.sha256(blob).hexdigest()==revision['ciphertext_sha256']
assert json.loads(blob)['header']['recipient']==revision['recipient_fingerprint']==m['recipient_fingerprint']
transfer=json.loads((root/'releases/manifest-private-transfer-20261106.json').read_bytes())
blob=(root/'releases'/transfer['encrypted_artifact']).read_bytes()
assert len(blob)==transfer['ciphertext_bytes'] and hashlib.sha256(blob).hexdigest()==transfer['ciphertext_sha256']
assert json.loads(blob)['header']['recipient']==transfer['recipient_fingerprint']==m['recipient_fingerprint']
reference=json.loads((root/'releases/manifest-reference-0.10.1a1.json').read_bytes())
blob=(root/'releases'/reference['encrypted_artifact']).read_bytes()
assert len(blob)==reference['ciphertext_bytes'] and hashlib.sha256(blob).hexdigest()==reference['ciphertext_sha256']
assert json.loads(blob)['header']['recipient']==reference['recipient_fingerprint']==m['recipient_fingerprint']
native=json.loads((root/'releases/manifest-native-0.10.2a1.json').read_bytes())
blob=(root/'releases'/native['encrypted_artifact']).read_bytes()
assert len(blob)==native['ciphertext_bytes'] and hashlib.sha256(blob).hexdigest()==native['ciphertext_sha256']
assert json.loads(blob)['header']['recipient']==native['recipient_fingerprint']==m['recipient_fingerprint']
print('Public encrypted distribution and benchmark fixture integrity passed; core execution and owner decryption are separate checks.')
