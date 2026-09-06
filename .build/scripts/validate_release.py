"""Validate package shape, local links, privacy patterns and archive contents."""
import hashlib,json,re,zipfile
from pathlib import Path
from build import NAMES,ROOT,BUILD

def validate():
 errors=[]
 skills=list((ROOT).glob('*/SKILL.md'))
 if len(skills)!=4:errors.append('Expected exactly four installed entrypoints')
 source=json.loads((BUILD/'research/sources.json').read_text(encoding='utf-8'))
 ids={s['id'] for s in source}
 if len(source)!=73 or len(ids)!=73:errors.append('Expected 73 unique inspected sources')
 for key,rows in json.loads((BUILD/'research/selections.json').read_text()).items():
  if len(rows)!=10 or len(set(rows))!=10 or not set(rows)<=ids:errors.append('Invalid top-ten '+key)
 if len(json.loads((BUILD/'research/selections.json').read_text()))!=8:errors.append('Expected eight lists')
 for name in NAMES:
  p=ROOT/name;entry=(p/'SKILL.md').read_text(encoding='utf-8')
  if not entry.startswith('---\nname: '+name+'\n') or '\ndescription: ' not in entry:errors.append('Frontmatter '+name)
  for shared in (BUILD/'src/common').rglob('*'):
   if shared.is_file() and '__pycache__' not in shared.parts:
    target=p/shared.relative_to(BUILD/'src/common')
    if not target.exists() or target.read_bytes()!=shared.read_bytes():errors.append('Shared module drift '+str(target))
  for file in p.rglob('*.md'):
   text=file.read_text(encoding='utf-8')
   # Only markdown local links, not illustrative code/URLs.
   for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
    if re.match(r'^[a-z]+:',link) or link.startswith('#'):continue
    target=link.split('#')[0].strip('<>')
    if target and not (file.parent/target).exists():errors.append('Broken link '+str(file.relative_to(ROOT))+' -> '+target)
   if '<VERIFY>' in text:errors.append('Unresolved bridge placeholder '+str(file))
  zpath=ROOT/f'install-{name}.zip'
  with zipfile.ZipFile(zpath) as z:
   actual={i.filename:z.read(i.filename) for i in z.infolist()}
   expected={f.relative_to(ROOT).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
   if actual!=expected:errors.append('ZIP differs '+name)
 if len(list(ROOT.glob('install-*.zip')))!=4:errors.append('Expected four ZIPs')
 for file in ROOT.rglob('*'):
  if not file.is_file() or '.git' in file.parts or '__pycache__' in file.parts or file.suffix=='.zip':continue
  if file.suffix in ['.md','.py','.json','.jsonl','.yaml','.yml']:
   text=file.read_text(encoding='utf-8')
   patterns=[r'[A-Za-z]:[/\\]Users[/\\]',r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{24,}',r'(?i)Bearer\s+[A-Za-z0-9_\-]{24,}']
   if file.name!='validate_release.py' and any(re.search(x,text) for x in patterns):errors.append('Potential private data '+str(file.relative_to(ROOT)))
 print(json.dumps({'errors':errors,'skill_count':len(skills),'source_count':len(source),'zip_count':len(list(ROOT.glob('install-*.zip')))},indent=2))
 return bool(errors)
if __name__=='__main__':raise SystemExit(validate())
