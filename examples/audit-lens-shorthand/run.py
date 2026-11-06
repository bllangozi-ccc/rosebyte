#!/usr/bin/env python3
"""Explicit local CLI adapter for the qualified native RoseByte runtime."""
import argparse,json,subprocess,tempfile,sys,os,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'audit-lens'))
from adapter import normalize,MAX_BYTES
from scan import scan

def read_regular(path):
    import stat
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):raise ValueError('Regular report file required')
        with os.fdopen(fd,'rb',closefd=False) as stream:return stream.read(MAX_BYTES+1)
    finally:os.close(fd)

def main():
    parser=argparse.ArgumentParser(description='RoseByte Audit Lens: saved npm audit-v2 report triage; no network or fixes')
    parser.add_argument('report');parser.add_argument('--format',choices=('summary','html'),default='summary')
    parser.add_argument('--runtime',default='rosebyte-native',help='Qualified native runtime executable; never an input-derived command')
    args=parser.parse_args();raw=read_regular(args.report);scan(raw);entries=normalize(raw)
    code=Path(__file__).with_name('audit-lens.rblb');manifest=json.loads(Path(__file__).with_name('manifest.json').read_bytes())
    if hashlib.sha256(read_regular(code)).hexdigest()!=manifest['files']['audit-lens.rblb']:raise ValueError('Application hash mismatch')
    with tempfile.TemporaryDirectory(prefix='rosebyte-audit-lens-') as directory:
        inputs=Path(directory)/'inputs.json';inputs.write_text(json.dumps([entries,args.format],ensure_ascii=False,separators=(',',':')),encoding='utf-8');inputs.chmod(0o600)
        result=subprocess.run([args.runtime,'run',str(Path(__file__).with_name('audit-lens.rblb')),str(inputs)],capture_output=True,timeout=8,check=False)
    if result.returncode or len(result.stdout)>262144:raise ValueError('Runtime rejected report or exceeded limit')
    value=json.loads(result.stdout)['result']
    output=value if args.format=='html' else json.dumps(value,ensure_ascii=False,separators=(',',':'))
    scan(output.encode('utf-8'));print(output)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.TimeoutExpired,KeyError) as error:
        print('Audit Lens: '+str(error),file=sys.stderr);sys.exit(2)
