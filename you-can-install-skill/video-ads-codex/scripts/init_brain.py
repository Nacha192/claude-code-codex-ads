"""Create the skill's integrated private campaign memory. Python 3.10+, offline."""
import argparse,json
from pathlib import Path

def initialize(project, apply=False):
    project=Path(project).expanduser().resolve(strict=True)
    if not project.is_dir(): raise ValueError('Project must be a directory')
    target=project/'.ads-brain'
    if target.is_symlink(): raise ValueError('Refusing a symbolic-link brain')
    if target.exists():
        raise ValueError('Brain already exists; read and update its records, do not reset it')
    files={'.gitignore':'*\n','index.md':'# Advertising second brain\n\nPrivate project data. Start with brand.json and buyers.json, then retrieve relevant evidence, hypotheses and lessons.\n',
           'brand.json':json.dumps({'schema_v':'1.0.0','status':'intake_required','offer':None,'country':None,'ad_language':None,'facts':[],'unknowns':[]},indent=2)+'\n',
           'buyers.json':json.dumps({'schema_v':'1.0.0','segments':[]},indent=2)+'\n',
           # Reaching this script already proves an interpreter, but record the command
           # and version explicitly; a ZIP install can land on a machine without one.
           'runtime.json':json.dumps({'schema_v':'1.0.0','python':{'status':'unchecked','command':None,'version':None,'checked_at':None}},indent=2)+'\n',
           'lessons.md':'# Campaign lessons\n\nNo measured campaign lessons yet.\n'}
    for name in ['evidence','research','hypotheses','creatives','experiments','decisions','contradictions','operations']:
        files[name+'.jsonl']=''
    if apply:
        target.mkdir(exist_ok=False)
        for name,body in files.items():
            with (target/name).open('x',encoding='utf-8',newline='\n') as f:f.write(body)
    return {'action':'created' if apply else 'preview','directory':str(target),'files':list(files),'next':'Internal .gitignore excludes new records. Verify ignore coverage before private writes or publication; already tracked/force-added files need separate handling.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
    try: print(json.dumps(initialize(a.project,a.apply),indent=2))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
