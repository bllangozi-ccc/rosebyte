"""Public adapter/reference tests; optional differential checks use authorised core.
ROSEBYTE_CORE_SOURCE points to a private review checkout, never downloaded here.
"""
import copy,html,json,os,random,subprocess,sys,tempfile,time,unittest
from pathlib import Path
from html.parser import HTMLParser
from adapter import normalize
from reference import triage
ROOT=Path(__file__).resolve().parent
CORE=os.environ.get('ROSEBYTE_CORE_SOURCE')
if CORE:
 sys.path.insert(0,CORE)
 from rosebyte import structured as vm
CODE=(ROOT/'audit-lens.rblb').read_bytes()

class ToolTests(unittest.TestCase):
 def test_sample_and_unused_cvss_float(self):
  value=triage(normalize((ROOT/'sample-audit.json').read_bytes()))
  self.assertEqual(value,['review-required',[0,1,0,1,0],[['demo-widget','high',True,'breaking-change-review'],['demo-helper','low',False,'manual-review']]])
 def test_reject_error_versions_duplicates_and_missing_fields(self):
  cases=[b'{}',b'{"auditReportVersion":2,"vulnerabilities":{},"error":{}}',b'{"auditReportVersion":true,"vulnerabilities":{}}',b'{"auditReportVersion":3,"vulnerabilities":{}}',b'{"auditReportVersion":2,"vulnerabilities":{},"vulnerabilities":{}}',b'{"auditReportVersion":2,"vulnerabilities":{"x":{"name":"other"}}}',b'{"auditReportVersion":2,"vulnerabilities":{"x":{"name":"x"}}}',b'\xff',b'{"auditReportVersion":2,"vulnerabilities":{},"metadata":NaN}',b'x'*65537]
  for raw in cases:
   with self.subTest(raw=raw[:100]),self.assertRaises(ValueError):normalize(raw)
 def test_no_findings_is_not_safe(self):
  self.assertEqual(triage(normalize(b'{"auditReportVersion":2,"vulnerabilities":{}}'))[0],'no-findings-reported')
 def test_html_has_no_executable_attacker_content(self):
  payload='<script>alert(1)</script><img src=x onerror=alert(2)>"&🌹'
  output=triage([[payload,'critical',True,False]],'html')
  self.assertIn(html.escape(payload,quote=True),output)
  if CORE:self.assertEqual(vm.execute(CODE,[[[payload,'critical',True,False]],'html']),output)
  class Inspect(HTMLParser):
   def handle_starttag(inner,tag,attrs):
    self.assertNotIn(tag,('script','img','iframe','object','embed','form'))
    self.assertFalse(any(k.startswith('on') for k,_ in attrs))
  Inspect().feed(output)
 @unittest.skipUnless(CORE,'Authorised core checkout required for VM differential tests')
 def test_rebuild_and_1000_generated_oracle_cases(self):
  self.assertEqual(vm.compile_rb((ROOT/'audit-lens.rbl.json').read_bytes()),CODE)
  rng=random.Random(71651)
  for i in range(1000):
   entries=[[f'p{j}-🌹-{i}',rng.choice(['critical','high','moderate','low','info']),rng.choice([True,False]),rng.choice([True,False,{'isSemVerMajor':True},{'isSemVerMajor':False}])] for j in range(rng.randrange(17))]
   for form in ('summary','html'):
    self.assertEqual(vm.execute(CODE,[entries,form]),triage(entries,form))
 @unittest.skipUnless(CORE,'Authorised core checkout required for VM negative/boundary tests')
 def test_vm_bad_inputs_and_maximum(self):
  bad=[None,{},[["x","unknown",True,False]],[["x","high",1,False]],[["x","high",True,1]],[["x","high",True,{}]],[["x","high",True,{'isSemVerMajor':1}]],[["","high",True,False]],[["x"*129,"high",True,False]],[["x","high",True,False]]*2,[["x","high",True,False]]*257]
  for value in bad:
   with self.subTest(value=str(value)[:120]),self.assertRaises(ValueError):vm.execute(CODE,[value,'summary'])
  rows=[[f'p{i}','high',True,False] for i in range(256)]
  self.assertEqual(vm.execute(CODE,[rows,'summary']),triage(rows))
  self.assertEqual(vm.execute(CODE,[rows,'html']),triage(rows,'html'))
 @unittest.skipUnless(CORE,'Authorised native test build required')
 def test_native_differential_and_sanitizer(self):
  rng=random.Random(712)
  with tempfile.TemporaryDirectory() as temp:
   inputs=Path(temp)/'inputs.json'
   for i in range(120):
    entries=[[f'package-{n}-é',rng.choice(['critical','high','moderate','low','info']),bool(n%2),bool(n%3)] for n in range(rng.randrange(20))]
    if i==1:entries=[['<script>not executed</script>\"&🌹','critical',True,False]]
    form='html' if i%2 else 'summary';inputs.write_text(json.dumps([entries,form]))
    for exe in ('rb-native-test',*(['rb-native-sanitize'] if i<24 else [])):
     run=subprocess.run([str(Path(CORE)/'native'/exe),'run',str(ROOT/'audit-lens.rblb'),str(inputs),'--gate-socket','TEST-ONLY-NO-SCAN'],capture_output=True,timeout=8)
     self.assertEqual(run.returncode,0,run.stderr.decode());self.assertEqual(json.loads(run.stdout)['result'],triage(entries,form));self.assertNotIn(b'runtime error:',run.stderr);self.assertNotIn(b'AddressSanitizer',run.stderr)

if __name__=='__main__':unittest.main()
