import json,hashlib,time,statistics,zlib,gzip,bz2,lzma,sys,platform,os
from pathlib import Path
import brotli,zstandard as zstd,cbor2
CORE=Path(os.environ['ROSEBYTE_CORE_SOURCE']);sys.path.insert(0,str(CORE))
from rosebyte import shorthand,structured
ROOT=CORE;OUT=Path(__file__).resolve().parent;DIST=OUT.parents[1]
CODECS={'raw':(lambda b:b,lambda b:b),'zlib9':(lambda b:zlib.compress(b,9),zlib.decompress),'gzip9':(lambda b:gzip.compress(b,compresslevel=9,mtime=0),gzip.decompress),'bz2-9':(lambda b:bz2.compress(b,compresslevel=9),bz2.decompress),'lzma6':(lambda b:lzma.compress(b,preset=6),lzma.decompress),'brotli11':(lambda b:brotli.compress(b,quality=11),brotli.decompress),'zstd19':(lambda b:zstd.ZstdCompressor(level=19).compress(b),lambda b:zstd.ZstdDecompressor().decompress(b))}
def dumps(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()
def program(value):return {'version':'RBL1','entry':'main','functions':[{'name':'main','params':[],'body':[{'return':value}]}]}
cases=[('audit-lens',json.loads((DIST/'examples/audit-lens/audit-lens.rbl.json').read_bytes())),('release-check',json.loads((ROOT/'examples/release-check.rbl.json').read_bytes())),('dictionary',json.loads((ROOT/'spec/dictionary.rbl.json').read_bytes())),('compiler',json.loads((ROOT/'rosebyte/bootstrap/compiler.rbl.json').read_bytes()))]
for name,value in [('tiny-sum',{'op':'add','args':[1,1]}),('unicode','é成功🌹'+chr(0xad8e3)),('integers',list(range(256))),('squares',[i*i for i in range(256)]),('repeated-text',['same phrase repeated']*128),('irregular-ints',[((i*31337)%997)-498 for i in range(256)])]:cases.append((name,program(value)))
results=[];roundtrips=0
for name,ast in cases:
 text=shorthand.dumps(ast);normalized=shorthand.parse(text);code=structured.compile_rb(text)
 forms={'RoseByte-RBS1':text,'JSON-numeric-slots':dumps(normalized),'CBOR-numeric-slots':cbor2.dumps(normalized,canonical=True),'RBLB1-numeric-slots':code}
 if name=='audit-lens':forms['Python-equivalent']=(DIST/'examples/audit-lens/reference.py').read_bytes()
 sizes={};timings={}
 for representation,raw in forms.items():
  rows={}
  for codec,(encode,decode) in CODECS.items():
   t=time.perf_counter_ns();packed=encode(raw);elapsed=(time.perf_counter_ns()-t)/1e6
   assert decode(packed)==raw;roundtrips+=1;rows[codec]={'bytes':len(packed),'encode_ms_single_observation':round(elapsed,6)}
  sizes[representation]={'raw_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'best':min(rows,key=lambda k:rows[k]['bytes']),'best_bytes':min(v['bytes'] for v in rows.values()),'codecs':rows}
 # Representation-semantic equality, distinct from exact compressed-byte roundtrips.
 assert json.loads(forms['JSON-numeric-slots'])==cbor2.loads(forms['CBOR-numeric-slots'])==structured.decode(code)==normalized
 alternatives=[(k,v['best_bytes']) for k,v in sizes.items() if k!='RoseByte-RBS1'];best=min(n for _,n in alternatives);rb=sizes['RoseByte-RBS1']['best_bytes']
 results.append({'fixture':name,'representations':sizes,'RoseByte_beats_best_tested_alternative':rb<best,'RoseByte_vs_best_alternative_percent':round((1-rb/best)*100,2)})
dictionary=(DIST/'spec/shorthand-dictionary.json').read_bytes();dc=brotli.compress(dictionary,quality=11)
audit=results[0]['representations'];rbs=audit['RoseByte-RBS1']['best_bytes'];py=audit['Python-equivalent']['best_bytes']
result={'schema':'rosebyte-shorthand-benchmark-1','environment':{'python':platform.python_version(),'zlib':zlib.ZLIB_RUNTIME_VERSION,'brotli':brotli.__version__,'zstd':zstd.__version__,'cbor2':'6.2.0.post2'},'fixtures':results,'exact_compression_roundtrips':roundtrips,'summary':{'fixtures':len(results),'strict_wins_vs_best_other_representation':sum(r['RoseByte_beats_best_tested_alternative'] for r in results),'universal_winner':False},'dictionary_cold_cost':{'raw_bytes':len(dictionary),'brotli11_bytes':len(dc),'sha256':hashlib.sha256(dictionary).hexdigest(),'charge':'Additional dictionary transfer on a cold receiver, not hidden inside payload-only comparisons. Runtime/compiler installation costs are excluded for all languages.','audit_RBS1_plus_dictionary_bytes':rbs+len(dc),'audit_Python_payload_only_bytes':py,'amortization_repeated_audit_sized_distinct_programs':None if py<=rbs else len(dc)//(py-rbs)+1,'warning':'Repeated identical transfers may instead use caching; this is a size arithmetic illustration, not a traffic forecast.'},'delivery':'See delivery.json for actual existing authenticated hosted RBW1 packet sizes; no stripped safety checks or new unauthenticated transport.','scope':'Same alpha-normalized AST for JSON/CBOR/RBLB1/RBS1; original variable/function spellings and comments are not preserved. Python comparison only for the equivalent Audit Lens app. Exact decompression bytes verified separately; no vulnerability/security or universal compressor superiority claim.'}
(OUT/'measurements.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summary':result['summary'],'roundtrips':roundtrips,'audit':{k:v['best_bytes'] for k,v in audit.items()},'cold_dictionary':result['dictionary_cold_cost']},indent=2))
