"""Offline checks for brief, creative and generation-request JSON. No API calls."""
import argparse,json,math,re
from datetime import date
from pathlib import Path

# Credential shapes. An artifact is copied into prompts, peer messages and reports,
# so authentication material must never survive one, whatever the field is called.
SECRETS=[r'sk-[A-Za-z0-9]{20,}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'xox[baprs]-[A-Za-z0-9-]{10,}',r'AKIA[0-9A-Z]{16}',
         r'-----BEGIN [A-Z ]*PRIVATE KEY',r'(?i)\bbearer\s+[A-Za-z0-9._\-]{20,}',
         r'(?i)\b(api[_-]?key|secret|password|token)\b\s*[:=]\s*[^\s"\']{16,}']
# Meta truncation thresholds at capture [platform]; an artifact may declare its own.
LIMITS={'primary_text':125,'headline':40,'description':30}
COPY_FIELDS=['hook','primary_text','headline','description','cta']
EVIDENCE_TYPES=['user_stated','product_observed','customer_quote','measurement','public_observation','derived','hypothesis','unverified']

def walk(node,path='$'):
    if isinstance(node,dict):
        for key,value in node.items():yield from walk(value,path+'.'+str(key))
    elif isinstance(node,list):
        for i,value in enumerate(node):yield from walk(value,path+'['+str(i)+']')
    elif isinstance(node,str):yield path,node

def secret_scan(data):
    return ['Credential-shaped value at '+p+'; an artifact never carries authentication material' for p,v in walk(data) if any(re.search(x,v) for x in SECRETS)]

def check(data):
    errors=[];warnings=[]
    if not isinstance(data,dict):return ['Artifact must be an object'],[]
    errors+=secret_scan(data)
    def need(obj,key):
        if not isinstance(obj.get(key),str) or not obj[key].strip():errors.append('Missing nonempty '+key)
    if data.get('schema_v')!='1.0.0':errors.append('Unsupported schema_v')
    kind=data.get('kind')
    if kind=='brief':
        for k in ['offer','country','ad_language','objective']:need(data,k)
        try:
            start=date.fromisoformat(data['window']['start']);end=date.fromisoformat(data['window']['end'])
            if end<start:errors.append('Research end precedes start')
        except (KeyError,TypeError,ValueError):errors.append('Window requires valid ISO start/end dates')
    elif kind=='creative':
        for k in ['hook','ad_language','cta']:need(data,k)
        limits=data.get('limits') if isinstance(data.get('limits'),dict) else {}
        # A misspelled override would otherwise disable a limit without saying so.
        for key in sorted(limits):
            if key not in LIMITS:errors.append('Unknown declared limit '+str(key))
        for field,default in LIMITS.items():
            text=data.get(field)
            if text is None:continue
            if not isinstance(text,str):errors.append(field+' must be text');continue
            cap=limits.get(field,default)
            if isinstance(cap,bool) or not isinstance(cap,int) or cap<=0:errors.append('Invalid declared limit for '+field);continue
            if len(text)>cap:errors.append(f'{field} is {len(text)} characters, over the {cap}-character limit')
        banned=data.get('prohibited_terms',[])
        if not isinstance(banned,list):errors.append('prohibited_terms must be an array')
        else:
            rendered={k:v for k,v in data.items() if k in COPY_FIELDS and isinstance(v,str)}
            for term in banned:
                if not isinstance(term,str) or not term.strip():errors.append('Prohibited term must be nonempty text');continue
                for field,text in sorted(rendered.items()):
                    if re.search(r'(?<!\w)'+re.escape(term.strip())+r'(?!\w)',text,re.IGNORECASE):errors.append('Prohibited term "'+term.strip()+'" appears in '+field)
            if banned:warnings.append('The red line matches declared terms only; a paraphrase carrying the same forbidden meaning still passes and needs human review.')
        proof=data.get('evidence',[]);claims=data.get('claims',[])
        if not isinstance(proof,list) or not isinstance(claims,list):return errors+['evidence and claims must be arrays'],warnings
        ids={}
        for row in proof:
            if not isinstance(row,dict):errors.append('Evidence must be objects');continue
            eid=row.get('id')
            if not isinstance(eid,str) or not eid.strip():errors.append('Evidence id missing');continue
            if eid in ids:errors.append('Duplicate evidence id '+eid)
            ids[eid]=row
            if row.get('type') not in EVIDENCE_TYPES:errors.append('Unknown evidence type')
            if row.get('type')=='customer_quote':need(row,'verbatim')
        for claim in claims:
            if not isinstance(claim,dict):errors.append('Claims must be objects');continue
            need(claim,'text');refs=claim.get('proof_ids')
            if not isinstance(refs,list) or not refs:errors.append('Claim lacks proof_ids');continue
            for ref in refs:
                if not isinstance(ref,str) or ref not in ids:errors.append('Unknown proof reference');continue
                row=ids[ref]
                if row.get('type') in ['hypothesis','unverified']:errors.append('Claim rests on unverified evidence')
                need(row,'source');need(row,'supports')
            if claim.get('testimonial') and not any(isinstance(r,str) and ids.get(r,{}).get('type')=='customer_quote' and ids.get(r,{}).get('verbatim') for r in refs):errors.append('Testimonial lacks an actual quote record')
        warnings.append('Human/model review must assess whether each source actually supports the claim; this checker cannot do that.')
    elif kind=='generation_request':
        for k in ['provider','model','account_alias']:need(data,k)
        items=data.get('items')
        if not isinstance(items,list) or not items:errors.append('Nonempty items array required')
        approval=data.get('approval')
        if not isinstance(approval,dict):errors.append('New media requires a recorded approval object')
        else:
            for k in ['granted_at','provider','model','account_alias','ceiling']:need(approval,k)
            try:
                if date.fromisoformat(approval['granted_at'])>date.today():errors.append('Approval is dated in the future')
            except (KeyError,TypeError,ValueError):errors.append('Approval needs a valid ISO granted_at date')
            for k in ['provider','model','account_alias']:
                if data.get(k)!=approval.get(k):errors.append('Request '+k+' does not match the approval; a change there needs a new decision')
            cap=approval.get('max_items')
            if isinstance(cap,bool) or not isinstance(cap,int) or cap<=0:errors.append('Approval needs a positive max_items ceiling')
            elif isinstance(items,list) and len(items)>cap:errors.append(f'Request asks for {len(items)} items, over the approved ceiling of {cap}')
        if data.get('credits_remaining') is None:warnings.append('Remaining credits unknown; cost certainty is not established.')
        else:
            credits=data['credits_remaining']
            if isinstance(credits,bool) or not isinstance(credits,(int,float)) or not math.isfinite(credits) or credits<0:errors.append('credits_remaining must be a nonnegative number or null')
            elif credits==0:errors.append('Zero credits on the named account: stop, and ask the user to switch to another funded account they own. Never rotate identities to evade a limit')
        warnings.append('This checks that an approval was recorded and that the request stays inside it. It cannot prove the user actually granted that approval.')
    else:errors.append('kind must be brief, creative or generation_request')
    return errors,warnings

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file');a=p.parse_args()
    try:d=json.loads(Path(a.file).read_text(encoding='utf-8'));errors,warnings=check(d)
    except (OSError,ValueError,RecursionError) as e:p.exit(1,str(e)+'\n')
    print(json.dumps({'errors':errors,'warnings':warnings},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
