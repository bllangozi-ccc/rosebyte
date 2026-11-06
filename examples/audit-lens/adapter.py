"""Npm audit-v2 input adapter; policy and rendering live in audit-lens.rblb.

No network, npm invocation or remediation. Unused advisory fields are omitted.
"""
import json
MAX_BYTES=65536

def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate JSON field')
        result[key]=value
    return result

def reject_constant(value):raise ValueError('Non-finite JSON number')

def normalize(raw):
    if not isinstance(raw,bytes) or not 1<=len(raw)<=MAX_BYTES:raise ValueError('Use 1..65536 UTF-8 bytes')
    try:report=json.loads(raw.decode('utf-8'),object_pairs_hook=unique,parse_constant=reject_constant)
    except (UnicodeError,RecursionError,json.JSONDecodeError) as error:raise ValueError('Invalid UTF-8 JSON report') from error
    if not isinstance(report,dict) or type(report.get('auditReportVersion')) is not int or report['auditReportVersion']!=2 or 'error' in report:
        raise ValueError('Expected a successful npm auditReportVersion 2 report')
    records=report.get('vulnerabilities')
    if not isinstance(records,dict) or len(records)>256:raise ValueError('Expected at most 256 vulnerable-package records')
    entries=[]
    for name,item in records.items():
        if not isinstance(item,dict) or item.get('name')!=name:raise ValueError('Package name mismatch')
        if not all(key in item for key in ('severity','isDirect','fixAvailable')):raise ValueError('Required triage field missing')
        fix=item['fixAvailable']
        # Project only the fix flag used by the RB policy. No package paths,
        # advisory prose, URLs, versions or unused CVSS floats enter the VM.
        if isinstance(fix,dict):fix={'isSemVerMajor':fix.get('isSemVerMajor')}
        entries.append([name,item['severity'],item['isDirect'],fix])
    return entries
