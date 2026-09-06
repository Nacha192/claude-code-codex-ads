"""Offline checks for brief, creative, and storyboard JSON. No API calls."""
import argparse,json,math
from datetime import date
from pathlib import Path

def check(data):
    errors=[];warnings=[]
    if not isinstance(data,dict):return ['Artifact must be an object'],[]
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
        proof=data.get('evidence',[]);claims=data.get('claims',[])
        if not isinstance(proof,list) or not isinstance(claims,list):return errors+['evidence and claims must be arrays'],warnings
        ids={}
        for row in proof:
            if not isinstance(row,dict):errors.append('Evidence must be objects');continue
            eid=row.get('id')
            if not isinstance(eid,str) or not eid.strip():errors.append('Evidence id missing');continue
            if eid in ids:errors.append('Duplicate evidence id '+eid)
            ids[eid]=row
            if row.get('type') not in ['user_stated','product_observed','customer_quote','measurement','public_observation','derived','hypothesis','unverified']:errors.append('Unknown evidence type')
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
    elif kind=='storyboard':
        scenes=data.get('scenes')
        if not isinstance(scenes,list) or not scenes:return errors+['Nonempty scenes array required'],warnings
        previous=0.0
        for i,s in enumerate(scenes):
            if not isinstance(s,dict):errors.append('Scene must be an object');continue
            start=s.get('start');end=s.get('end')
            valid=lambda n:isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n)
            if not valid(start) or not valid(end) or start<0 or end<=start:errors.append(f'Scene {i}: invalid times');continue
            if start<previous:errors.append(f'Scene {i}: overlap; use explicit transition metadata in the source project instead')
            if start>previous:warnings.append(f'Scene {i}: timeline gap requires review')
            previous=end
            need(s,'visual')
            duration=s.get('measured_voice_seconds')
            if duration is not None and (not valid(duration) or duration<0):errors.append(f'Scene {i}: invalid measured voice duration')
            elif duration is not None and duration>end-start:errors.append(f'Scene {i}: voice exceeds available scene duration')
            elif s.get('voice') and duration is None:warnings.append(f'Scene {i}: narration fit not measured')
    else:errors.append('kind must be brief, creative or storyboard')
    return errors,warnings

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file');a=p.parse_args()
    try:d=json.loads(Path(a.file).read_text(encoding='utf-8'));errors,warnings=check(d)
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
    print(json.dumps({'errors':errors,'warnings':warnings},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
