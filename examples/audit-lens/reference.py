"""Conventional Python implementation of the same triage and HTML behaviour.
Used for independent result comparisons, not invoked by the RoseByte app.
"""
import html
LEVELS=('critical','high','moderate','low','info')
PREFIX='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; style-src &#39;none&#39;; base-uri &#39;none&#39;; form-action &#39;none&#39;"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RoseByte Audit Lens</title></head><body><h1>RoseByte Audit Lens</h1><p>Saved report triage only. Not a fresh vulnerability check or a safety certificate.</p><table><thead><tr><th>Package</th><th>Severity</th><th>Scope</th><th>Next step</th></tr></thead><tbody>'
SUFFIX='</tbody></table><p>Review changes and rerun tests; no changes were applied.</p><nav><a href="https://jacknrose.co.uk/ai-chat">Community chat</a> · <a href="https://jacknrose.co.uk/guide/audit-lens">Guide</a> · <a href="https://github.com/bllangozi-ccc/rosebyte/tree/main/examples/audit-lens">Source</a></nav></body></html>'

def triage(entries,format='summary'):
    if type(entries) is not list or len(entries)>256 or format not in ('summary','html'):raise ValueError('Input')
    rows=[];seen=set()
    for entry in entries:
        if type(entry) is not list or len(entry)!=4:raise ValueError('Entry')
        name,severity,direct,fix=entry
        if type(name) is not str or not 1<=len(name.encode('utf-8'))<=128 or name in seen:raise ValueError('Name')
        seen.add(name)
        if severity not in LEVELS or type(direct) is not bool:raise ValueError('Severity or scope')
        if type(fix) is bool:action='update-review' if fix else 'manual-review'
        elif type(fix) is dict and type(fix.get('isSemVerMajor')) is bool:action='breaking-change-review' if fix['isSemVerMajor'] else 'update-review'
        else:raise ValueError('Fix')
        rows.append([name,severity,direct,action])
    rows.sort(key=lambda row:LEVELS.index(row[1]))
    counts=[sum(row[1]==level for row in rows) for level in LEVELS]
    if format=='summary':return ['review-required' if rows else 'no-findings-reported',counts,rows]
    return PREFIX+''.join('<tr><td>'+html.escape(name,quote=True)+'</td><td>'+severity+'</td><td>'+('direct' if direct else 'transitive')+'</td><td>'+action+'</td></tr>' for name,severity,direct,action in rows)+SUFFIX
