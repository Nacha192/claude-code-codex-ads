"""Validate package shape, local links, privacy patterns, checksums and archive contents."""
import hashlib,json,re,zipfile
from pathlib import Path
from build import SCOPES,NAMES,ROOT,BUILD

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

def files_under(root):
 return {f.relative_to(root).as_posix():f for f in root.rglob('*') if f.is_file() and '__pycache__' not in f.parts}

def reachable(pack):
 """Every .md a reader can actually get to by following links from SKILL.md."""
 seen=set();queue=[pack/'SKILL.md']
 while queue:
  f=queue.pop()
  if not f.is_file():continue
  try:text=f.read_text(encoding='utf-8')
  except (OSError,UnicodeDecodeError):continue
  for link in LINK.findall(text):
   if re.match(r'^[a-z]+:',link) or link.startswith('#'):continue
   target=(f.parent/link.split('#')[0].strip('<>')).resolve()
   if target.suffix=='.md' and target.is_file() and target not in seen:seen.add(target);queue.append(target)
 return {p.relative_to(pack).as_posix() for p in seen}

def validate():
 errors=[]
 skills=list((ROOT/'you-can-install-skill').glob('*/SKILL.md'))
 if len(skills)!=len(NAMES):errors.append(f'Expected exactly {len(NAMES)} installed entrypoints')
 source=json.loads((BUILD/'research/sources.json').read_text(encoding='utf-8'))
 ids={s['id'] for s in source}
 if len(source)!=73 or len(ids)!=73:errors.append('Expected 73 unique inspected sources')
 selections=json.loads((BUILD/'research/selections.json').read_text(encoding='utf-8'))
 if set(selections)!=set(SCOPES):errors.append('Selections must cover exactly the built scopes')
 common=files_under(BUILD/'src/common')
 # The split is the point of this repository, so it is checked structurally rather
 # than against a list of names somebody has to remember to extend.
 # A generated source card in the trunk would reach both halves at once.
 for relative in sorted(common):
  if relative.startswith('modules/'):errors.append('Source card sitting in the shared trunk: '+relative)
 # A file that exists in the trunk and in a craft layer is ambiguous: the pack gets
 # one of them and nobody can tell which by reading the tree.
 for scope in SCOPES:
  for relative in sorted(set(common)&set(files_under(BUILD/'src'/scope))):
   errors.append('Name defined in both the trunk and the '+scope+' layer: '+relative)
 for scope,spec in SCOPES.items():
  layer=BUILD/'src'/scope
  shared={**common,**files_under(layer)}
  own={s['id'] for s in source if s['route'] in spec['routes']}
  foreign=ids-own
  rows=selections.get(scope,{})
  if len(rows)!=6:errors.append('Expected six lists in scope '+scope)
  for key,entries in rows.items():
   if len(entries)!=10 or len(set(entries))!=10 or not set(entries)<=own:errors.append('Invalid top-ten '+scope+'/'+key)
  # A reference nobody can reach is dead weight that still ships, and it is how a
  # merged trunk quietly grows files one half never reads.
  read=set()
  for name in spec['names']:read|=reachable(ROOT/'you-can-install-skill'/name)
  for relative in sorted(shared):
   if relative.startswith(('references/','modules/')) and relative not in read:errors.append('Unreachable from any '+scope+' entrypoint: '+relative)
  # Checked against what the packs actually contain, not against the layer that was
  # supposed to fill them, so a card arriving by any other route is still caught.
  for name in spec['names']:
   for ident in sorted(foreign):
    if (ROOT/'you-can-install-skill'/name/'modules'/(ident+'.md')).exists():errors.append('Module from the other half shipped in '+name+': '+ident)
  for route,target in sorted(spec['routes'].items()):
   if 'references/'+target not in shared:errors.append('Route '+route+' in scope '+scope+' points at a missing reference: '+target)
  for name in spec['names']:
   p=ROOT/'you-can-install-skill'/name;entry=(p/'SKILL.md').read_text(encoding='utf-8')
   if not entry.startswith('---\nname: '+name+'\n') or '\ndescription: ' not in entry:errors.append('Frontmatter '+name)
   for relative,origin in sorted(shared.items()):
    target=p/relative
    if not target.exists() or target.read_bytes()!=origin.read_bytes():errors.append('Shared module drift '+str(target))
   # Reverse direction: a file with no source must not survive in a shipped pack.
   for relative in files_under(p):
    if relative not in shared and relative not in GENERATED:errors.append('Orphan file in pack '+name+': '+relative)
   if json.loads((p/'manifest.json').read_text(encoding='utf-8')).get('scope')!=scope:errors.append('Manifest scope mismatch in '+name)
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
 if len(archives)!=len(NAMES):errors.append(f'Expected {len(NAMES)} ZIPs')
 # The published checksums must describe the archives that are actually here.
 published={}
 sums=ROOT/'SHA256SUMS'
 if not sums.is_file():errors.append('SHA256SUMS is missing')
 else:
  for line in sums.read_text(encoding='utf-8').splitlines():
   if not line.strip():continue
   digest,_,filename=line.partition('  ');published[filename]=digest
  if set(published)!={a.name for a in archives}:errors.append('SHA256SUMS does not list exactly the built archives')
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
