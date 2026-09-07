"""Install selected all-in-one skills locally. Preview by default; no network."""
# Nothing here removes or moves anything, so nothing that can is imported.
import argparse,hashlib,json
from pathlib import Path
# install.py lives in system/; the unpacked packs sit in you-can-install-skill/ at the root.
ROOT=Path(__file__).resolve().parents[1]
# Two scopes, two runtimes, two modes. A pack is chosen by all three, and the
# default installs the four editions that fit the runtime you name.
CHOICES={'codex':{'static':['meta-ads-static-codex','meta-ads-static-team-codex-and-claude-code'],
                  'motion':['video-ads-codex','video-ads-codex-claude-code']},
         'claude':{'static':['meta-ads-static-claude-code','meta-ads-static-team-claude-code-and-codex'],
                   'motion':['video-ads-claude-code','video-ads-claude-code-codex']}}
SCOPES=['static','motion']

def inventory(root):
    result={}
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('Symbolic links are not accepted in a skill package')
        if p.is_file() and '__pycache__' not in p.parts:
            result[p.relative_to(root).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result

def install(runtime,mode='both',project=None,target_root=None,apply=False,scope='both'):
    if runtime not in CHOICES:raise ValueError('Unknown runtime')
    if mode not in ['solo','team','both']:raise ValueError('Unknown mode')
    if scope not in SCOPES+['both']:raise ValueError('Unknown scope')
    if project and target_root:raise ValueError('Choose project or target-root, not both')
    # An explicit empty string is a mistake, not a request for the default location:
    # falling back would install somewhere the caller never named.
    for label,value in [('project',project),('target-root',target_root)]:
        if value is not None and not str(value).strip():raise ValueError('Empty '+label+' is not a location')
    if project:
        parent=Path(project).expanduser().resolve(strict=True)
        if not parent.is_dir():raise ValueError('Project must be a directory')
        target=parent/('.agents' if runtime=='codex' else '.claude')/'skills'
    elif target_root:target=Path(target_root).expanduser().absolute()
    else:target=Path.home()/('.agents' if runtime=='codex' else '.claude')/'skills'
    # Resolve legitimate system aliases (for example macOS /var), but refuse a redirected target leaf.
    if target.is_symlink():raise ValueError('Refusing symlinked installation target')
    target=target.resolve()
    names=[]
    for one in (SCOPES if scope=='both' else [scope]):
        picks=CHOICES[runtime][one]
        names+=picks if mode=='both' else [picks[0 if mode=='solo' else 1]]
    plans=[]
    for name in names:
        source=ROOT/'you-can-install-skill'/name
        if not (source/'SKILL.md').is_file():raise ValueError('Missing built skill '+name)
        expected=inventory(source);dest=target/name
        if dest.is_symlink():raise ValueError('Refusing symlinked skill destination')
        if dest.exists():
            if not dest.is_dir() or inventory(dest)!=expected:raise ValueError('Existing skill differs; back it up or select another target: '+str(dest))
            plans.append({'skill':name,'target':str(dest),'action':'already-identical'})
        else:plans.append({'skill':name,'target':str(dest),'action':'install' if apply else 'would-install'})
    if apply:
        target.mkdir(parents=True,exist_ok=True)
        for plan in plans:
            if plan['action']!='install':continue
            dest=Path(plan['target']);dest.mkdir(exist_ok=False)
            # Exclusive top-level reservation, then copy only known package files.
            # On I/O failure preserve partial files for inspection; never delete user data.
            source=ROOT/'you-can-install-skill'/plan['skill']
            for relative in inventory(source):
                out=dest/relative;out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('xb') as f:f.write((source/relative).read_bytes())
            if inventory(dest)!=inventory(source):raise ValueError('Installed hash verification failed')
    return plans

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime',choices=CHOICES,required=True);p.add_argument('--mode',choices=['solo','team','both'],default='both');p.add_argument('--scope',choices=SCOPES+['both'],default='both');g=p.add_mutually_exclusive_group();g.add_argument('--project');g.add_argument('--target-root');p.add_argument('--apply',action='store_true');a=p.parse_args()
    try:print(json.dumps(install(a.runtime,a.mode,a.project,a.target_root,a.apply,a.scope),indent=2))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
