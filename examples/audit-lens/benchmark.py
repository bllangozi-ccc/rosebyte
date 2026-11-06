"""Reproducible synthetic size and separately labelled timing measurements."""
import hashlib,json,os,statistics,subprocess,sys,tempfile,time,zlib
from pathlib import Path
from adapter import normalize
from reference import triage
ROOT=Path(__file__).resolve().parent

def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()
def fixture(n):
 records={}
 for i in range(n):
  name=f'example-package-{i}'
  records[name]={'name':name,'severity':['critical','high','moderate','low','info'][i%5],'isDirect':bool(i%2),'fixAvailable':{'name':name,'version':'2.0.0','isSemVerMajor':bool(i%3)},'via':[{'title':'Synthetic fixture only, not a real advisory. '+'Details omitted from triage. '*10,'url':'https://example.invalid/synthetic-advisory','cvss':{'score':7.5}}],'effects':[],'range':'<2.0.0','nodes':[f'node_modules/{name}','FAKE_PRIVATE_MARKER/project/node_modules/'+name]}
 return compact({'auditReportVersion':2,'vulnerabilities':records,'metadata':{'dependencies':{'prod':n,'total':n}}})

def main():
 rows=[]
 for name,data in [('sample',(ROOT/'sample-audit.json').read_bytes()),('synthetic-24',fixture(24))]:
  normalized=normalize(data);result=compact(triage(normalized));page=triage(normalized,'html').encode()
  assert b'FAKE_PRIVATE_MARKER' not in result+page
  rows.append({'fixture':name,'synthetic':True,'input_bytes':len(data),'summary_bytes':len(result),'html_bytes':len(page),'summary_reduction_percent':round((1-len(result)/len(data))*100,2),'input_zlib9_bytes':len(zlib.compress(data,9)),'summary_zlib9_bytes':len(zlib.compress(result,9)),'input_sha256':hashlib.sha256(data).hexdigest(),'summary_sha256':hashlib.sha256(result).hexdigest(),'meaning':'Lossy field projection, not lossless compression; Python reference returns identical output.'})
  if name=='synthetic-24':(ROOT/'synthetic-24.json').write_bytes(data+b'\n')
 source=(ROOT/'audit-lens.rbl.json').read_bytes();code=(ROOT/'audit-lens.rblb').read_bytes();baseline=(ROOT/'reference.py').read_bytes()
 sizes={'rosebyte_source_bytes':len(source),'rosebyte_bytecode_bytes':len(code),'bytecode_reduction_from_own_source_percent':round((1-len(code)/len(source))*100,2),'reference_python_bytes':len(baseline),'rosebyte_bytecode_zlib9_bytes':len(zlib.compress(code,9)),'rosebyte_source_zlib9_bytes':len(zlib.compress(source,9)),'reference_python_zlib9_bytes':len(zlib.compress(baseline,9)),'scope':'Application artifacts only; excludes runtime, adapter, dependencies and scan gate. Python reference is smaller than RB bytecode in this example.'}
 timings={};entries=normalize(fixture(24))
 core=os.environ.get('ROSEBYTE_CORE_SOURCE')
 if core:
  sys.path.insert(0,core);from rosebyte import structured as vm
  for name,fn in [('python_reference_in_process',lambda:triage(entries)),('rosebyte_reference_vm_in_process',lambda:vm.execute(code,[entries,'summary']))]:
   samples=[]
   for i in range(101):
    start=time.perf_counter_ns();value=fn();elapsed=time.perf_counter_ns()-start;assert value==triage(entries)
    if i:samples.append(elapsed/1e6)
   timings[name]={'runs':len(samples),'median_ms':statistics.median(samples),'p95_ms':sorted(samples)[94],'scope':'Normalized 24-row summary only; no parsing, IPC, scanner or filesystem'}
 with tempfile.TemporaryDirectory() as d:
  path=Path(d)/'inputs.json';path.write_bytes(compact([entries,'summary']));samples=[]
  for _ in range(25):
   start=time.perf_counter_ns();run=subprocess.run(['rosebyte-native','run',str(ROOT/'audit-lens.rblb'),str(path)],capture_output=True,timeout=8,check=True);samples.append((time.perf_counter_ns()-start)/1e6);assert json.loads(run.stdout)['result']==triage(entries)
  timings['native_process_with_live_scan_gate']={'runs':25,'median_ms':statistics.median(samples),'p95_ms':sorted(samples)[23],'scope':'Whole process including program/input scanning and JSON serialization; not directly comparable with in-process measurements'}
 result={'schema':'rosebyte-audit-lens-measurements-1','fixtures':rows,'artifact_sizes':sizes,'timings':timings,'security':'No claim of superior vulnerability detection or universal safety. Fixed RB program has no shell/filesystem/network primitives; output escapes HTML and omits advisory prose/paths. Adapter/runtime remain trusted.'}
 (ROOT/'measurements.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
