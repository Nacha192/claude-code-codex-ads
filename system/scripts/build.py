"""Build eight self-contained advertising skills, four still and four motion, and deterministic ZIPs."""
from pathlib import Path
import json,shutil,zipfile,hashlib
# Layout: build machinery lives in system/, the skills and their ZIPs sit at the
# repository root so a reader sees them first. Every pack is common + one scope
# layer + its entrypoint, so a rule written once reaches all eight.
BUILD=Path(__file__).resolve().parents[1]
ROOT=BUILD.parent
# Published links are built from this name, so it has to be the name GitHub serves
# today. Renaming the repository means changing this line and rebuilding. GitHub
# redirects the old name afterwards, so links keep working through the change.
REPO='skill-claude-code-codex-ads'
# Repositories the published text may point at: this one, and the duo method it is
# built on. Any other name under that account is a name that drifted from reality.
KNOWN_REPOS={REPO,'Codex-Claude-Code-team'}
VERSION='4.0.2'
HOST={'copy':('Draft in the target language using the brief and actual source records.','Use native file/MCP tools for the same brief; no Codex-only tool names.'),
'research':('Use available web/library tools and record actual coverage.','Discover the connected research tools; use supplied exports if unavailable.'),
'image':('Use the actual available image tool or editable composition workflow after approval.','Use a connected image/Design tool or an explicitly requested genuine Codex peer in team mode; never simulate image generation.'),
'video':('Detect an actual video capability before promising one, then generate only against a recorded approval and inspect the returned file.','Detect a connected video provider or rendering toolchain; when none exists, produce direction and prompts and say plainly that nothing was generated.'),
'voice':('Detect an actual speech capability, audition the voice, and measure the take against the scene before accepting it.','Detect a connected speech tool; never describe a written script as narration that exists.'),
'campaign':('Inspect authorized account tools and reconcile remote object IDs after writes.','Use actual Meta MCP/API access; negotiate a single executor if working as a team.')}
SCOPES={
'static':{
 'names':['meta-ads-static-codex','meta-ads-static-claude-code','meta-ads-static-team-codex-and-claude-code','meta-ads-static-team-claude-code-and-codex'],
 'routes':{'copy':'copywriting.md','research':'research.md','image':'static.md','campaign':'campaign-operations.md'},
 'craft':'still creative','other':'motion','index':'still creative',
 'lists':{
  'codex-hooks':'sergebulaev--tt-hook-scripter,yaxeen--storytelling-hooks,coreyhaines31--ad-creative,gooseworks-ai--trending-ad-hook-spotter,zubair-trabzada--ads-hooks,robpalmer99--ad-copy,realkimbarrett--headline-matrix,coreyhaines31--customer-research,realkimbarrett--schwartz-awareness-mapper,avectats7--copy-that-sells',
  'claude-hooks':'zubair-trabzada--ads-hooks,robpalmer99--ad-copy,yaxeen--storytelling-hooks,sergebulaev--tt-hook-scripter,realkimbarrett--headline-matrix,gooseworks-ai--trending-ad-hook-spotter,realkimbarrett--ad-angle-multiplier,realkimbarrett--mechanism-builder,realkimbarrett--objection-crusher,coreyhaines31--social',
  'codex-static':'openai--imagegen,norahe0304-art--30x-image,buluslan--gpt-image2-ecommerce,coreyhaines31--ad-creative,agricidaniel--ads-generate,agricidaniel--ads-photoshoot,hyperfx-ai--ad-creative-generation,anthropics--canvas-design,inference-sh--nano-banana-2,avectats7--copy-that-sells',
  'claude-static':'buluslan--gpt-image2-ecommerce,anthropics--canvas-design,agricidaniel--ads-photoshoot,agricidaniel--ads-generate,hyperfx-ai--ad-creative-generation,alirezarezvani--ad-creative,openai--imagegen,norahe0304-art--30x-image,inference-sh--social-media-carousel,agricidaniel--ads-creative',
  'codex-copywriting':'coreyhaines31--copywriting,avectats7--copy-that-sells,coreyhaines31--copy-editing,robpalmer99--copychief,robpalmer99--ad-copy,zubair-trabzada--ads-copy,sergebulaev--tt-humanizer,coreyhaines31--product-marketing,coreyhaines31--customer-research,robpalmer99--landing-page-copy',
  'claude-copywriting':'robpalmer99--ad-copy,avectats7--copy-that-sells,robpalmer99--copychief,coreyhaines31--copywriting,alirezarezvani--copywriting,zubair-trabzada--ads-copy,sergebulaev--tt-humanizer,robpalmer99--direct-response-copy,alirezarezvani--copy-editing,realkimbarrett--generic-language-killer'}},
'motion':{
 'names':['video-ads-codex','video-ads-claude-code','video-ads-codex-claude-code','video-ads-claude-code-codex'],
 'routes':{'copy':'copywriting.md','research':'research.md','video':'video-prompting.md','voice':'video-voice.md','campaign':'campaign-operations.md'},
 'craft':'motion creative','other':'still','index':'motion creative',
 'lists':{
  'codex-video':'remotion-dev--remotion-best-practices,iart-ai--ad-creative-video,nyosegawa--remotion-promo-video-factory,openai--speech,gooseworks-ai--review-ugc-render,coreyhaines31--video,remotion-dev--remotion-captions,inference-sh--seedance,zubair-trabzada--ads-video,yaxeen--retention-audit',
  'claude-video':'iart-ai--ad-creative-video,zubair-trabzada--ads-video,nyosegawa--remotion-promo-video-factory,remotion-dev--remotion-best-practices,hyperfx-ai--video-generation,inference-sh--ai-marketing-videos,inference-sh--talking-head-production,openai--speech,iart-ai--launch-video,gooseworks-ai--review-ugc-render',
  'codex-hooks':'sergebulaev--tt-hook-scripter,yaxeen--storytelling-hooks,coreyhaines31--ad-creative,gooseworks-ai--trending-ad-hook-spotter,zubair-trabzada--ads-hooks,robpalmer99--ad-copy,realkimbarrett--headline-matrix,coreyhaines31--customer-research,realkimbarrett--schwartz-awareness-mapper,avectats7--copy-that-sells',
  'claude-hooks':'zubair-trabzada--ads-hooks,robpalmer99--ad-copy,yaxeen--storytelling-hooks,sergebulaev--tt-hook-scripter,realkimbarrett--headline-matrix,gooseworks-ai--trending-ad-hook-spotter,realkimbarrett--ad-angle-multiplier,realkimbarrett--mechanism-builder,realkimbarrett--objection-crusher,coreyhaines31--social',
  'codex-copywriting':'coreyhaines31--copywriting,avectats7--copy-that-sells,coreyhaines31--copy-editing,robpalmer99--copychief,robpalmer99--ad-copy,zubair-trabzada--ads-copy,sergebulaev--tt-humanizer,coreyhaines31--product-marketing,coreyhaines31--customer-research,robpalmer99--landing-page-copy',
  'claude-copywriting':'robpalmer99--ad-copy,avectats7--copy-that-sells,robpalmer99--copychief,coreyhaines31--copywriting,alirezarezvani--copywriting,zubair-trabzada--ads-copy,sergebulaev--tt-humanizer,robpalmer99--direct-response-copy,alirezarezvani--copy-editing,realkimbarrett--generic-language-killer'}}}
