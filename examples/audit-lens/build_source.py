"""Author the application AST. No compiler/runtime implementation is included."""
import json
from pathlib import Path
v=lambda n:{'var':n}
op=lambda n,*a:{'op':n,'args':list(a)}
call=lambda n,*a:{'call':n,'args':list(a)}
let=lambda n,e:{'let':n,'value':e}
set_=lambda n,e:{'set':n,'value':e}
ret=lambda e:{'return':e}
iff=lambda c,t,e=[]:{'if':c,'then':t,'else':e}
loop=lambda n,items,body:{'for':n,'in':items,'body':body}
fail=lambda:ret(op('fail','Invalid audit report'))
require=lambda c:iff(op('not',c),[fail()])
fn=lambda n,p,b:{'name':n,'params':p,'body':b}
cat=lambda *xs:__import__('functools').reduce(lambda a,b:op('concat',a,b),xs)
functions=[fn('rank',['severity'],[
 *[iff(op('eq',v('severity'),s),[ret(i)]) for i,s in enumerate(['info','low','moderate','high','critical'])],fail()]),
 fn('fix',['value'],[
 iff(op('eq',op('kind',v('value')),'bool'),[iff(v('value'),[ret('update-review')],[ret('manual-review')])]),
 require(op('eq',op('kind',v('value')),'object')),
 require(op('eq',op('kind',op('get',v('value'),'isSemVerMajor')),'bool')),
 iff(op('get',v('value'),'isSemVerMajor'),[ret('breaking-change-review')],[ret('update-review')])]),
 fn('main',['entries','format'],[
 require(op('eq',op('kind',v('entries')),'list')),
 require(op('le',op('len',v('entries')),256)),
 require(op('or',op('eq',v('format'),'summary'),op('eq',v('format'),'html'))),
 let('rows',[]),let('counts',[]),let('seen',[]),let('fix_label',''),let('direct_label',''),let('n',0),let('rank_value',0),let('row',[]),let('name',''),let('severity',''),let('direct',False),
 loop('entry',v('entries'),[
 require(op('eq',op('kind',v('entry')),'list')),require(op('eq',op('len',v('entry')),4)),
 set_('name',op('at',v('entry'),0)),set_('severity',op('at',v('entry'),1)),set_('direct',op('at',v('entry'),2)),
 require(op('eq',op('kind',v('name')),'text')),require(op('lt',0,op('len',v('name')))),require(op('le',op('len',op('utf8',v('name'))),128)),
 require(op('eq',op('kind',v('direct')),'bool')),
 loop('old',v('seen'),[require(op('not',op('eq',v('old'),v('name'))))]),
 set_('seen',op('append',v('seen'),v('name'))),
 set_('rank_value',call('rank',v('severity'))),set_('fix_label',call('fix',op('at',v('entry'),3))),
 ]),
 # Sort by severity through a fixed five-pass bucket walk. No arbitrary comparator.
 loop('level',['critical','high','moderate','low','info'],[
 set_('n',0),
 loop('entry',v('entries'),[
 iff(op('eq',op('at',v('entry'),1),v('level')),[
 set_('n',op('add',v('n'),1)),
 set_('rows',op('append',v('rows'),[op('at',v('entry'),0),v('level'),op('at',v('entry'),2),call('fix',op('at',v('entry'),3))]))])]),
 set_('counts',op('append',v('counts'),v('n')))]),
 let('status','no-findings-reported'),iff(op('lt',0,op('len',v('rows'))),[set_('status','review-required')]),
 iff(op('eq',v('format'),'summary'),[ret([v('status'),v('counts'),v('rows')])]),
 let('html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; style-src &#39;none&#39;; base-uri &#39;none&#39;; form-action &#39;none&#39;"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RoseByte Audit Lens</title></head><body><h1>RoseByte Audit Lens</h1><p>Saved report triage only. Not a fresh vulnerability check or a safety certificate.</p><table><thead><tr><th>Package</th><th>Severity</th><th>Scope</th><th>Next step</th></tr></thead><tbody>'),
 loop('item',v('rows'),[
 set_('direct_label','transitive'),iff(op('at',v('item'),2),[set_('direct_label','direct')]),
 set_('html',cat(v('html'),'<tr><td>',op('html_escape',op('at',v('item'),0)),'</td><td>',op('at',v('item'),1),'</td><td>',v('direct_label'),'</td><td>',op('at',v('item'),3),'</td></tr>'))]),
 ret(cat(v('html'),'</tbody></table><p>Review changes and rerun tests; no changes were applied.</p><nav><a href="https://jacknrose.co.uk/ai-chat">Community chat</a> · <a href="https://jacknrose.co.uk/guide/audit-lens">Guide</a> · <a href="https://github.com/bllangozi-ccc/rosebyte/tree/main/examples/audit-lens">Source</a></nav></body></html>'))])]
program={'version':'RBL1','entry':'main','functions':functions}
if __name__=='__main__':
 Path(__file__).with_name('audit-lens.rbl.json').write_text(json.dumps(program,ensure_ascii=False,separators=(',',':'))+'\n')
