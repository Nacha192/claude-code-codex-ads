"""Validate package shape, local links, privacy patterns, checksums and archive contents."""
import hashlib,json,re,zipfile
from pathlib import Path
from build import NAMES,ROOT,BUILD

GENERATED=['SKILL.md','LICENSE','THIRD_PARTY_NOTICES.md','install-this-skill.md','manifest.json']
LINK=re.compile(r'\[[^\]]*\]\(([^)]+)\)')

def local_links(file,errors):
 try:text=file.read_text(encoding='utf-8')
 except (OSError,UnicodeDecodeError):errors.append('Unreadable markdown '+str(file.relative_to(ROOT)));return
 # Only markdown local links, not illustrative code/URLs.
 for link in LINK.findall(text):
  if re.match(r'^[a-z]+:',link) or link.startswith('#'):continue
  target=link.split('#')[0].strip('<>')
  if target and not (file.parent/target).exists():errors.append('Broken link '+str(file.relative_to(ROOT))+' -> '+target)
 if '<VERIFY>' in text:errors.append('Unresolved bridge placeholder '+str(file))

def validate():
 errors=[]
 skills=list((ROOT/'you-can-install-skill').glob('*/SKILL.md'))
 if len(skills)!=4:errors.append('Expected exactly four installed entrypoints')
 source=json.loads((BUILD/'research/sources.json').read_text(encoding='utf-8'))
 ids={s['id'] for s in source}
 if len(source)!=73 or len(ids)!=73:errors.append('Expected 73 unique inspected sources')
 # This pack is still creative only: nothing routed to video or voice may ship in it.
 moved={s['id'] for s in source if s['route'] in ('video','voice')}
 static_ids=ids-moved
 selections=json.loads((BUILD/'research/selections.json').read_text(encoding='utf-8'))
 for key,rows in selections.items():
  if len(rows)!=10 or len(set(rows))!=10 or not set(rows)<=static_ids:errors.append('Invalid top-ten '+key)
 if len(selections)!=6:errors.append('Expected six lists')
 if set((BUILD/'src/common/references').glob('video*.md')):errors.append('A video reference is still in the shared sources')
 for ident in sorted(moved):
  if (BUILD/'src/common/modules'/(ident+'.md')).exists():errors.append('Non-static module still built: '+ident)
 shared={f.relative_to(BUILD/'src/common').as_posix() for f in (BUILD/'src/common').rglob('*') if f.is_file() and '__pycache__' not in f.parts}
 for name in NAMES:
  p=ROOT/'you-can-install-skill'/name;entry=(p/'SKILL.md').read_text(encoding='utf-8')
  if not entry.startswith('---\nname: '+name+'\n') or '\ndescription: ' not in entry:errors.append('Frontmatter '+name)
  for relative in sorted(shared):
   target=p/relative
   if not target.exists() or target.read_bytes()!=(BUILD/'src/common'/relative).read_bytes():errors.append('Shared module drift '+str(target))
  # Reverse direction: a file with no source must not survive in a shipped pack.
  for file in p.rglob('*'):
   if not file.is_file() or '__pycache__' in file.parts:continue
   relative=file.relative_to(p).as_posix()
   if relative not in shared and relative not in GENERATED:errors.append('Orphan file in pack '+name+': '+relative)
  for file in p.rglob('*.md'):local_links(file,errors)
  zpath=ROOT/f'install-{name}.zip'
  with zipfile.ZipFile(zpath) as z:
   actual={i.filename:z.read(i.filename) for i in z.infolist()}
   expected={f.relative_to(ROOT/'you-can-install-skill').as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
   if actual!=expected:errors.append('ZIP differs '+name)
 # SAFETY.md promises a test behind each enforced rule; a renamed test would turn
 # that table into a false claim without anything failing.
 suite=(BUILD/'tests/test_tools.py').read_text(encoding='utf-8')
 defined=set(re.findall(r'def (test_\w+)',suite))
 cited=set(re.findall(r'`(test_\w+)`',(BUILD/'SAFETY.md').read_text(encoding='utf-8')))
 for name in sorted(cited-defined):errors.append('SAFETY.md cites a test that does not exist: '+name)
 archives=sorted(ROOT.glob('install-*.zip'))
 if len(archives)!=4:errors.append('Expected four ZIPs')
 # The published checksums must describe the archives that are actually here.
 published={}
 sums=ROOT/'SHA256SUMS'
 if not sums.is_file():errors.append('SHA256SUMS is missing')
 else:
  for line in sums.read_text(encoding='utf-8').splitlines():
   if not line.strip():continue
   digest,_,filename=line.partition('  ');published[filename]=digest
  if set(published)!={a.name for a in archives}:errors.append('SHA256SUMS does not list exactly the four archives')
  for archive in archives:
   if published.get(archive.name)!=hashlib.sha256(archive.read_bytes()).hexdigest():errors.append('Checksum mismatch for '+archive.name)
 # Documentation outside the build sources: its links must resolve as published.
 for file in ROOT.rglob('*.md'):
  if '.git' in file.parts or (BUILD/'src') in file.parents:continue
  if (ROOT/'you-can-install-skill') in file.parents and file.parent!=ROOT/'you-can-install-skill':continue
  local_links(file,errors)
 for file in ROOT.rglob('*'):
  if not file.is_file() or '.git' in file.parts or '__pycache__' in file.parts or file.suffix=='.zip':continue
  if file.suffix in ['.md','.py','.json','.jsonl','.yaml','.yml']:
   try:text=file.read_text(encoding='utf-8')
   except (OSError,UnicodeDecodeError):errors.append('Unreadable release file '+str(file.relative_to(ROOT)));continue
   patterns=[r'[A-Za-z]:[/\\]Users[/\\]',r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{24,}',r'(?i)Bearer\s+[A-Za-z0-9_\-]{24,}']
   if file.name not in ['validate_release.py','check_artifact.py'] and any(re.search(x,text) for x in patterns):errors.append('Potential private data '+str(file.relative_to(ROOT)))
 print(json.dumps({'errors':errors,'skill_count':len(skills),'source_count':len(source),'zip_count':len(archives)},indent=2))
 return bool(errors)
if __name__=='__main__':raise SystemExit(validate())
