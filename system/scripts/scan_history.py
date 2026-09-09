"""Scan every blob of every commit, not only the working tree.

A clone carries the whole history. `validate_release.py` reads the tree that is
checked out, so anything that was committed once and removed later stays published
and stays invisible to it. That is exactly how a copyright line naming the author
survived a history rewrite that had cleaned three other files.

Findings are reported by location and kind. The matching text is never printed:
a scanner that echoes what it found puts it in a log, a terminal and a CI page.

Exit codes: 0 clean, 1 findings, 2 not a git repository.
"""
import json,re,subprocess,sys

SECRETS=[('github token',rb'gh[pousr]_[A-Za-z0-9]{30,}'),
         ('openai-style key',rb'sk-[A-Za-z0-9]{24,}'),
         ('aws key',rb'AKIA[0-9A-Z]{16}'),
         ('slack token',rb'xox[baprs]-[A-Za-z0-9-]{10,}'),
         ('private key',rb'-----BEGIN [A-Z ]*PRIVATE KEY'),
         ('bearer token',rb'(?i)bearer\s+[A-Za-z0-9._\-]{24,}'),
         ('secret assignment',rb'(?i)\b(api[_-]?key|secret|password|access[_-]?token)\b\s*[:=]\s*[^\s"\']{16,}'),
         ('windows user path',rb'[A-Za-z]:[/\\]Users[/\\]')]
# The scanners must contain these shapes to look for them. Exempt by file name,
# because a path moves across a history and a name does not.
SCANNERS={'check_artifact.py','validate_release.py','check_motion_project.py','scan_history.py','test_tools.py'}
# Every commit must be authored by the publishing identity. A stray local identity
# is a real name and a real address, published in 73 places at once.
IDENTITY=re.compile(r'^[0-9]+\+[A-Za-z0-9-]+@users\.noreply\.github\.com$')
# The copyright holder is one published handle and nothing else. No credential
# pattern can catch a person's name, and writing the name here to look for it would
# republish the very thing being removed. The shape is checkable instead: a legal
# name added beside the handle, or in a parenthesis after it, breaks this and
# nothing else does. That is exactly how one leaked, in the two oldest commits,
# through a history rewrite that had cleaned three other files and not this one.
COPYRIGHT=re.compile(rb'^Copyright \(c\) [0-9]{4} [A-Za-z0-9._-]+$')

def git(*args,binary=False):
    r=subprocess.run(['git']+list(args),capture_output=True)
    if binary:return r.returncode,r.stdout
    return r.returncode,(r.stdout or b'').decode('utf-8','replace')

def scan():
    findings=[]
    code,_=git('rev-parse','--git-dir')
    if code!=0:return None
    code,listing=git('rev-list','--objects','--all')
    named=[l.split(' ',1) for l in listing.splitlines() if ' ' in l]
    named=[(s,p) for s,p in named if p.strip()]
    if named:
        request=('\n'.join(s for s,_ in named)+'\n').encode()
        r=subprocess.run(['git','cat-file','--batch'],input=request,capture_output=True)
        out=r.stdout;i=0;index=0
        while i<len(out) and index<len(named):
            end=out.find(b'\n',i)
            if end<0:break
            header=out[i:end].split()
            if len(header)<3:i=end+1;index+=1;continue
            size=int(header[2]);body=out[end+1:end+1+size];path=named[index][1]
            if header[1]==b'blob' and path.rsplit('/',1)[-1] not in SCANNERS:
                for label,pattern in SECRETS:
                    if re.search(pattern,body):
                        findings.append({'kind':label,'path':path,'object':named[index][0][:12]})
                if path.rsplit('/',1)[-1]=='LICENSE':
                    for line in body.splitlines():
                        if line.startswith(b'Copyright') and not COPYRIGHT.match(line.strip()):
                            findings.append({'kind':'copyright naming more than the published handle',
                                             'path':path,'object':named[index][0][:12]})
            i=end+1+size+1;index+=1
    _,people=git('log','--all','--format=%ae%n%ce')
    for address in sorted({a.strip() for a in people.splitlines() if a.strip()}):
        if not IDENTITY.match(address):
            findings.append({'kind':'commit identity that is not the publishing one','path':'(commit metadata)','object':address})
    return findings

def main():
    findings=scan()
    if findings is None:
        print('Not a git repository, so there is no history to scan. This is not a pass.',file=sys.stderr)
        return 2
    print(json.dumps({'findings':findings,'count':len(findings)},indent=2))
    return 1 if findings else 0

if __name__=='__main__':sys.exit(main())
