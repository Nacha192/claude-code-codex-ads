"""Offline validation of a motion-project manifest. Standard library only, no API calls.

The manifest is the single object tying a brief to the files on disk. This script
decides whether it is internally consistent and whether it claims more than it can
show. It never opens a video: `inspect_video.py` does that. The two are separate on
purpose, because a manifest that agrees with itself and disagrees with the render is
exactly the failure this pack exists to catch.
"""
import argparse,hashlib,json,math,re,sys
from pathlib import Path,PurePosixPath

SCHEMA='1.0.0'
# Ordered. A project may not claim a later state while an earlier one is unmet.
STATES=['planned','generated','rendered','measured','inspected','corrected','approved','delivered']
NEEDS_FILE=STATES.index('rendered')
LOCK=['insight','problem','angle','promise','mechanism','proof','objection','cta',
      'register','emotion','hook','reason_to_keep_watching','payoff']
SCENE=['id','role','composition','subject','primary_motion','acceptance']
HOOK_CRITERIA=['specificity','speed_of_understanding','audience_fit','tension',
               'continuity_with_payoff','credibility','first_frame_strength']
SECRET=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{24,}',r'(?i)Bearer\s+[A-Za-z0-9_\-]{24,}',
        r'(?i)\b(api[_-]?key|secret|password|access[_-]?token)\b\s*[:=]\s*\S{8,}']
RATIO=re.compile(r'^\d{1,2}:\d{1,2}$')
VERDICTS=['pass','pass_with_noted_risk','fail']
DEFECT=['timecode','observation','severity','why_it_fails','fix','target','status']

def num(v):
    """A real, finite number. Booleans are not numbers, however Python feels about it."""
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)

def text(v):
    return isinstance(v,str) and bool(v.strip())

def whole(v):
    """A pixel count is a whole number. A frame 1080.5 pixels wide does not exist."""
    return num(v) and float(v).is_integer()

def seq(value,name,errors):
    """A list, or nothing at all.

    A number or a string where a list belongs used to be iterated anyway, which
    crashed on the first and produced a report about single characters on the
    second. A malformed manifest has to be refused, not to take the checker down
    with it.
    """
    if value is None:return []
    if isinstance(value,list):return value
    errors.append(name+' must be a list')
    return []

def escaping(value):
    """Why a declared path could reach outside the project, or None if it cannot.

    Paths in a manifest name files inside the project being delivered. An absolute
    path or one climbing with '..' turns the export check into a read of somewhere
    else on the machine, and lets a manifest written elsewhere pass by pointing at
    a file that was never part of this job.
    """
    if re.match(r'^[A-Za-z]:',value) or value.startswith(('/','\\')):return 'absolute'
    if '..' in PurePosixPath(value.replace('\\','/')).parts:return 'climbing out with ".."'
    return None

def digest_of(path):
    """Hash in chunks. An export is a video, and reading one whole into memory is
    how a checker dies on the delivery it was meant to verify."""
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda:fh.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def walk(node,path='$'):
    """Every string in the document, keys included."""
    if isinstance(node,dict):
        for key,value in node.items():
            if isinstance(key,str):yield path+'.<key>',key
            yield from walk(value,path+'.'+str(key))
    elif isinstance(node,list):
        for i,value in enumerate(node):yield from walk(value,path+'['+str(i)+']')
    elif isinstance(node,str):yield path,node

