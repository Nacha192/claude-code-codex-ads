"""Install selected all-in-one skills locally. Preview by default; no network."""
import argparse,hashlib,json,os,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHOICES={'codex':['meta-ads-codex','meta-ads-team-codex-and-claude-code'],
         'claude':['meta-ads-claude-code','meta-ads-team-claude-code-and-codex']}

def inventory(root):
    result={}
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('Symbolic links are not accepted in a skill package')
        if p.is_file() and '__pycache__' not in p.parts:
            result[p.relative_to(root).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result

def install(runtime,mode='both',project=None,target_root=None,apply=False):
    if runtime not in CHOICES:raise ValueError('Unknown runtime')
    if mode not in ['solo','team','both']:raise ValueError('Unknown mode')
    if project and target_root:raise ValueError('Choose project or target-root, not both')
    if project:
        parent=Path(project).expanduser().resolve(strict=True)
        if not parent.is_dir():raise ValueError('Project must be a directory')
        target=parent/('.agents' if runtime=='codex' else '.claude')/'skills'
    elif target_root:target=Path(target_root).expanduser().absolute()
    else:target=Path.home()/('.agents' if runtime=='codex' else '.claude')/'skills'
    # Resolve legitimate system aliases (for example macOS /var), but refuse a redirected target leaf.
    if target.is_symlink():raise ValueError('Refusing symlinked installation target')
    target=target.resolve()
    names=CHOICES[runtime] if mode=='both' else [CHOICES[runtime][0 if mode=='solo' else 1]]
    plans=[]
    for name in names:
        source=ROOT/name
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
            source=ROOT/plan['skill']
            for relative in inventory(source):
                out=dest/relative;out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('xb') as f:f.write((source/relative).read_bytes())
            if inventory(dest)!=inventory(source):raise ValueError('Installed hash verification failed')
    return plans

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime',choices=CHOICES,required=True);p.add_argument('--mode',choices=['solo','team','both'],default='both');g=p.add_mutually_exclusive_group();g.add_argument('--project');g.add_argument('--target-root');p.add_argument('--apply',action='store_true');a=p.parse_args()
    try:print(json.dumps(install(a.runtime,a.mode,a.project,a.target_root,a.apply),indent=2))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