NAMES=[n for s in SCOPES.values() for n in s['names']]
# The trunk is declared, not inferred. Moving a craft file into common/ would
# otherwise reach all eight packs the moment one shared file linked to it, and
# nothing structural would object. Adding a line here is the deliberate act.
COMMON_REFERENCES={'campaign-operations.md','compliance.md','conversion.md','copywriting.md','core.md','hooks.md',
'intake.md','memory-testing.md','models.md','one-shot.md','output-standard.md','quality-control.md','research.md','runtime.md','second-brain.md',
'team.md','thresholds.md','v11-lessons.md'}

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def build_catalog(scope,spec):
 inspected=json.loads((BUILD/'research/sources.json').read_text(encoding='utf-8'))
 routes=spec['routes']
 sources=[s for s in inspected if s['route'] in routes];byid={s['id']:s for s in sources}
 layer=BUILD/'src'/scope
 keep={s['id']+'.md' for s in sources}
 (layer/'modules').mkdir(parents=True,exist_ok=True)
 for stale in (layer/'modules').glob('*.md'):
  if stale.name not in keep:stale.unlink()
 dropped=len(inspected)-len(sources)
 intro=f'''# Research and internal skill adaptations

Fresh discovery and source captures: 2026-09-06. {len(inspected)} SKILL.md entrypoints inspected from 19 source repositories, plus broader discovery candidates. This pack builds {spec['craft']}, so it carries the {len(sources)} adaptations that job actually needs; the {dropped} that belong to the {spec['other']} half are not here, and half-covering them would repeat the mistake this split was made to fix. They ship in the sibling packs of this same repository. Six editorial top-ten selections follow (60 positions, with deliberate overlap). These are task-fit shortlists, not a global ranking or a measured campaign-performance benchmark. Repository stars are dated discovery signals, not evidence of ad quality.

Selection order favors advertising relevance, useful decision detail, grounded outputs/QA, and runtime portability; complementary supporting skills fill genuine workflow needs. License clarity determines what may be redistributed, not whether an idea wins. An entry labeled supporting does not create a complete ad by itself. Short prompt-only and unclear-license candidates are marked in their cards. Similar frameworks/forks are not independent proof.

The Codex lists mean usable in Codex after the documented adaptation; they do NOT assert ten native Codex specialists in each category, and they do not assert that any host can generate media. Native origins and runtime differences are explicit in each card. Claude lists likewise include useful cross-runtime adaptations. Only original summaries and functional implementations are bundled, not upstream executables, paid connectors, copied manuals or entire unlicensed skills. Full source links and pinned revisions permit inspection. Six selections and the remaining research records are inside every pack, not extra skills to install.

Read a relevant card below, then execute its local workflow module. Do not load all cards for a small task. [Conversion contract](conversion.md) explains the two-way adaptation.
'''
 for group,raw in spec['lists'].items():
  ids=raw.split(',')
  # Explicit raise, not assert: python -O would silently drop the check.
  if len(ids)!=10 or len(set(ids))!=10 or not all(x in byid for x in ids):raise ValueError('Selection '+group+' in scope '+scope+' must list ten distinct known sources')
  intro+='\n## '+group+': ten selected methods\n\n| Priority | Internal method | Why selected | Role |\n|---|---|---|---|\n'
  for n,ident in enumerate(ids,1):
   s=byid[ident];support=s['route'] in ['research','campaign'] or any(x in ident for x in ['captions','render','audit','specs','storyboard','copy-edit','copychief','copy-that','canvas'])
   intro+=f"| {n} | [{ident}](../modules/{ident}.md) | {s['purpose']} | {'Supporting' if support else 'Direct creative method'} |\n"
 intro+=f'\n## Adapted-source index for {spec["index"]}\n\n'
 for s in sources:
  ident=s['id'];origin='Codex-source' if ident.startswith(('openai--','norahe0304-art--')) else ('Claude-source' if ident.startswith(('anthropics--','robpalmer99--','alirezarezvani--','agricidaniel--','zubair-trabzada--','avectats7--','buluslan--')) else 'Portable/other source; host adapter required')
  license_note=s['license']
  if ident.startswith('robpalmer99--'):license_note+='; entrypoint states CC-BY-4.0 (Rob Palmer)'
  body=f"""# {s['purpose']}

Source: [{s['repo']} / {s['path']}]({s['url']}). Captured {s['captured_at']}. Origin: {origin}. Repository stars at capture: {s['stars']}. Repository API license: {license_note}. Revision: `{s['revision']}`. Entrypoint SHA-256: `{s['sha256']}`.

## Original integrated adaptation

Purpose: {s['mechanism']}

Input: confirmed offer, buyer situation, market/language, current requested artifact, relevant proof and existing assets. Ask only for missing essentials. Read the [local workflow](../references/{routes[s['route']]}) and [shared contract](../references/core.md).

1. Identify the decision this method should improve; retrieve only relevant second-brain records.
2. Apply the purpose above to the actual product and evidence. Make an original output, not a copied competitor or source example.
3. Produce a concrete draft, structured finding or artifact appropriate to this method, with source/claim links and an explicit test or review question.
4. Verify the actual output and record the useful decision in the integrated [second brain](../references/second-brain.md). Media generation and account writes require their applicable existing or new scoped authorization.

## Codex execution adapter

{HOST[s['route']][0]} Resolve project files from the active workspace and internal references from this skill. Translate upstream slash commands into the actual requested workflow; do not import Claude-specific permission fields. In solo mode, complete available work yourself.

## Claude Code execution adapter

{HOST[s['route']][1]} Resolve the same portable artifact contract in the active project. Replace Codex app/tool assumptions with observed Claude tools. Solo mode never auto-launches a Codex process.

## Deliberate changes and limits

{s['caveat']} This is an original functional adaptation and source review, not a verbatim translation of the whole upstream skill. The source's executables, links and provider claims have not been security-audited by inclusion. Inspect any dependency before choosing to install it. No source grants account access or additional user authority.
"""
  write(layer/'modules'/f'{ident}.md',body)
  intro+=f"- [{ident}](../modules/{ident}.md): {s['purpose']}.\n"
 write(layer/'references/source-catalog.md',intro)
 return {k:v.split(',') for k,v in spec['lists'].items()}