def ratio_of(w,h):
    g=math.gcd(int(w),int(h)) or 1
    return '%d:%d'%(int(w)//g,int(h)//g)

LAYER_KINDS = {'image', 'video', 'text', 'shape'}
# Fractions of the frame, so a layout survives being composed at three sizes. A value
# outside this range is a pixel count somebody wrote in the wrong field.
FRACTION = ['x', 'y', 'w', 'h', 'opacity', 'parallax', 'camera_amount', 'gap']


def check_layers(scene, index, errors, asset_ids):
    """The drawing instructions of one scene, checked before a renderer sees them.

    A layer the renderer cannot draw is a failure halfway through a job that has
    already spent minutes encoding, and the message it produces names a filter rather
    than the scene. Catching it here costs nothing and says where to look.
    """
    layers = scene.get('layers')
    if layers is None:
        return
    if not isinstance(layers, list):
        errors.append('Scene %d: layers must be a list' % index)
        return
    for n, layer in enumerate(layers):
        where = 'Scene %d layer %d' % (index, n)
        if not isinstance(layer, dict):
            errors.append(where + ' must be an object')
            continue
        kind = layer.get('kind')
        if kind not in LAYER_KINDS:
            errors.append('%s has kind %r, and only %s can be drawn'
                          % (where, kind, ', '.join(sorted(LAYER_KINDS))))
            continue
        if kind in ('image', 'video'):
            ref = layer.get('asset')
            if not isinstance(ref, str) or ref not in asset_ids:
                errors.append('%s references unknown asset %r' % (where, ref))
        if kind == 'text' and not text(layer.get('content')):
            errors.append(where + ' is text with nothing to say')
        for field in FRACTION:
            value = layer.get(field)
            if value is None:
                continue
            if not num(value) or not 0 <= value <= 1:
                errors.append('%s: %s is %r, and these are fractions of the frame '
                              'between 0 and 1, not pixels' % (where, field, value))
        at = layer.get('at')
        if at is not None:
            span = float(scene['end']) - float(scene['start'])
            if not num(at) or at < 0:
                errors.append('%s starts at %r' % (where, at))
            elif at >= span:
                errors.append('%s starts at %.2fs, after its own scene has ended'
                              % (where, at))


def check(data,root=None):
    """Return (errors, warnings). Errors block delivery, warnings are reported and pass."""
    errors=[];warnings=[]
    if not isinstance(data,dict):return ['Manifest must be a JSON object'],[]

    if data.get('kind')!='motion_project':errors.append('kind must be "motion_project"')
    if data.get('schema_v')!=SCHEMA:errors.append('schema_v must be '+SCHEMA)
    state=data.get('state')
    if state not in STATES:errors.append('state must be one of: '+', '.join(STATES))
    rank=STATES.index(state) if state in STATES else -1

    # A credential pasted as a field name travels as far as one pasted as a value.
    for where,value in walk(data):
        for pattern in SECRET:
            if re.search(pattern,value):
                errors.append('Credential-shaped value at '+where);break

    brief=data.get('brief')
    if not isinstance(brief,dict):errors.append('brief object required')
    else:
        for field in ['offer','audience','objective','market','ad_language','cta_destination']:
            if not text(brief.get(field)):errors.append('brief.'+field+' required as nonempty text')
        window=brief.get('duration_seconds')
        if isinstance(window,list) and len(window)==2 and all(num(x) and x>0 for x in window):
            if window[0]>window[1]:errors.append('brief.duration_seconds range is reversed')
        elif not (num(window) and window>0):
            errors.append('brief.duration_seconds must be a positive number or a [min,max] range')
        asked=brief.get('formats')
        if not isinstance(asked,list) or not asked:errors.append('brief.formats must be a nonempty list')
        else:
            for r in asked:
                if not (text(r) and RATIO.match(r)):errors.append('brief.formats entry is not a ratio like 9:16: '+repr(r))

    # The one-shot contract: proceeding without an answer is allowed, hiding it is not.
    for i,a in enumerate(seq(data.get('assumptions'),'assumptions',errors)):
        if not isinstance(a,dict):errors.append('assumptions[%d] must be an object'%i);continue
        for field in ['field','value','because','changes_if_wrong']:
            if not text(a.get(field)):errors.append('assumptions[%d].%s required'%(i,field))

    evidence=seq(data.get('evidence'),'evidence',errors)
    ids=set()
    for i,e in enumerate(evidence):
        if not isinstance(e,dict):errors.append('evidence[%d] must be an object'%i);continue
        eid=e.get('id')
        if not text(eid):errors.append('evidence[%d].id required'%i);continue
        if eid in ids:errors.append('Duplicate evidence id: '+eid)
        ids.add(eid)
        if not text(e.get('type')):errors.append('evidence[%s].type required'%eid)
        if not text(e.get('source')):errors.append('evidence[%s].source required'%eid)
    for i,c in enumerate(seq(data.get('claims'),'claims',errors)):
        if not isinstance(c,dict):errors.append('claims[%d] must be an object'%i);continue
        if not text(c.get('text')):errors.append('claims[%d].text required'%i)
        proofs=c.get('proof_ids')
        if not isinstance(proofs,list) or not proofs:
            errors.append('Claim %d carries no proof_ids: %s'%(i,str(c.get('text'))[:60]));continue
        for p in proofs:
            if not isinstance(p,str) or p not in ids:
                errors.append('Claim %d points at unknown evidence: %r'%(i,p));continue
            kind=next((x.get('type') for x in evidence if isinstance(x,dict) and x.get('id')==p),None)
            if kind=='hypothesis':
                errors.append('Claim %d rests on hypothesis %s; a hypothesis is not proof'%(i,p))

    lock=data.get('creative_lock')
    if not isinstance(lock,dict):errors.append('creative_lock object required')
    else:
        for field in LOCK:
            if not text(lock.get(field)):errors.append('creative_lock.'+field+' required')
    hooks=data.get('hooks_considered')
    if not isinstance(hooks,list) or len(hooks)<3:
        errors.append('hooks_considered must hold at least three hooks; choosing from one is not choosing')
    else:
        chosen=[h for h in hooks if isinstance(h,dict) and h.get('selected')]
        if len(chosen)!=1:errors.append('Exactly one hook must be marked selected')
        for i,h in enumerate(hooks):
            if not isinstance(h,dict):errors.append('hooks_considered[%d] must be an object'%i);continue
            if not text(h.get('text')):errors.append('hooks_considered[%d].text required'%i)
            scores=h.get('scores')
            if not isinstance(scores,dict):errors.append('hooks_considered[%d].scores required'%i);continue
            for crit in HOOK_CRITERIA:
                if not num(scores.get(crit)):errors.append('hooks_considered[%d].scores.%s must be a number'%(i,crit))
        for h in chosen:
            if not text(h.get('why')):errors.append('The selected hook must say why it won')
        if isinstance(lock,dict) and chosen and text(lock.get('hook')) and chosen[0].get('text')!=lock.get('hook'):
            errors.append('creative_lock.hook does not match the hook marked selected')

    scenes=data.get('scenes')
    total=0.0
    if not isinstance(scenes,list) or not scenes:errors.append('scenes must be a nonempty list')
    else:
        seen=set();last_end=None
        for i,s in enumerate(scenes):
            if not isinstance(s,dict):errors.append('scenes[%d] must be an object'%i);continue
            for field in SCENE:
                if not text(s.get(field)):errors.append('Scene %d: %s required'%(i,field))
            sid=s.get('id')
            if text(sid):
                if sid in seen:errors.append('Duplicate scene id: '+str(sid))
                seen.add(sid)
            start,end=s.get('start'),s.get('end')
            if not (num(start) and num(end)):errors.append('Scene %d: start and end must be finite numbers'%i);continue
            if start<0:errors.append('Scene %d: negative start'%i)
            if end<=start:errors.append('Scene %d: end must be after start'%i);continue
            if last_end is not None:
                if start<last_end:errors.append('Scene %d overlaps the previous scene'%i)
                elif start>last_end:warnings.append('Gap in the timeline before scene %d'%i)
            last_end=end;total=max(total,end)
            narration=s.get('narration')
            if narration is not None and not text(narration):
                errors.append('Scene %d: narration must be nonempty text when present'%i)
            measured=s.get('measured_voice_seconds')
            if measured is not None:
                if not num(measured) or measured<0:errors.append('Scene %d: invalid measured_voice_seconds'%i)
                elif not text(narration):errors.append('Scene %d: measured narration on a scene with no line'%i)
                elif measured==0:errors.append('Scene %d: a spoken line cannot measure zero seconds'%i)
                elif measured>end-start:errors.append('Scene %d: narration exceeds the scene it sits in'%i)
            elif text(narration):
                warnings.append('Scene %d: narration fit not measured'%i)

    if isinstance(brief,dict) and total>0:
        window=brief.get('duration_seconds')
        if num(window) and abs(total-window)>0.75:
            errors.append('Timeline runs %.2fs and the brief asks for %.2fs'%(total,window))
        elif isinstance(window,list) and len(window)==2 and all(num(x) for x in window):
            if not (window[0]-0.75<=total<=window[1]+0.75):
                errors.append('Timeline runs %.2fs, outside the requested %s to %ss'%(total,window[0],window[1]))

    voice=data.get('voice')
    spoken=isinstance(scenes,list) and any(isinstance(s,dict) and text(s.get('narration')) for s in scenes)
    if spoken:
        if not isinstance(voice,dict):errors.append('voice object required when any scene carries narration')
        else:
            for field in ['archetype','source']:
                if not text(voice.get(field)):errors.append('voice.'+field+' required')
            if voice.get('source')=='cloned' and not text(voice.get('consent_ref')):
                errors.append('A cloned voice requires consent_ref pointing at the recorded consent')

    captions=data.get('captions')
    if isinstance(captions,dict):
        if captions.get('derived_from')!='final_take':
            errors.append('captions.derived_from must be "final_take": captions written from the script drift from the read')
        cues=captions.get('cues')
        if not isinstance(cues,list):errors.append('captions.cues must be a list')
        else:
            for i,c in enumerate(cues):
                if not isinstance(c,dict):errors.append('captions.cues[%d] must be an object'%i);continue
                cs,ce=c.get('start'),c.get('end')
                if not (num(cs) and num(ce)):errors.append('captions.cues[%d]: start and end must be numbers'%i);continue
                if ce<=cs:errors.append('captions.cues[%d]: end must be after start'%i)
                if cs<0:errors.append('captions.cues[%d]: negative start'%i)
                if total and ce>total+0.001:
                    errors.append('captions.cues[%d] ends at %.2fs, past the %.2fs timeline'%(i,ce,total))
                if not text(c.get('text')):errors.append('captions.cues[%d].text required'%i)
    elif captions is not None:errors.append('captions must be an object')

    loud=data.get('loudness_target')
    if isinstance(loud,dict):
        if not num(loud.get('value')):errors.append('loudness_target.value must be a number')
        if not text(loud.get('unit')):errors.append('loudness_target.unit required')
        if not text(loud.get('source')):
            errors.append('loudness_target.source required: a target with no origin is a preference wearing a standard')
    elif loud is not None:errors.append('loudness_target must be an object')

    asset_ids=set()
    for i,a in enumerate(seq(data.get('assets'),'assets',errors)):
        if not isinstance(a,dict):errors.append('assets[%d] must be an object'%i);continue
        aid=a.get('id')
        if not text(aid):errors.append('assets[%d].id required'%i);continue
        if aid in asset_ids:errors.append('Duplicate asset id: '+aid)
        asset_ids.add(aid)
        if not text(a.get('rights')):errors.append('Asset '+aid+' has no recorded rights')
        if text(a.get('path')):
            why=escaping(a['path'])
            if why:errors.append('Asset %s has a path %s: an asset path names a file inside the project'%(aid,why))
        if a.get('identifiable_person'):
            if not text(a.get('release_ref')):errors.append('Asset '+aid+' shows an identifiable person and has no release_ref')
            if not text(a.get('release_expires')):errors.append('Asset '+aid+' has a release with no expiry date recorded')
    if isinstance(scenes,list):
        for i,s in enumerate(scenes):
            if not isinstance(s,dict):continue
            if num(s.get('start')) and num(s.get('end')) and s['end']>s['start']:
                check_layers(s,i,errors,asset_ids)
            refs=s.get('assets')
            if refs is None:continue
            if not isinstance(refs,list):errors.append('Scene %d: assets must be a list of ids'%i);continue
            for aid in refs:
                # A dict or a list here would reach a set membership test and raise
                # TypeError: unhashable. An id is a string or it is not an id.
                if not isinstance(aid,str) or aid not in asset_ids:
                    errors.append('Scene %d references unknown asset %r'%(i,aid))

    engine=data.get('engine')
    if not isinstance(engine,dict):errors.append('engine object required')
    else:
        if not text(engine.get('kind')):errors.append('engine.kind required')
        if not text(engine.get('name')):errors.append('engine.name required')
        if engine.get('detected') is not True:
            errors.append('engine.detected must be true: the pipeline is chosen from what was found, not from what was hoped for')

    formats=data.get('formats')
    built=set()
    if not isinstance(formats,list) or not formats:errors.append('formats must be a nonempty list')
    else:
        for i,f in enumerate(formats):
            if not isinstance(f,dict):errors.append('formats[%d] must be an object'%i);continue
            r,w,h,fps=f.get('ratio'),f.get('width'),f.get('height'),f.get('fps')
            if not (text(r) and RATIO.match(r)):errors.append('formats[%d].ratio must look like 9:16'%i);continue
            if r in built:errors.append('Format %s appears twice'%r)
            built.add(r)
            if not (whole(w) and whole(h) and w>0 and h>0):errors.append('formats[%s]: width and height must be whole positive pixel counts'%r);continue
            if ratio_of(w,h)!=r:errors.append('formats[%s]: %dx%d is %s, not %s'%(r,int(w),int(h),ratio_of(w,h),r))
            if not (num(fps) and fps>0):errors.append('formats[%s].fps required'%r)
            if not isinstance(f.get('safe_zones'),dict):errors.append('formats[%s].safe_zones required'%r)
            if not text(f.get('composition')):
                errors.append('formats[%s] has no composition of its own: a blind crop of another ratio is not a composition'%r)
    if isinstance(brief,dict) and isinstance(brief.get('formats'),list):
        for r in brief['formats']:
            if isinstance(r,str) and r not in built:errors.append('Brief asks for %s and no format was composed for it'%r)

    exports=seq(data.get('exports'),'exports',errors)
    if rank>=NEEDS_FILE:
        if not exports:errors.append('state is "%s" and no export is listed'%state)
        done=set()
        for i,e in enumerate(exports):
            if not isinstance(e,dict):errors.append('exports[%d] must be an object'%i);continue
            r=e.get('ratio');path=e.get('path')
            if not (text(r) and RATIO.match(r)):errors.append('exports[%d].ratio required'%i)
            else:done.add(r)
            if not text(path):errors.append('exports[%d].path required'%i);continue
            why=escaping(path)
            if why:
                errors.append('exports[%s] has a path %s: an export path names a file inside the project'%(r,why));continue
            digest=e.get('sha256')
            good=isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest)
            if not good:
                errors.append('exports[%s] has no sha256: an export nobody hashed is an export nobody can prove'%r)
            if root is not None:
                base=Path(root).resolve()
                p=base/path
                # Second lock, after the textual one: a symlink inside the tree can
                # still point out of it, and only resolving the real path sees that.
                try:p.resolve().relative_to(base)
                except (OSError,ValueError):
                    errors.append('exports[%s] resolves outside the project root: %s'%(r,path));continue
                if not p.is_file():errors.append('exports[%s] names a file that is not there: %s'%(r,path))
                elif good:
                    try:
                        if digest_of(p)!=digest:errors.append('exports[%s] hash does not match the file on disk'%r)
                    except OSError as exc:errors.append('exports[%s] could not be read: %s'%(r,exc))
        for r in sorted(built-done):errors.append('Format %s was composed and never exported'%r)
    elif exports:
        warnings.append('Exports are listed while the state is "%s"; the state is what the delivery is judged on'%state)

    qa=data.get('qa')
    if rank>=STATES.index('inspected'):
        if not isinstance(qa,dict):errors.append('qa object required once the project claims to be inspected')
        else:
            for half in ['technical','creative']:
                block=qa.get(half)
                if not isinstance(block,dict):errors.append('qa.'+half+' required');continue
                if block.get('verdict') not in VERDICTS:
                    errors.append('qa.%s.verdict must be one of: %s'%(half,', '.join(VERDICTS)))
                if block.get('verdict')=='fail' and rank>=STATES.index('approved'):
                    errors.append('qa.%s failed and the project claims to be %s'%(half,state))
                for j,d in enumerate(seq(block.get('defects'),'qa.'+half+'.defects',errors)):
                    if not isinstance(d,dict):errors.append('qa.%s.defects[%d] must be an object'%(half,j));continue
                    for field in DEFECT:
                        if not text(d.get(field)):errors.append('qa.%s.defects[%d].%s required'%(half,j,field))
                    if d.get('severity') in ('blocking','high') and d.get('status')=='open' and rank>=STATES.index('approved'):
                        errors.append('qa.%s.defects[%d] is %s and still open'%(half,j,d.get('severity')))
            creative=qa.get('creative')
            if isinstance(creative,dict) and creative.get('verdict')=='pass' and not text(creative.get('reviewed_by')):
                warnings.append('Creative QA passed with no reviewer recorded')

    pending=data.get('human_decisions_pending')
    if pending is not None and not isinstance(pending,list):errors.append('human_decisions_pending must be a list')
    elif pending and rank>=STATES.index('delivered'):
        warnings.append('Delivered with %d decision(s) still on a human; name them in the handover'%len(pending))
    return errors,warnings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('path')
    p.add_argument('--root',help='Directory the export paths are relative to; enables file and hash checks')
    a=p.parse_args()
    try:data=json.loads(Path(a.path).read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:print('Unreadable manifest: '+str(e));return 2
    errors,warnings=check(data,a.root)
    for w in warnings:print('warning: '+w)
    for e in errors:print('error: '+e)
    print(json.dumps({'errors':len(errors),'warnings':len(warnings)}))
    return 1 if errors else 0

if __name__=='__main__':sys.exit(main())
