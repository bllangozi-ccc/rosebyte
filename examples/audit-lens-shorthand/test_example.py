import json,os,random,subprocess,sys,tempfile,unittest,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ORIGINAL=HERE.parent/'audit-lens';sys.path.insert(0,str(ORIGINAL))
from adapter import normalize
from reference import triage
CORE=os.environ.get('ROSEBYTE_CORE_SOURCE')
if CORE:
 sys.path.insert(0,CORE);from rosebyte import structured as vm,shorthand
class ShorthandExampleTests(unittest.TestCase):
 def test_published_manifest(self):
  m=json.loads((HERE/'manifest.json').read_bytes())
  for n,h in m['files'].items():self.assertEqual(hashlib.sha256((HERE/n).read_bytes()).hexdigest(),h)
 @unittest.skipUnless(CORE,'Authorised core checkout required; public CI does not execute encrypted core')
 def test_1000_oracle_cases_and_original_preserved_semantics(self):
  code=(HERE/'audit-lens.rblb').read_bytes();old=(ORIGINAL/'audit-lens.rblb').read_bytes()
  self.assertEqual(vm.compile_rb((HERE/'audit-lens.rbs').read_bytes()),code)
  rng=random.Random(112251)
  for i in range(1000):
   entries=[[f'package-{n}-🌹',rng.choice(['critical','high','moderate','low','info']),bool(n%2),rng.choice([True,False,{'isSemVerMajor':True},{'isSemVerMajor':False}])] for n in range(rng.randrange(17))]
   for mode in ('summary','html'):
    result=vm.execute(code,[entries,mode]);self.assertEqual(result,triage(entries,mode));self.assertEqual(result,vm.execute(old,[entries,mode]))
 @unittest.skipUnless(CORE,'Authorised native build required')
 def test_native_shorthand_and_hostile_html(self):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory);run=subprocess.run([str(Path(CORE)/'native/rb-native-test'),'compile',str(HERE/'audit-lens.rbs'),str(p/'code'),'--gate-socket','TEST-ONLY-NO-SCAN'],capture_output=True,timeout=8)
   self.assertEqual(run.returncode,0,run.stderr);self.assertEqual((p/'code').read_bytes(),(HERE/'audit-lens.rblb').read_bytes())
   entries=[['<img src=x onerror="alert(1)">','critical',True,False]];(p/'inputs').write_text(json.dumps([entries,'html']))
   run=subprocess.run([str(Path(CORE)/'native/rb-native-sanitize'),'run',str(p/'code'),str(p/'inputs'),'--gate-socket','TEST-ONLY-NO-SCAN'],capture_output=True,timeout=8)
   self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(json.loads(run.stdout)['result'],triage(entries,'html'))
if __name__=='__main__':unittest.main()