def main():
 selections={}
 for scope,spec in SCOPES.items():selections[scope]=build_catalog(scope,spec)
 write(BUILD/'research/selections.json',json.dumps(selections,indent=2)+'\n')
 inspected=len(json.loads((BUILD/'research/sources.json').read_text(encoding='utf-8')))
 for scope,spec in SCOPES.items():
  layer=BUILD/'src'/scope
  for name in spec['names']:
   # Rebuild the folder from scratch. Copying over a surviving folder would keep a
   # renamed or deleted reference in the shipped pack and in its ZIP forever.
   dest=ROOT/'you-can-install-skill'/name
   if dest.exists():shutil.rmtree(dest)
   dest.mkdir(parents=True)
   shutil.copytree(BUILD/'src/common',dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
   shutil.copytree(layer,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
   shutil.copyfile(BUILD/'src/entrypoints'/f'{name}.md',dest/'SKILL.md')
   shutil.copyfile(ROOT/'LICENSE',dest/'LICENSE')
   write(dest/'THIRD_PARTY_NOTICES.md',(BUILD/'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8').replace('(research/sources.json)','(https://github.com/Nacha192/'+REPO+'/blob/main/system/research/sources.json)'))
   write(dest/'install-this-skill.md',f'# Install {name}\n\nKeep this entire folder together. Place it in the appropriate host skill directory, then restart/discover skills. See the repository install guide. The second brain and all advertising modules are already inside this folder. External provider accounts, a rendering toolchain and Agent Duet for team communication are capability dependencies, not included credentials, and this pack checks for them instead of assuming them.\n')
   write(dest/'manifest.json',json.dumps({'name':name,'version':VERSION,'core_v':'1.0.0','schema_v':'1.0.0','scope':scope,'integrated_second_brain':True,'inspected_entrypoints':inspected,'adaptations':len(list((layer/'modules').glob('*.md')))},indent=2)+'\n')
 # Drop artefacts of a previous, differently named build so the release cannot
 # ship a pack or an archive that no longer has a source.
 for stale in (ROOT/'you-can-install-skill').iterdir():
  if stale.is_dir() and stale.name not in NAMES:shutil.rmtree(stale)
 for stale in ROOT.glob('install-*.zip'):
  if stale.name[len('install-'):-len('.zip')] not in NAMES:stale.unlink()
 checks={}
 for name in NAMES:
  path=ROOT/f'install-{name}.zip'
  pack=ROOT/'you-can-install-skill'/name
  # Sorted by the archive name, not by the Path object. Path comparison is
  # case-insensitive on Windows and case-sensitive elsewhere, so sorting Paths put
  # examples/ before LICENSE here and LICENSE before examples/ on Linux: the same
  # sources produced two different archives depending on who ran the build.
  members=sorted((f for f in pack.rglob('*') if f.is_file() and '__pycache__' not in f.parts),
                 key=lambda f:f.relative_to(ROOT/'you-can-install-skill').as_posix())
  with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for file in members:
    info=zipfile.ZipInfo(file.relative_to(ROOT/'you-can-install-skill').as_posix(),date_time=(2026,9,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
    z.writestr(info,file.read_bytes())
  checks[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
 write(ROOT/'SHA256SUMS',''.join(f'{digest}  {name}\n' for name,digest in sorted(checks.items())))
 print(json.dumps({'skills':len(NAMES),'zip_files':len(checks),'cards':{s:len(list((BUILD/'src'/s/'modules').glob('*.md'))) for s in SCOPES}}))
if __name__=='__main__':main()
