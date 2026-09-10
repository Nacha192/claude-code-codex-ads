import copy,hashlib,importlib.util,io,json,shutil,subprocess,sys,tempfile,unittest,unittest.mock,zipfile
from pathlib import Path
BUILD=Path(__file__).resolve().parents[1]
ROOT=BUILD.parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
checker=load('checker',BUILD/'src/common/scripts/check_artifact.py')
brain=load('brain',BUILD/'src/common/scripts/init_brain.py')
installer=load('installer',BUILD/'install.py')
# The release validator imports build.py by name, so its directory has to be importable.
sys.path.insert(0,str(BUILD/'scripts'))
releaser=load('releaser',BUILD/'scripts/validate_release.py')
motion=load('motion',BUILD/'src/motion/scripts/check_motion_project.py')
inspector=load('inspector',BUILD/'src/motion/scripts/inspect_video.py')
engine=load('engine',BUILD/'src/motion/scripts/motion_engine.py')
renderer=load('renderer',BUILD/'src/motion/scripts/render_motion.py')
EXAMPLE=BUILD/'src/motion/examples/motion-project.example.json'
RENDER_EXAMPLE=BUILD/'src/motion/examples/motion-project.render.json'
FFMPEG=shutil.which('ffmpeg') and shutil.which('ffprobe')
# ffmpeg being on PATH is not the same as ffmpeg being able to draw. Homebrew's
# macOS bottle ships libx264 and aac and no libfreetype, so `drawtext` and
# `subtitles` do not exist and nothing with a word in it can be rendered. The engine
# already refuses that machine by name; these tests have to make the same
# distinction instead of failing on a runner that is behaving exactly as designed.
_CAPS=engine.detect() if FFMPEG else {'usable':False,'reason':'no ffmpeg on PATH'}
RENDERABLE=bool(_CAPS.get('usable'))
WHY_NOT=_CAPS.get('reason','')

class ToolTests(unittest.TestCase):
 def brief(self):return {'schema_v':'1.0.0','kind':'brief','offer':'A fictional repair service','country':'FR','ad_language':'fr-FR','objective':'qualified inquiries','window':{'start':'2026-08-01','end':'2026-08-31'}}
 def creative(self):return {'schema_v':'1.0.0','kind':'creative','hook':'A clearer repair quote','ad_language':'en-GB','cta':'See the process','claims':[{'text':'Written scope included','proof_ids':['E1']}],'evidence':[{'id':'E1','type':'product_observed','source':'synthetic-fixture','supports':'Written scope is included'}]}
 def storyboard(self):return {'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':3,'visual':'product','voice':'demo','measured_voice_seconds':2}]}
 def test_complete_brief(self):self.assertEqual(checker.check(self.brief())[0],[])
 def test_missing_language(self):
  d=self.brief();d['ad_language']=' ';self.assertTrue(checker.check(d)[0])
 def test_reversed_window(self):
  d=self.brief();d['window']['end']='2025-01-01';self.assertTrue(checker.check(d)[0])
 def test_invalid_date(self):
  d=self.brief();d['window']['start']='2026-02-30';self.assertTrue(checker.check(d)[0])
 def test_claim_reference(self):self.assertEqual(checker.check(self.creative())[0],[])
 def test_unknown_proof(self):
  d=self.creative();d['claims'][0]['proof_ids']=['missing'];self.assertTrue(checker.check(d)[0])
 def test_duplicate_evidence(self):
  d=self.creative();d['evidence']*=2;self.assertTrue(checker.check(d)[0])
 def test_hypothesis_not_proof(self):
  d=self.creative();d['evidence'][0]['type']='hypothesis';self.assertTrue(checker.check(d)[0])
 def test_fake_testimonial(self):
  d=self.creative();d['claims'][0]['testimonial']=True;self.assertTrue(checker.check(d)[0])
 def test_unhashable_reference_does_not_crash(self):
  d=self.creative();d['claims'][0]['proof_ids']=[{}];self.assertTrue(checker.check(d)[0])
 def test_missing_evidence_type(self):
  d=self.creative();d['evidence'][0].pop('type');self.assertTrue(checker.check(d)[0])
 def test_quote_requires_text(self):
  for value in [True,1,' ','',{}]:
   d=self.creative();d['claims'][0]['testimonial']=True;d['evidence'][0].update(type='customer_quote',verbatim=value);self.assertTrue(checker.check(d)[0])
 def test_storyboard_measured_overrun(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product','voice':'demo','measured_voice_seconds':3}]};self.assertTrue(checker.check(d)[0])
 def test_nan_and_bool_times(self):
  for value in [float('nan'),True]:
   d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':value,'end':2,'visual':'product'}]};self.assertTrue(checker.check(d)[0])
 def test_unmeasured_voice_warns(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':3,'visual':'product','voice':'demo'}]};e,w=checker.check(d);self.assertFalse(e);self.assertTrue(w)
 def test_timeline_gap_warns(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'a'},{'start':3,'end':5,'visual':'b'}]};e,w=checker.check(d);self.assertFalse(e);self.assertTrue(w)
 def test_empty_voice_value_refused(self):
  for value in [[],'','   ',7]:
   d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product','voice':value}]};self.assertTrue(checker.check(d)[0])
 def test_measured_narration_without_a_line_refused(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product','measured_voice_seconds':1}]};self.assertTrue(checker.check(d)[0])
 def test_storyboard_overlap_is_an_error(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':3,'visual':'a'},{'start':2,'end':5,'visual':'b'}]};self.assertTrue(checker.check(d)[0])
 def generation(self):return {'schema_v':'1.0.0','kind':'generation_request','provider':'a-provider','model':'a-model','account_alias':'studio-main','credits_remaining':400,'items':[{'prompt':'synthetic fixture'}],'approval':{'granted_at':'2026-09-01','provider':'a-provider','model':'a-model','account_alias':'studio-main','max_items':4,'ceiling':'200 credits'}}
 def test_generation_within_approval(self):self.assertEqual(checker.check(self.generation())[0],[])
 def test_generation_needs_recorded_approval(self):
  d=self.generation();d.pop('approval');self.assertTrue(checker.check(d)[0])
 def test_generation_material_change_refused(self):
  for field in ['provider','model','account_alias']:
   d=self.generation();d[field]='changed-after-approval';self.assertTrue(checker.check(d)[0])
 def test_generation_over_approved_ceiling(self):
  d=self.generation();d['items']=[{'prompt':'x'}]*5;self.assertTrue(checker.check(d)[0])
 def test_zero_credits_stops_generation(self):
  d=self.generation();d['credits_remaining']=0;self.assertTrue(checker.check(d)[0])
 def test_unknown_credits_only_warns(self):
  d=self.generation();d['credits_remaining']=None;e,w=checker.check(d);self.assertFalse(e);self.assertTrue(any('credits' in x for x in w))
 def test_future_dated_approval_refused(self):
  d=self.generation();d['approval']['granted_at']='2099-01-01';self.assertTrue(checker.check(d)[0])
 def test_invalid_credit_values(self):
  for value in [True,-1,'many',float('inf')]:
   d=self.generation();d['credits_remaining']=value;self.assertTrue(checker.check(d)[0])
 def test_credentials_refused_in_every_kind(self):
  self.assertEqual(checker.check(self.storyboard())[0],[])
  for fixture in [self.brief,self.creative,self.generation,self.storyboard]:
   d=fixture();d['notes']='authorization: Bearer '+'A'*32;self.assertTrue(checker.check(d)[0])
   # A credential pasted as a field name travels exactly as far as one pasted as a value.
   d=fixture();d['sk-'+'C'*30]='looks harmless';self.assertTrue(checker.check(d)[0])
 def test_credential_nested_in_evidence(self):
  d=self.creative();d['evidence'][0]['source']='api_key='+'B'*24;self.assertTrue(checker.check(d)[0])
 def test_generation_item_must_describe_something(self):
  for value in [None,'','   ',{},[],True,False,0,42]:
   d=self.generation();d['items']=[value];self.assertTrue(checker.check(d)[0],repr(value)+' passed as an item')
 def test_malformed_limits_refused(self):
  for value in [[],'40',20]:
   d=self.creative();d['limits']=value;self.assertTrue(checker.check(d)[0],repr(value)+' passed as limits')
 def test_placement_length_limits(self):
  d=self.creative();d['headline']='x'*41;self.assertTrue(checker.check(d)[0])
  d['headline']='x'*40;self.assertEqual(checker.check(d)[0],[])
  d['limits']={'headline':20};self.assertTrue(checker.check(d)[0])
  d['limits']={'headlines':80};self.assertTrue(checker.check(d)[0])
 def test_red_line_on_rendered_copy(self):
  d=self.creative();d['prohibited_terms']=['cure'];d['primary_text']='This will cure the problem.'
  self.assertTrue(checker.check(d)[0])
  d['primary_text']='Obscure wording is still allowed.';e,w=checker.check(d)
  self.assertEqual(e,[]);self.assertTrue(any('paraphrase' in x for x in w))
 def test_unknown_kind_refused(self):
  d=self.brief();d['kind']='poster';self.assertTrue(checker.check(d)[0])
 def test_brain_preview_and_preserve(self):
  with tempfile.TemporaryDirectory() as t:
   result=brain.initialize(t);self.assertFalse((Path(t)/'.ads-brain').exists())
   brain.initialize(t,True);self.assertEqual((Path(t)/'.ads-brain/.gitignore').read_text(),'*\n');p=Path(t)/'.ads-brain/brand.json';original=p.read_bytes()
   with self.assertRaises(ValueError):brain.initialize(t,True)
   self.assertEqual(p.read_bytes(),original);self.assertEqual(json.loads(original)['status'],'intake_required')
   runtime=json.loads((Path(t)/'.ads-brain/runtime.json').read_text(encoding='utf-8'))
   self.assertEqual(runtime['python']['status'],'unchecked')
 def test_install_preview_idempotence_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   target=Path(t)/'skills';installer.install('codex',target_root=target);self.assertFalse(target.exists())
   installer.install('codex',target_root=target,apply=True)
   plans=installer.install('codex',target_root=target,apply=True);self.assertTrue(all(x['action']=='already-identical' for x in plans))
   file=target/'video-ads-codex/SKILL.md';file.write_text('user edit',encoding='utf-8')
   with self.assertRaises(ValueError):installer.install('codex',target_root=target,apply=True)
   self.assertEqual(file.read_text(),'user edit')
 def test_installer_project_and_modes(self):
  with tempfile.TemporaryDirectory() as t:
   for runtime,mode,scope in [('codex','solo','static'),('claude','team','motion')]:
    plans=installer.install(runtime,mode,project=t,apply=True,scope=scope);self.assertEqual(len(plans),1)
    self.assertTrue((Path(plans[0]['target'])/'SKILL.md').is_file())
 def test_symlinked_ancestor_allowed_but_target_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();alias=root/'alias'
   try:alias.symlink_to(real,target_is_directory=True)
   except OSError as e:self.skipTest('Symlink privilege unavailable: '+str(e))
   installer.install('codex','solo',target_root=alias/'skills',apply=True)
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=alias,apply=True)
 def link_dir(self,link,target):
  """A symlink where that is allowed, a directory junction on Windows. A junction
  needs no privilege, which is why the rule has to hold for it too."""
  try:
   link.symlink_to(target,target_is_directory=True);return True
  except (OSError,NotImplementedError):
   r=subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],capture_output=True)
   return r.returncode==0 and link.exists()
 def test_a_redirected_installation_target_is_refused_including_a_junction(self):
  """`is_symlink()` is False for a Windows junction, so the symlink rule used to be
  walked straight past by the cheaper of the two redirections."""
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();alias=root/'alias'
   if not self.link_dir(alias,real):self.skipTest('no way to make a directory link here')
   self.assertTrue(installer.redirected(alias),'a junction or symlink target must read as redirected')
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=alias,apply=True)
   # An ordinary directory underneath a redirected ancestor stays legitimate.
   installer.install('codex','solo',target_root=alias/'skills',apply=True)
 def test_a_junction_planted_as_a_skill_destination_is_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();skills=root/'skills';skills.mkdir()
   if not self.link_dir(skills/'video-ads-codex',real):self.skipTest('no way to make a directory link here')
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=skills,apply=True,scope='motion')
   self.assertEqual([x for x in real.rglob('*') if x.is_file()],[],'nothing may be written through the link')
 def test_scope_selection(self):
  with tempfile.TemporaryDirectory() as t:
   both=installer.install('codex',target_root=Path(t)/'a');self.assertEqual(len(both),4)
   still=installer.install('codex',target_root=Path(t)/'b',scope='static')
   self.assertTrue(all(x['skill'].startswith('meta-ads-static-') for x in still))
   motion=installer.install('codex',target_root=Path(t)/'c',scope='motion')
   self.assertTrue(all(x['skill'].startswith('video-ads-') for x in motion))
   with self.assertRaises(ValueError):installer.install('codex',scope='nope')
 def test_symlinked_skill_destination_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();target=root/'skills';target.mkdir()
   try:(target/'video-ads-codex').symlink_to(real,target_is_directory=True)
   except OSError as e:self.skipTest('Symlink privilege unavailable: '+str(e))
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=target,apply=True)
 def test_installer_rejects_bad_runtime(self):
  with self.assertRaises(ValueError):installer.install('unknown')
class ReleaseRuleTests(unittest.TestCase):
 """The structural invariants, proved by planting a violation in a throwaway copy.

 Manual proof does not survive a refactor. These fail the day somebody weakens a
 rule, which is the only moment the proof is worth anything."""
 def copy(self):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup);tree=Path(box.name)/'release'
  shutil.copytree(ROOT,tree,ignore=shutil.ignore_patterns('.git','__pycache__'))
  return tree
 def check(self,tree):return releaser.validate(tree,tree/'system',report=False)
 def refused(self,tree,fragment):
  found=self.check(tree)
  self.assertTrue(any(fragment in e for e in found),fragment+' not refused; got '+repr(found[:4]))
 def test_reachability_survives_a_symlinked_ancestor(self):
  """A temporary directory on macOS lives under /var, which is a symlink to
  /private/var. reachable() resolved the link targets and not the pack, so
  relative_to raised and every release rule errored at once. The failure needs a
  redirected ancestor, which is why no local run ever saw it."""
  with tempfile.TemporaryDirectory() as box:
   root=Path(box)/'real';root.mkdir()
   pack=root/'video-ads-codex'
   shutil.copytree(ROOT/'you-can-install-skill/video-ads-codex',pack)
   alias=Path(box)/'alias'
   try:alias.symlink_to(root,target_is_directory=True)
   except (OSError,NotImplementedError):
    r=subprocess.run(['cmd','/c','mklink','/J',str(alias),str(root)],capture_output=True)
    if r.returncode!=0 or not alias.exists():self.skipTest('no way to make a directory link here')
   direct=releaser.reachable(pack)
   through=releaser.reachable(alias/'video-ads-codex')
   self.assertTrue(direct,'the pack must reach something at all')
   self.assertEqual(through,direct,'a redirected ancestor must not change what is reachable')
 def test_the_whole_history_carries_no_secret_and_one_identity(self):
  """validate_release reads the tree that is checked out. A clone carries every
  commit, so a file that was published once and removed later is still published,
  and no rule was looking there. That is how a copyright line naming the author
  survived a history rewrite which had cleaned three other files and not this one."""
  if not (ROOT/'.git').exists():self.skipTest('not a git checkout')
  r=subprocess.run([sys.executable,str(BUILD/'scripts/scan_history.py')],cwd=ROOT,
                   capture_output=True,text=True)
  self.assertEqual(r.returncode,0,'history scan found something: '+(r.stdout or '')+(r.stderr or ''))
 def test_a_clean_copy_of_the_release_passes(self):self.assertEqual(self.check(self.copy()),[])
 def test_source_card_in_the_shared_trunk_refused(self):
  tree=self.copy();(tree/'system/src/common/modules').mkdir(parents=True,exist_ok=True)
  (tree/'system/src/common/modules/planted.md').write_text('planted\n',encoding='utf-8')
  self.refused(tree,'Source card sitting in the shared trunk')
 def test_undeclared_trunk_reference_refused(self):
  tree=self.copy();(tree/'system/src/common/references/planted.md').write_text('planted\n',encoding='utf-8')
  self.refused(tree,'Reference in the trunk that build.py does not declare')
 def test_declared_trunk_reference_removed_refused(self):
  tree=self.copy();(tree/'system/src/common/references/hooks.md').unlink()
  self.refused(tree,'Reference declared for the trunk but absent')
 def test_name_defined_in_trunk_and_layer_refused(self):
  tree=self.copy();shutil.copyfile(tree/'system/src/static/references/scope.md',tree/'system/src/common/references/scope.md')
  self.refused(tree,'Name defined in both the trunk and the static layer')
 def test_reference_no_entrypoint_can_reach_refused(self):
  tree=self.copy();(tree/'system/src/static/references/planted.md').write_text('Nothing links here.\n',encoding='utf-8')
  self.refused(tree,'Unreachable from any static entrypoint')
 def test_source_card_from_the_other_half_refused(self):
  tree=self.copy();sources=json.loads((tree/'system/research/sources.json').read_text(encoding='utf-8'))
  ident=next(s['id'] for s in sources if s['route']=='video')
  (tree/'you-can-install-skill/meta-ads-static-codex/modules'/(ident+'.md')).write_text('planted\n',encoding='utf-8')
  self.refused(tree,'Module from the other half shipped in meta-ads-static-codex')
 def test_script_cited_but_not_shipped_refused(self):
  for cited in ['absent_helper.py','helpers/absent_helper.py']:
   tree=self.copy();page=tree/'you-can-install-skill/video-ads-codex/references/scope.md'
   page.write_text(page.read_text(encoding='utf-8')+'\nRun `scripts/'+cited+'` first.\n',encoding='utf-8')
   self.refused(tree,'Script cited but not shipped in video-ads-codex: '+cited)
 def test_directory_named_like_a_script_is_not_a_script(self):
  tree=self.copy();page=tree/'you-can-install-skill/video-ads-codex/references/scope.md'
  (tree/'you-can-install-skill/video-ads-codex/scripts/pretend.py').mkdir()
  page.write_text(page.read_text(encoding='utf-8')+'\nRun `scripts/pretend.py` first.\n',encoding='utf-8')
  self.refused(tree,'Script cited but not shipped in video-ads-codex: pretend.py')
 def test_credential_in_an_unlisted_file_type_refused(self):
  tree=self.copy();(tree/'notes.txt').write_text('sk-'+'D'*30+'\n',encoding='utf-8')
  self.refused(tree,'Potential private data')
 def test_file_named_like_the_scanner_is_still_scanned(self):
  tree=self.copy();(tree/'check_artifact.py').write_text('KEY="sk-'+'E'*30+'"'+'\n',encoding='utf-8')
  self.refused(tree,'Potential private data')
 def test_unknown_repository_name_refused(self):
  tree=self.copy();page=tree/'README.md'
  page.write_text(page.read_text(encoding='utf-8')+'\nSee https://github.com/Nacha192/a-repo-that-moved.\n',encoding='utf-8')
  self.refused(tree,'Repository name that is not the published one')
 def test_manifest_declaring_the_wrong_scope_refused(self):
  tree=self.copy();manifest=tree/'you-can-install-skill/video-ads-codex/manifest.json'
  data=json.loads(manifest.read_text(encoding='utf-8'));data['scope']='static'
  manifest.write_text(json.dumps(data,indent=2),encoding='utf-8')
  self.refused(tree,'Manifest scope mismatch in video-ads-codex')

class MotionProjectTests(unittest.TestCase):
 """The manifest is the only thing that ties a brief to files on disk, so it is the
 only place a lie about what was produced can be caught offline."""
 def project(self):return json.loads(EXAMPLE.read_text(encoding='utf-8'))
 def refused(self,mutate,fragment):
  d=self.project();mutate(d);e,_=motion.check(d)
  self.assertTrue(any(fragment.lower() in x.lower() for x in e),fragment+' not refused; got '+repr(e[:3]))
 def test_the_shipped_example_is_valid(self):
  e,w=motion.check(self.project());self.assertEqual(e,[])
 def test_claim_without_a_source_refused(self):
  self.refused(lambda d:d['claims'][0].__setitem__('proof_ids',[]),'no proof_ids')
 def test_claim_pointing_at_unknown_evidence_refused(self):
  self.refused(lambda d:d['claims'][0].__setitem__('proof_ids',['nope']),'unknown evidence')
 def test_claim_resting_on_a_hypothesis_refused(self):
  self.refused(lambda d:d['evidence'][0].__setitem__('type','hypothesis'),'hypothesis is not proof')
 def test_requested_format_never_composed_refused(self):
  self.refused(lambda d:d['brief']['formats'].append('16:9'),'no format was composed')
 def test_composed_format_never_exported_refused(self):
  self.refused(lambda d:d['exports'].pop(),'never exported')
 def test_export_without_a_hash_refused(self):
  self.refused(lambda d:d['exports'][0].pop('sha256'),'no sha256')
 def test_dimensions_contradicting_the_ratio_refused(self):
  self.refused(lambda d:d['formats'][0].__setitem__('height',1000),'not 9:16')
 def test_format_without_its_own_composition_refused(self):
  self.refused(lambda d:d['formats'][1].__setitem__('composition','   '),'no composition of its own')
 def test_captions_past_the_timeline_refused(self):
  self.refused(lambda d:d['captions']['cues'][-1].__setitem__('end',95.0),'past the')
 def test_captions_written_from_the_script_refused(self):
  self.refused(lambda d:d['captions'].__setitem__('derived_from','script'),'final_take')
 def test_selected_hook_must_match_the_lock(self):
  self.refused(lambda d:d['creative_lock'].__setitem__('hook','something else'),'does not match')
 def test_choosing_from_fewer_than_three_hooks_refused(self):
  self.refused(lambda d:d.__setitem__('hooks_considered',d['hooks_considered'][:1]),'at least three')
 def test_assumed_engine_refused(self):
  self.refused(lambda d:d['engine'].__setitem__('detected',False),'must be true')
 def test_overlapping_scenes_refused(self):
  self.refused(lambda d:d['scenes'][1].__setitem__('start',1.0),'overlaps')
 def test_narration_longer_than_its_scene_refused(self):
  self.refused(lambda d:d['scenes'][0].__setitem__('measured_voice_seconds',9.0),'exceeds the scene')
 def test_timeline_outside_the_brief_refused(self):
  self.refused(lambda d:d['scenes'][3].__setitem__('end',95.0),'outside the requested')
 def test_loudness_target_without_an_origin_refused(self):
  self.refused(lambda d:d['loudness_target'].pop('source'),'source required')
 def test_identifiable_person_without_a_release_refused(self):
  self.refused(lambda d:d['assets'][0].__setitem__('identifiable_person',True),'no release_ref')
 def test_cloned_voice_without_consent_refused(self):
  self.refused(lambda d:d['voice'].__setitem__('source','cloned'),'consent_ref')
 def test_blocking_defect_left_open_refused(self):
  self.refused(lambda d:d['qa']['technical']['defects'][0].__setitem__('status','open'),'still open')
 def test_failed_creative_verdict_on_an_approved_project_refused(self):
  self.refused(lambda d:d['qa']['creative'].__setitem__('verdict','fail'),'failed and the project claims')
 def test_credential_in_a_value_or_a_key_refused(self):
  self.refused(lambda d:d['brief'].__setitem__('note','api_key: '+'x'*30),'credential-shaped')
  self.refused(lambda d:d.__setitem__('sk-'+'y'*30,'harmless'),'credential-shaped')
 def test_rendered_state_with_no_export_refused(self):
  self.refused(lambda d:d.__setitem__('exports',[]),'no export is listed')
 def test_export_path_that_leaves_the_project_refused(self):
  """A manifest names files inside the job it describes.

  Before this rule an absolute path, or one climbing with "..", was joined to
  --root and read wherever it landed. A manifest written anywhere could point at
  any file on the machine, and if the hash matched, the export check passed while
  nothing produced here had been verified at all.
  """
  self.refused(lambda d:d['exports'][0].__setitem__('path','/etc/hosts'),'absolute')
  self.refused(lambda d:d['exports'][0].__setitem__('path','C:/Windows/win.ini'),'absolute')
  self.refused(lambda d:d['exports'][0].__setitem__('path','../../elsewhere.mp4'),'climbing out')
  self.refused(lambda d:d['assets'][0].__setitem__('path','../../elsewhere.png'),'climbing out')
 def test_a_file_outside_the_root_is_never_hashed_as_an_export(self):
  with tempfile.TemporaryDirectory() as box:
   outside=Path(box)/'outside.bin';outside.write_bytes(b'never part of this job')
   root=Path(box)/'project';root.mkdir()
   d=self.project()
   d['exports']=[dict(d['exports'][0])];d['formats']=[d['formats'][0]]
   d['brief']['formats']=[d['formats'][0]['ratio']];d['exports'][0]['ratio']=d['formats'][0]['ratio']
   d['exports'][0]['path']=outside.as_posix()
   d['exports'][0]['sha256']=hashlib.sha256(outside.read_bytes()).hexdigest()
   e,_=motion.check(d,root)
   self.assertTrue(e,'a correct hash of a file outside the project must not validate it')
   self.assertTrue(any('absolute' in x for x in e),repr(e[:3]))
 def test_a_link_pointing_out_of_the_project_refused(self):
  with tempfile.TemporaryDirectory() as box:
   outside=Path(box)/'outside.bin';outside.write_bytes(b'never part of this job')
   root=Path(box)/'project';root.mkdir()
   d=self.project()
   d['exports']=[dict(d['exports'][0])];d['formats']=[d['formats'][0]]
   d['brief']['formats']=[d['formats'][0]['ratio']];d['exports'][0]['ratio']=d['formats'][0]['ratio']
   # A path can be textually clean and still leave the tree, so the second lock
   # resolves it. Symlink where that is allowed, directory junction on Windows,
   # which needs no privilege and is the form this actually turns up in.
   link=root/'exports'
   try:link.symlink_to(outside.parent,target_is_directory=True)
   except (OSError,NotImplementedError,AttributeError):
    r=subprocess.run(['cmd','/c','mklink','/J',str(link),str(outside.parent)],capture_output=True)
    if r.returncode!=0 or not link.exists():self.skipTest('no way to make a link on this machine')
   d['exports'][0]['path']='exports/outside.bin'
   d['exports'][0]['sha256']=hashlib.sha256(outside.read_bytes()).hexdigest()
   e,_=motion.check(d,root)
   self.assertTrue(any('resolves outside' in x for x in e),'a link out of the tree must be refused; got '+repr(e[:3]))
 def test_a_section_that_is_not_a_list_is_refused_not_iterated(self):
  """A number where a list belongs used to raise TypeError and take the checker
  down. A malformed manifest has to be refused with a message, not a traceback."""
  for field,value in [('assets',5),('exports',5),('claims',{'a':1}),('evidence',7),('assumptions','none')]:
   d=self.project();d[field]=value
   e,_=motion.check(d)
   self.assertTrue(any(field+' must be a list' in x for x in e),field+' -> '+repr(e[:3]))
  d=self.project();d['qa']['technical']['defects']='blocked'
  e,_=motion.check(d)
  self.assertTrue(any('defects must be a list' in x for x in e),repr(e[:3]))
 def test_an_unhashable_asset_reference_does_not_crash(self):
  """A dict or a list in scenes[].assets used to reach a set membership test and
  raise TypeError. Same class of defect as the one already fixed in the artifact
  checker, found here by fuzzing every field with every hostile shape."""
  for bad in [[[]],[{'a':1}],[None],[5]]:
   d=self.project();d['scenes'][0]['assets']=bad
   e,_=motion.check(d)
   self.assertTrue(any('unknown asset' in x for x in e),repr(bad)+' -> '+repr(e[:3]))
 def test_fractional_pixel_dimensions_refused(self):
  self.refused(lambda d:d['formats'][0].__setitem__('width',1080.5),'whole positive pixel counts')
 def test_a_manifest_that_is_not_utf8_exits_cleanly(self):
  """Exit 2 and one line, not a traceback: the caller reads the exit code."""
  with tempfile.TemporaryDirectory() as box:
   bad=Path(box)/'m.json';bad.write_bytes(bytes([255,254,0])+b'binary')
   r=subprocess.run([sys.executable,str(BUILD/'src/motion/scripts/check_motion_project.py'),str(bad)],
                    capture_output=True,text=True)
   self.assertEqual(r.returncode,2)
   self.assertNotIn('Traceback',(r.stdout or '')+(r.stderr or ''))
 def test_hashing_reads_the_file_in_chunks_and_still_agrees(self):
  """Exports are videos. The digest is streamed, so it must match the one-shot
  hash of the same bytes across a file larger than a single chunk."""
  with tempfile.TemporaryDirectory() as box:
   big=Path(box)/'big.bin';payload=(b'motion'*400000)  # about 2.4 MB, several chunks
   big.write_bytes(payload)
   self.assertEqual(motion.digest_of(big),hashlib.sha256(payload).hexdigest())
   self.assertEqual(inspector.digest_of(big),hashlib.sha256(payload).hexdigest())
 def test_a_silent_nonzero_decode_is_still_a_finding(self):
  """ffmpeg failing with an empty stderr used to leave decode_errors at zero and
  produce no finding, which reads exactly like a clean decode."""
  original=inspector.run
  def fake(cmd):
   if cmd[0]=='ffprobe':
    return 0,json.dumps({'format':{'duration':'4.0','size':'1000'},
     'streams':[{'codec_type':'video','width':1080,'height':1920,'avg_frame_rate':'30/1'}]}),''
   if '-f' in cmd and 'null' in cmd and '-vf' not in cmd and '-af' not in cmd:return 137,'',''
   return 0,'',''
  inspector.run=fake
  try:m,findings=inspector.measure(Path('unused.mp4'))
  finally:inspector.run=original
  self.assertTrue(any(f['severity']=='blocking' for f in findings),
                  'a nonzero decode must be reported even when ffmpeg says nothing: '+repr(findings))
 def test_export_file_and_hash_are_checked_against_disk(self):
  with tempfile.TemporaryDirectory() as box:
   root=Path(box);d=self.project()
   e,_=motion.check(d,root)
   self.assertTrue(any('not there' in x for x in e),'a missing export file must be refused')
   for entry in d['exports']:
    p=root/entry['path'];p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(b'not the file that was hashed')
   e,_=motion.check(d,root)
   self.assertTrue(any('hash does not match' in x for x in e),'a wrong hash must be refused')
   for entry in d['exports']:
    entry['sha256']=hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()
   e,_=motion.check(d,root)
   self.assertEqual(e,[])

@unittest.skipUnless(FFMPEG,'ffmpeg and ffprobe are required to measure a real file')
class VideoInspectionTests(unittest.TestCase):
 """Measured against files this test makes, so a passing result means the decoder agreed."""
 @classmethod
 def setUpClass(cls):
  cls.box=tempfile.TemporaryDirectory();cls.dir=Path(cls.box.name)
  cls.good=cls.dir/'good.mp4'
  subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=4',
   '-f','lavfi','-i','sine=frequency=420:duration=4','-c:v','libx264','-pix_fmt','yuv420p',
   '-c:a','aac','-shortest','-y',str(cls.good)],check=True,capture_output=True)
 @classmethod
 def tearDownClass(cls):cls.box.cleanup()
 def measure(self,path):return inspector.measure(Path(path))
 def test_a_real_file_measures_what_it_is(self):
  m,f=self.measure(self.good)
  self.assertEqual(m['ratio'],'9:16');self.assertEqual(m['width'],1080);self.assertEqual(m['height'],1920)
  self.assertAlmostEqual(m['duration_seconds'],4.0,delta=0.2)
  self.assertAlmostEqual(m['fps'],30.0,delta=0.1)
  self.assertEqual(m['audio_streams'],1);self.assertEqual(m['decode_errors'],0)
  self.assertIsNotNone(m['loudness_lufs']);self.assertIsNotNone(m['true_peak_dbfs'])
  self.assertEqual([x for x in f if x['severity']=='blocking'],[])
 def test_a_truncated_file_is_refused_rather_than_measured(self):
  broken=self.dir/'broken.mp4'
  broken.write_bytes(self.good.read_bytes()[:len(self.good.read_bytes())//4])
  m,f=self.measure(broken)
  self.assertTrue([x for x in f if x['severity']=='blocking'],'a file that cannot be decoded must block')
 def test_a_video_opening_on_black_is_blocking(self):
  black=self.dir/'black.mp4'
  subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=black:size=640x360:rate=25:duration=1',
   '-f','lavfi','-i','testsrc2=size=640x360:rate=25:duration=2','-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0',
   '-c:v','libx264','-pix_fmt','yuv420p','-y',str(black)],check=True,capture_output=True)
  m,f=self.measure(black)
  self.assertTrue(any('opens on' in x['observation'] for x in f))
 def test_a_silent_video_is_reported(self):
  silent=self.dir/'silent.mp4'
  subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=640x640:rate=25:duration=2',
   '-c:v','libx264','-pix_fmt','yuv420p','-y',str(silent)],check=True,capture_output=True)
  m,f=self.measure(silent)
  self.assertEqual(m['audio_streams'],0)
  self.assertTrue(any('No audio stream' in x['observation'] for x in f))
 def test_expectations_come_from_arguments_and_are_enforced(self):
  class A:pass
  a=A();a.expect_ratio='16:9';a.expect_width=None;a.expect_height=None
  a.expect_duration=12.0;a.duration_tolerance=0.5;a.expect_fps=None
  a.expect_audio_streams=None;a.expect_sample_rate=None
  a.loudness=None;a.loudness_tolerance=1.5;a.max_true_peak=None;a.captions_end=99.0
  m,_=self.measure(self.good)
  found=inspector.compare(m,a)
  self.assertTrue(any('Ratio is 9:16' in x['observation'] for x in found))
  self.assertTrue(any('Duration is' in x['observation'] for x in found))
  self.assertTrue(any('past the' in x['observation'] for x in found))
 def test_no_expectation_means_no_invented_threshold(self):
  class A:pass
  a=A()
  for field in ['expect_ratio','expect_width','expect_height','expect_duration','expect_fps',
                'expect_audio_streams','expect_sample_rate','loudness','max_true_peak','captions_end']:
   setattr(a,field,None)
  a.duration_tolerance=0.5;a.loudness_tolerance=1.5
  m,_=self.measure(self.good)
  self.assertEqual(inspector.compare(m,a),[],'the inspector must not invent a threshold nobody asked for')
 def test_forward_from_a_minimal_brief_to_inspected_exports(self):
  """The whole contract in one pass: plan, render real files, measure them, inspect, deliver."""
  root=self.dir/'forward';root.mkdir()
  project=json.loads(EXAMPLE.read_text(encoding='utf-8'))
  project['state']='planned';project.pop('exports');project.pop('qa')
  e,_=motion.check(project);self.assertEqual(e,[],'a planned project needs no files')
  exports=[]
  for fmt in project['formats']:
   name='out/ad-%s.mp4'%fmt['ratio'].replace(':','x')
   path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
   subprocess.run(['ffmpeg','-v','error','-f','lavfi',
    '-i','testsrc2=size=%dx%d:rate=%d:duration=20'%(fmt['width'],fmt['height'],fmt['fps']),
    '-f','lavfi','-i','sine=frequency=300:duration=20','-c:v','libx264','-pix_fmt','yuv420p',
    '-c:a','aac','-shortest','-y',str(path)],check=True,capture_output=True)
   m,findings=inspector.measure(path)
   self.assertEqual([x for x in findings if x['severity']=='blocking'],[])
   self.assertEqual(m['ratio'],fmt['ratio'])
   exports.append({'ratio':fmt['ratio'],'path':name,'state':'delivered',
    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'measured':{'duration_seconds':m['duration_seconds'],'width':m['width'],
                'height':m['height'],'fps':m['fps']}})
  project['exports']=exports;project['state']='rendered'
  e,_=motion.check(project,root);self.assertEqual(e,[])
  project['state']='inspected'
  e,_=motion.check(project,root)
  self.assertTrue(any('qa object required' in x for x in e),'inspected without a QA block must fail')
  project['qa']={'technical':{'verdict':'pass','defects':[]},
                 'creative':{'verdict':'pass','reviewed_by':'the side that did not build it','defects':[]}}
  project['state']='delivered'
  e,w=motion.check(project,root)
  self.assertEqual(e,[],'a complete forward run must validate')

class BuildDeterminismTests(unittest.TestCase):
 def build(self):
  run=subprocess.run([sys.executable,str(BUILD/'scripts/build.py')],cwd=ROOT,capture_output=True,text=True)
  self.assertEqual(run.returncode,0,run.stderr)
  return ((ROOT/'SHA256SUMS').read_bytes(),
          {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('install-*.zip'))})
 def test_building_twice_produces_the_same_bytes(self):
  """A build that differs run to run makes every checksum in the release meaningless.

  Compared between two builds in the same environment, which is the claim that
  holds everywhere. It is deliberately not compared against the committed archives:
  DEFLATE output is a property of the zlib the interpreter was linked against, so
  byte equality across machines is not something this repository can promise, and
  the workflow already says so. What must be true everywhere is that the archives
  carry exactly the committed packs, and that is checked by content just below and
  file by file in validate_release.
  """
  first=self.build();second=self.build()
  self.assertEqual(second[0],first[0],'SHA256SUMS changed on a rebuild of unchanged sources')
  self.assertEqual(second[1],first[1],'archive bytes changed on a rebuild of unchanged sources')
 def test_each_archive_carries_exactly_the_committed_pack(self):
  """Portable where byte equality is not: the same names and the same contents."""
  for pack in sorted((ROOT/'you-can-install-skill').iterdir()):
   if not pack.is_dir():continue
   expected={f.relative_to(ROOT/'you-can-install-skill').as_posix():f.read_bytes()
             for f in pack.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
   with zipfile.ZipFile(ROOT/('install-'+pack.name+'.zip')) as z:
    self.assertEqual({i.filename:z.read(i.filename) for i in z.infolist()},expected,pack.name)
 def test_archive_order_does_not_depend_on_the_operating_system(self):
  """Path objects compare case-insensitively on Windows and case-sensitively
  everywhere else, so sorting them wrote LICENSE and examples/ in one order here
  and the opposite order on Linux. Same sources, two different archives, two
  different checksums, and a CI failure that reads like a stale build."""
  for pack in sorted(ROOT.glob('install-*.zip')):
   with zipfile.ZipFile(pack) as z:
    names=z.namelist()
    self.assertEqual(names,sorted(names),pack.name+' is not ordered by its archive names')
 def test_no_cache_or_temporary_file_ships(self):
  bad=[]
  for pack in sorted((ROOT/'you-can-install-skill').iterdir()):
   if not pack.is_dir():continue
   for f in pack.rglob('*'):
    rel=f.relative_to(pack).as_posix()
    if '__pycache__' in f.parts or f.suffix in ('.pyc','.tmp','.log','.bak') or rel.startswith('.'):
     bad.append(pack.name+'/'+rel)
  self.assertEqual(bad,[],'cache or temporary files in the published packs')


class SetupCheckTests(unittest.TestCase):
 """The first-run check: what this machine can do, before the job rather than during."""
 def pack(self,name):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  root=Path(box.name)
  shutil.copytree(ROOT/'you-can-install-skill'/name/'scripts',root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  return root
 def run_check(self,root,extra=None):
  r=subprocess.run([sys.executable,'scripts/check_setup.py','--json']+(extra or []),
                   cwd=str(root),capture_output=True,text=True)
  return r,json.loads(r.stdout)
 def test_a_still_pack_is_not_asked_for_a_renderer_it_does_not_use(self):
  root=self.pack('meta-ads-static-codex')
  r,data=self.run_check(root)
  self.assertEqual(r.returncode,0,r.stdout+r.stderr)
  self.assertEqual(data['render']['status'],'not_needed')
  self.assertEqual(data['verdict'],'ready')
 def test_a_video_pack_reports_the_renderer_it_actually_found(self):
  root=self.pack('video-ads-codex')
  _r,data=self.run_check(root)
  self.assertIn(data['render']['status'],('ok','missing'))
  if data['render']['status']=='ok':
   self.assertTrue(data['render']['ffmpeg'])
   self.assertTrue(data['render']['freetype'])
   self.assertEqual(data['render']['missing_filters'],[])
   self.assertEqual(data['verdict'],'ready')
  else:
   self.assertTrue(data['render'].get('why'),'it called it missing and did not say why')
   self.assertIn('ffmpeg',data['install'],'it named a gap and no way to close it')
 def test_what_no_script_can_see_is_listed_rather_than_guessed(self):
  """A script sees a binary on PATH. It does not see whether an account has credits
  or a connector is authorised, and inventing an answer there is how a pack promises
  a capability it does not have."""
  root=self.pack('video-ads-codex')
  _r,data=self.run_check(root)
  names={item['name'] for item in data['cannot_be_checked_from_a_script']}
  for expected in ('Image generation','Speech provider','Video model',
                   'Meta Ad Library','Meta Marketing API or MCP'):
   self.assertIn(expected,names)
  for item in data['cannot_be_checked_from_a_script']:
   self.assertTrue(item['why'].strip());self.assertTrue(item['how'].strip())
 def test_it_installs_nothing_on_its_own(self):
  """It prints the command. Installing software changes the user's machine and a
  skill has no standing authorization to do that."""
  source=(BUILD/'src/common/scripts/check_setup.py').read_text(encoding='utf-8')
  for forbidden in ('subprocess.run([\'winget','subprocess.run([\'brew',
                    'subprocess.run([\'apt','os.system(','check_call('):
   self.assertNotIn(forbidden,source,'it runs an installer itself: '+forbidden)
  calls=[l for l in source.splitlines() if 'subprocess.run' in l]
  self.assertEqual(len(calls),1,'the only shell it runs is the ffmpeg version probe')
  self.assertIn('-version',source)
 def test_a_machine_that_cannot_draw_is_reported_with_the_command_that_fixes_it(self):
  """The macOS case: libx264 and aac present, libfreetype absent, so every encode
  succeeds and no character can be put on screen."""
  root=self.pack('video-ads-codex')
  spec=importlib.util.spec_from_file_location('setup_probe',root/'scripts/check_setup.py')
  mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  crippled={'ffmpeg':'/opt/homebrew/bin/ffmpeg','ffprobe':'/opt/homebrew/bin/ffprobe',
            'freetype':False,'missing_filters':['drawtext','subtitles'],'fonts':370,
            'font_file':'/System/Library/Fonts/Helvetica.ttc','usable':False,
            'encoders':{'libx264':True,'aac':True},
            'reason':'missing filters: drawtext, subtitles; ffmpeg built without '
                     'libfreetype, so no text can be drawn'}
  fake=type('M',(),{'detect':staticmethod(lambda:crippled)})
  with unittest.mock.patch.object(mod,'engine_module',return_value=fake):
   data=mod.report()
  self.assertEqual(data['render']['status'],'missing')
  self.assertIn('libfreetype',data['render']['why'])
  self.assertIn('ffmpeg',data['missing'])
  self.assertIn('ffmpeg',data['install'])
  self.assertTrue(data['install']['ffmpeg']['command'])
  self.assertIn('libfreetype',data['install']['ffmpeg']['note'])
  self.assertEqual(data['verdict'],'partial',
                   'a missing renderer is not a blocked project: the copy still gets written')
  text=mod.human(data)
  self.assertIn('MISSING',text)
  self.assertIn('Ask before running',text)
 def test_the_report_can_be_written_where_the_next_session_will_find_it(self):
  root=self.pack('video-ads-codex')
  r,_d=self.run_check(root,['--write','.ads-brain/setup.json'])
  written=root/'.ads-brain/setup.json'
  self.assertTrue(written.is_file(),r.stdout+r.stderr)
  self.assertEqual(json.loads(written.read_text(encoding='utf-8'))['schema_v'],'1.0.0')
 def test_every_pack_ships_it_and_every_entrypoint_says_to_run_it(self):
  for name in sorted(p.name for p in (ROOT/'you-can-install-skill').iterdir() if p.is_dir()):
   script=ROOT/'you-can-install-skill'/name/'scripts/check_setup.py'
   self.assertTrue(script.is_file(),name+' ships no setup check')
   entry=(ROOT/'you-can-install-skill'/name/'SKILL.md').read_text(encoding='utf-8')
   self.assertIn('scripts/check_setup.py',entry,name+' never tells anyone to run it')


class MotionEngineTests(unittest.TestCase):
 """The engine's decisions, checked without rendering anything: what it would draw."""
 def manifest(self):return json.loads(RENDER_EXAMPLE.read_text(encoding='utf-8'))
 def design(self):return engine.resolve_design(self.manifest())
 def fmt(self,ratio):
  return next(f for f in self.manifest()['formats'] if f['ratio']==ratio)
 def layouts(self):
  d=self.design();m=self.manifest()
  return {f['ratio']:engine.fit_layout(engine.layout_for(f,d),d,m['scenes']) for f in m['formats']}
 @unittest.skipUnless(RENDERABLE,'this ffmpeg cannot draw: '+WHY_NOT)
 def test_the_leading_the_layout_measures_is_the_leading_that_gets_drawn(self):
  """Measured off the pixels, because the layout cannot know the font's glyph box.

  `drawtext` leads multi-line text at the font's own maximum glyph height plus
  `line_spacing`. That measured 2.50 em here where the layout had assumed 1.25, so a
  wrapped block was twice the height it had been measured at and the copy underneath
  was written over. Every line is drawn on its own now, at a y the engine computes."""
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  work=Path(box.name);font=engine.detect()['font_file']
  W,H=1400,1100
  for leading in (1.15,1.25,1.6):
   design=copy.deepcopy(self.design());design['type']['leading']=leading
   layout=engine.fit_layout(engine.layout_for(self.fmt('9:16'),design),
                            design,self.manifest()['scenes'],font)
   layout=dict(layout,width=W,height=H,text_x=40,text_width=W-80)
   size=90
   chains=[];last='bg'
   engine.text_chain({'kind':'text','role':'body','content':'Ag Ag Ag Ag Ag Ag Ag Ag Ag Ag Ag Ag',
                      'at':0,'enter':'fade','colour':'0xFFFFFF','size_px':size,'y':0.08},
                     layout,design,font,work,'t%d'%int(leading*100),1.0,chains,last)
   graph=';'.join(['[0:v]format=rgba,fps=25[bg]']+chains)
   out=chains[-1].rsplit('[',1)[1].rstrip(']')
   p=subprocess.run(['ffmpeg','-hide_banner','-v','error','-f','lavfi','-i',
                     'color=c=black:s=%dx%d:d=1:r=25'%(W,H),'-filter_complex',graph,
                     '-map','[%s]'%out,'-frames:v','25','-pix_fmt','gray','-f','rawvideo','-'],
                    capture_output=True)
   # The last frame, not the first: every entrance animates alpha from zero, so the
   # frame at t=0 is a correct layout drawn completely transparent.
   raw=p.stdout[-W*H:]
   self.assertGreaterEqual(len(raw),W*H,(p.stderr or b'').decode('utf-8','replace')[-400:])
   bands=[];start=None
   for y in range(H):
    lit=max(raw[y*W:(y+1)*W])>40
    if lit and start is None:start=y
    if not lit and start is not None:bands.append(start);start=None
   self.assertGreaterEqual(len(bands),2,'the copy did not wrap at leading %.2f'%leading)
   drawn=bands[1]-bands[0]
   want=int(size*leading)
   self.assertAlmostEqual(drawn,want,delta=4,
                          msg='leading %.2f drew %d px where the layout measured %d'
                              %(leading,drawn,want))
 def test_a_leading_the_manifest_did_not_set_falls_back_rather_than_crashing(self):
  self.assertEqual(engine.leading_of({}),engine.LEADING)
  self.assertEqual(engine.leading_of({'type':{}}),engine.LEADING)
  self.assertEqual(engine.leading_of({'type':{'leading':'gros'}}),engine.LEADING)
  self.assertEqual(engine.leading_of({'type':{'leading':40}}),engine.LEADING)
  self.assertEqual(engine.leading_of({'type':{'leading':1.4}}),1.4)
 def test_the_captions_take_their_colours_from_the_palette(self):
  """They were the one part of the film that ignored the brand: a white fill and a
  hard-coded navy outline, whatever the palette said."""
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  design={'palette':{'ink':'0x1B1B1B','paper':'0xF4F0E8','accent':'0x6E1A24'},
          'type':{'scale':{'caption':0.03}},'motion':{},'grid':{}}
  layout={'width':1080,'height':1920,'sizes':{'caption':40},'safe_bottom':300,
          'margin':90,'margin_right':90}
  path=Path(box.name)/'c.ass'
  engine.write_ass([{'start':0,'end':1,'text':'ok'}],layout,design,'Inter',path,
                   {'colour':'ink','outline':'paper'})
  style=[l for l in path.read_text(encoding='utf-8').splitlines() if l.startswith('Style:')][0]
  self.assertIn('&H001B1B1B',style)   # ink, as BGR
  self.assertIn('&H00E8F0F4',style)   # paper, as BGR
  engine.write_ass([{'start':0,'end':1,'text':'ok'}],layout,design,'Inter',path)
  style=[l for l in path.read_text(encoding='utf-8').splitlines() if l.startswith('Style:')][0]
  self.assertIn('&H00E8F0F4',style,'the default fill should still be the paper colour')
 def test_a_softened_plane_says_so_in_the_filter_graph(self):
  """Depth, such as it is: a plane behind the subject is blurred so the eye is told
  where to look. Sigma is a fraction of the frame height, not a pixel count, so one
  manifest reads the same at 1080 and at 1920."""
  layout=engine.fit_layout(engine.layout_for(self.fmt('9:16'),self.design()),
                           self.design(),self.manifest()['scenes'])
  chains=[]
  engine.media_layer(1,{'kind':'video','asset':'a','blur':0.01},layout,3.0,30,chains,'bg',{})
  self.assertTrue(any('gblur=sigma=' in c for c in chains),chains)
  sigma=float([c for c in chains if 'gblur' in c][0].split('gblur=sigma=')[1].split(',')[0].split('[')[0])
  self.assertAlmostEqual(sigma,0.01*layout['height'],delta=0.5)
  sharp=[]
  engine.media_layer(1,{'kind':'video','asset':'a'},layout,3.0,30,sharp,'bg',{})
  self.assertFalse(any('gblur' in c for c in sharp),'it blurred a plane nobody asked to blur')
 def test_the_reference_engine_never_requires_javascript(self):
  """The pack may not smuggle in a toolchain nobody agreed to install."""
  caps=engine.detect()
  self.assertFalse(caps['javascript_required'])
  self.assertEqual(caps['engine'],'ffmpeg-python-reference')
  source=(BUILD/'src/motion/scripts/motion_engine.py').read_text(encoding='utf-8')
  for word in ['npm ','npx ','node_modules','require(','yarn ']:
   self.assertNotIn(word,source,'the reference engine reached for '+word.strip())
 def test_detection_names_what_is_missing_rather_than_failing_late(self):
  caps=engine.detect()
  self.assertIn('missing_filters',caps);self.assertIn('usable',caps)
  if not caps['usable']:self.assertTrue(caps.get('reason'),'unusable without saying why')
 @unittest.skipUnless(RENDERABLE,'this ffmpeg cannot draw: '+WHY_NOT)
 def test_a_complete_build_reports_nothing_missing(self):
  caps=engine.detect()
  self.assertEqual(caps['missing_filters'],[])
  self.assertTrue(caps['freetype'])
  self.assertIsNotNone(caps['font_file'])
 def test_an_ffmpeg_that_cannot_draw_is_named_rather_than_used(self):
  """Homebrew's macOS ffmpeg has x264 and aac and no libfreetype, so it encodes
  perfectly and cannot put one character on screen. Detection has to say so, and the
  run has to stop, because the alternative is an ad delivered with no words in it."""
  caps=engine.detect()
  if caps['usable']:
   caps=dict(caps,missing_filters=['drawtext','subtitles'],freetype=False,usable=False)
   caps['reason']='missing filters: drawtext, subtitles; ffmpeg built without libfreetype, so no text can be drawn'
  self.assertFalse(caps['usable'])
  self.assertTrue(caps['reason'])
  self.assertIn('drawtext' if caps['missing_filters'] else 'ffmpeg',caps['reason'])
 def test_brand_tokens_replace_the_defaults(self):
  m=self.manifest();m.setdefault('design',{}).setdefault('palette',{})['accent']='0x00FF00'
  d=engine.resolve_design(m)
  self.assertEqual(engine.colour(d,'accent'),'0x00FF00')
  self.assertEqual(engine.colour(d,'not-a-token','0x123456'),'0x123456')
 def test_the_three_ratios_are_three_compositions_and_not_one_crop(self):
  """A crop shares its arrangement. These must not: different media rectangle,
  different type column, different stacking, sized from each frame."""
  l=self.layouts()
  self.assertEqual(l['9:16']['shape'],'portrait')
  self.assertEqual(l['4:5']['shape'],'square')
  self.assertEqual(l['16:9']['shape'],'landscape')
  # Portrait and square put the picture across the top; landscape gives it a column.
  for ratio in ('9:16','4:5'):
   self.assertEqual(l[ratio]['media']['x'],0)
   self.assertEqual(l[ratio]['media']['w'],l[ratio]['width'])
   self.assertLess(l[ratio]['media']['h'],l[ratio]['height'])
  self.assertGreater(l['16:9']['media']['x'],0)
  self.assertEqual(l['16:9']['media']['h'],l['16:9']['height'])
  self.assertLess(l['16:9']['text_width'],l['16:9']['width']*0.5)
  # Nothing is shared by all three, which is what a crop would produce.
  self.assertEqual(len({(l[r]['text_top'],l[r]['text_width'],l[r]['media']['w']) for r in l}),3)
 def test_type_is_sized_from_the_frame_not_copied_between_frames(self):
  l=self.layouts()
  self.assertNotEqual(l['9:16']['sizes']['display'],l['4:5']['sizes']['display'])
  for ratio,lay in l.items():
   self.assertGreater(lay['sizes']['display'],lay['sizes']['title'])
   self.assertGreater(lay['sizes']['title'],lay['sizes']['body'])
 def test_the_stack_is_measured_before_it_is_placed(self):
  """Every block below the one before it, none inside the caption band."""
  d=self.design();m=self.manifest()
  for ratio,lay in self.layouts().items():
   for scene in m['scenes']:
    placed=engine.place_stack(scene,lay,d)
    bottom=lay['text_top']
    for n in sorted(placed):
     item=placed[n]
     self.assertGreaterEqual(item['y'],bottom,'%s %s overlaps the block above'%(ratio,scene['id']))
     bottom=item['y']+item['height']
    self.assertLessEqual(bottom,lay['copy_bottom'],'%s %s runs into the caption band'%(ratio,scene['id']))
 def test_a_rule_declared_between_two_lines_lands_between_them(self):
  d=self.design();lay=self.layouts()['9:16']
  scene={'id':'t','start':0,'end':3,'layers':[
   {'kind':'text','role':'title','content':'Above'},
   {'kind':'shape','h':0.006},
   {'kind':'text','role':'body','content':'Below'}]}
  p=engine.place_stack(scene,lay,d)
  self.assertLess(p[0]['y'],p[1]['y']);self.assertLess(p[1]['y'],p[2]['y'])
 def test_the_type_shrinks_until_the_tallest_scene_fits(self):
  d=self.design();lay=engine.layout_for(self.fmt('9:16'),d)
  crowded=[{'id':'x','start':0,'end':3,'layers':[
   {'kind':'text','role':'display','content':'A headline that will not fit'},
   {'kind':'text','role':'title','content':'And a second line under it'},
   {'kind':'text','role':'body','content':'And a third that makes the column overflow entirely'}]}]
  fitted=engine.fit_layout(lay,d,crowded)
  self.assertLess(fitted['fit_scale'],1.0)
  self.assertLess(fitted['sizes']['display'],lay['sizes']['display'])
  _items,total=engine.stack_items(crowded[0],fitted,fitted['sizes'],d)
  self.assertLessEqual(total,fitted['copy_bottom']-fitted['text_top'])
 def test_copy_that_cannot_fit_is_refused_rather_than_hidden(self):
  d=self.design();lay=engine.layout_for(self.fmt('9:16'),d)
  wall=[{'id':'x','start':0,'end':3,'layers':[
   {'kind':'text','role':'display','content':' '.join(['mot']*400)}]}]
  with self.assertRaises(engine.EngineError):engine.fit_layout(lay,d,wall)
 def test_captions_never_shrink_with_the_copy(self):
  d=self.design();lay=engine.layout_for(self.fmt('9:16'),d)
  crowded=[{'id':'x','start':0,'end':3,'layers':[
   {'kind':'text','role':'display','content':'A headline long enough to force a fit'},
   {'kind':'text','role':'title','content':'A second line under it as well'},
   {'kind':'text','role':'body','content':'A third line so the column has to give way'}]}]
  fitted=engine.fit_layout(lay,d,crowded)
  self.assertLess(fitted['fit_scale'],1.0)
  self.assertEqual(fitted['sizes']['caption'],lay['sizes']['caption'])
 def test_wrapping_keeps_every_word_and_every_line_inside_the_column(self):
  text='Un entretien de chaudiere a prix fixe pour appartement, reservable en ligne'
  wrapped=engine.wrap_text(text,600,48)
  self.assertEqual(wrapped.replace('\n',' ').split(),text.split())
  for line in wrapped.split('\n'):
   self.assertLessEqual(len(line)*48*0.52,600+48*0.52)
 def test_a_single_word_longer_than_the_column_still_comes_back(self):
  self.assertEqual(engine.wrap_text('anticonstitutionnellement',10,90),'anticonstitutionnellement')
 def test_filter_paths_and_expressions_are_escaped_for_ffmpeg(self):
  self.assertEqual(engine.filter_path('C:'+chr(92)+'a'+chr(92)+'b.ttf'),'C'+chr(92)+':/a/b.ttf')
  self.assertNotIn(chr(92)+'a',engine.filter_path('C:'+chr(92)+'a'+chr(92)+'b.ttf'))
  self.assertNotIn(',',engine.expr('min(1,max(0,t))').replace(chr(92)+',',''))
 def test_text_goes_to_a_file_so_nothing_has_to_be_escaped(self):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  awkward="Prix : 19,90 EUR (offre 'lancement') 100% = "+chr(92)+"n"
  path=engine.text_file(Path(box.name),'k',awkward)
  self.assertEqual(Path(path).read_text(encoding='utf-8'),awkward)
 def test_one_frame_count_answers_the_renderer_and_the_resume_check(self):
  """Computed twice from the same floats these disagreed by a frame, and a resume
  then rebuilt clips it already had."""
  self.assertEqual(engine.scene_frames(3.2+0.35,30),engine.scene_frames(round(3.55,3),30))
  self.assertEqual(engine.scene_frames(3.2,30),96)
  self.assertEqual(engine.scene_frames(16.0,30),480)
 def test_a_transition_borrows_from_the_scene_before_it(self):
  scenes=[{'id':'a','start':0,'end':3},{'id':'b','start':3,'end':6,'transition':'dissolve','transition_seconds':0.4},
          {'id':'c','start':6,'end':9,'transition':'cut'}]
  self.assertAlmostEqual(engine.transition_tail(scenes,0),0.4)
  self.assertAlmostEqual(engine.transition_tail(scenes,1),0.0)
  self.assertAlmostEqual(engine.transition_tail(scenes,2),0.0)
 def test_camera_moves_are_bounded_expressions(self):
  self.assertIn('min(',engine.camera_zoom('push',0.1,120))
  self.assertIn('max(',engine.camera_zoom('pull',0.1,120))
  self.assertEqual(engine.camera_zoom('none',0.1,120),'1')
 def test_easings_are_clamped_at_both_ends(self):
  for name in engine.EASINGS:
   e=engine.eased(1.0,0.5,name)
   self.assertIn('min(1',e);self.assertIn('max(0',e)

 def render_project(self):return json.loads(RENDER_EXAMPLE.read_text(encoding='utf-8'))
 def test_the_shipped_render_example_validates_on_its_own(self):
  e,w=motion.check(self.render_project());self.assertEqual(e,[]);self.assertEqual(w,[])
 def test_a_layer_the_engine_cannot_draw_is_refused_before_rendering(self):
  d=self.render_project();d['scenes'][0]['layers'][0]['kind']='hologram'
  self.assertTrue(any('hologram' in x for x in motion.check(d)[0]))
 def test_a_picture_layer_must_name_an_asset_that_exists(self):
  for ref in ['not-an-asset',None,7,[]]:
   d=self.render_project()
   layer=next(l for s in d['scenes'] for l in s['layers'] if l['kind'] in ('image','video'))
   layer['asset']=ref
   self.assertTrue(motion.check(d)[0],repr(ref))
 def test_a_text_layer_with_nothing_to_say_is_refused(self):
  for content in ['','   ',None,5]:
   d=self.render_project()
   layer=next(l for s in d['scenes'] for l in s['layers'] if l['kind']=='text')
   layer['content']=content
   self.assertTrue(motion.check(d)[0],repr(content))
 def test_a_pixel_value_in_a_fraction_field_is_refused(self):
  # 0.075 of the frame and 75 pixels look alike in a manifest and not on screen.
  for value in [75,-0.1,1.5,'0.5',True,float('nan')]:
   d=self.render_project()
   layer=next(l for s in d['scenes'] for l in s['layers'] if l['kind']=='shape')
   layer['w']=value
   self.assertTrue(motion.check(d)[0],repr(value))
 def test_a_layer_cannot_start_after_its_own_scene_ends(self):
  d=self.render_project();scene=d['scenes'][0]
  scene['layers'][-1]['at']=float(scene['end'])-float(scene['start'])+1
  self.assertTrue(any('after its own scene' in x for x in motion.check(d)[0]))
 def test_layers_must_be_a_list(self):
  for value in [{},'text',3]:
   d=self.render_project();d['scenes'][0]['layers']=value
   self.assertTrue(motion.check(d)[0],repr(value))

 def test_each_ratio_keeps_its_own_reserve_for_the_platform(self):
  """A vertical loses a fifth of its height to the interface and a feed square loses
  almost none. The manifest has always declared this per format; reading only the
  project grid applied the strictest ratio's reserve to all three."""
  d=self.design();m=self.manifest()
  lays={f['ratio']:engine.layout_for(f,d) for f in m['formats']}
  for ratio,lay in lays.items():
   zones=next(f['safe_zones'] for f in m['formats'] if f['ratio']==ratio)
   self.assertEqual(lay['safe_bottom'],int(lay['height']*zones['bottom']),ratio)
   self.assertEqual(lay['safe_top'],int(lay['height']*zones['top']),ratio)
   self.assertEqual(lay['margin'],int(lay['width']*zones['left']),ratio)
   self.assertEqual(lay['margin_right'],int(lay['width']*zones['right']),ratio)
  # Expressed as a fraction so the three are compared rather than their pixel counts.
  reserved={r:round(l['safe_bottom']/l['height'],3) for r,l in lays.items()}
  self.assertEqual(len(set(reserved.values())),3,reserved)
  self.assertGreater(reserved['9:16'],reserved['16:9'])
 def test_a_format_with_no_safe_zones_falls_back_to_the_project_grid(self):
  d=self.design();fmt=dict(self.fmt('9:16'));fmt.pop('safe_zones',None)
  lay=engine.layout_for(fmt,d)
  self.assertEqual(lay['safe_bottom'],int(1920*float(d['grid']['safe_bottom'])))
  self.assertEqual(lay['safe_top'],int(1920*float(d['grid']['safe_top'])))
 def test_a_thinner_reserve_than_the_documented_one_warns(self):
  d=self.render_project()
  d['formats'][0]['safe_zones']['bottom']=0.05
  e,w=motion.check(d)
  self.assertEqual(e,[])
  self.assertTrue(any('thresholds.md' in x for x in w))
 def test_a_reserve_given_in_pixels_is_refused(self):
  for value in [200,1.5,-0.1,'0.2',True]:
   d=self.render_project();d['formats'][0]['safe_zones']['bottom']=value
   self.assertTrue(motion.check(d)[0],repr(value))
 def test_copy_the_viewer_cannot_read_is_refused(self):
  """Contrast is the part of legibility that is arithmetic, so it is checked rather
  than left to whoever looks at the export."""
  d=self.render_project()
  scene=next(s for s in d['scenes']
             if not any(l['kind'] in ('image','video') for l in s['layers']))
  for l in scene['layers']:
   if l['kind']=='text':l['colour']='support'
  e,_w=motion.check(d)
  self.assertTrue(any('decoration' in x for x in e),e)
 def test_contrast_is_not_guessed_over_a_picture(self):
  """A number invented from a token that was never on screen is worse than none."""
  d=self.render_project()
  scene=next(s for s in d['scenes'] if any(l['kind'] in ('image','video') for l in s['layers']))
  for l in scene['layers']:
   if l['kind']=='text':l['colour']='support'
  self.assertFalse([x for x in motion.check(d)[0] if 'decoration' in x])
 def test_a_caption_gone_before_it_is_read_is_refused(self):
  d=self.render_project();cue=d['captions']['cues'][0]
  cue['end']=cue['start']+0.3
  self.assertTrue(any('before it is read' in x for x in motion.check(d)[0]))
 def test_a_caption_that_is_a_sentence_warns(self):
  d=self.render_project()
  d['captions']['cues'][0]['text']='Un entretien de chaudiere a prix fixe pour appartement reservable en ligne'
  e,w=motion.check(d)
  self.assertEqual(e,[])
  self.assertTrue(any('two to four words' in x for x in w))
 def test_a_first_second_with_nothing_readable_warns(self):
  d=self.render_project()
  for l in d['scenes'][0]['layers']:
   if l['kind']=='text':l['at']=2.5
  e,w=motion.check(d)
  self.assertEqual(e,[])
  self.assertTrue(any('first' in x and 'muted' in x for x in w))
 def test_the_contrast_maths_is_the_documented_one(self):
  """Anchored on the WCAG worked values, so a refactor cannot quietly change it."""
  white,black=motion.rgb('0xFFFFFF'),motion.rgb('0x000000')
  self.assertAlmostEqual(motion.contrast(white,black),21.0,places=2)
  self.assertAlmostEqual(motion.contrast(white,white),1.0,places=2)
  self.assertIsNone(motion.rgb('not a colour'))
  self.assertEqual(motion.rgb('#F5A623'),(245,166,35))

 def ink_width(self,text,size,font):
  """What drawtext actually puts on screen, measured off the pixels."""
  W,H=2600,300
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  f=Path(box.name)/'t.txt';f.write_text(text,encoding='utf-8')
  p=subprocess.run(['ffmpeg','-hide_banner','-v','error','-f','lavfi',
   '-i','color=c=black:s=%dx%d'%(W,H),'-vf',
   "drawtext=fontfile='%s':textfile='%s':expansion=none:fontcolor=white:fontsize=%d:x=60:y=60"
   %(engine.filter_path(font),engine.filter_path(f),size),
   '-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True)
  raw=p.stdout
  if len(raw)<W*H:return None
  lo,hi=W,-1
  for y in range(H):
   row=raw[y*W:(y+1)*W]
   for x in range(W):
    if row[x]>40:
     if x<lo:lo=x
     if x>hi:hi=x
  return (hi-lo+1) if hi>=0 else None
 @unittest.skipUnless(RENDERABLE,'this ffmpeg cannot draw: '+WHY_NOT)
 def test_the_measured_width_is_the_width_that_gets_drawn(self):
  """The parser is checked against the renderer, not against itself.

  The old estimate assumed an average character. On ten capital I it was 96% too
  wide and on ten m it was 41% too narrow, so a line of wide glyphs ran most of the
  way out of the frame while nothing measured anything."""
  font=engine.detect()['font_file']
  self.assertIsNotNone(font)
  for size,text in [(64,'Reserver un creneau'),(120,'149 EUR'),
                    (44,'Perimetre publie, pieces sous 20 EUR incluses'),
                    (56,'IIIIIIIIII'),(56,'mmmmmmmmmm')]:
   drawn=self.ink_width(text,size,font)
   self.assertIsNotNone(drawn,text)
   computed=engine.measure_text(text,size,font)
   self.assertIsNotNone(computed,text)
   # Advance width includes the side bearings the ink does not, so it reads a little
   # wide. Wide is the safe direction for wrapping; narrow is what runs off the frame.
   self.assertGreaterEqual(computed,drawn*0.98,'%r measured narrower than it draws'%text)
   self.assertLessEqual(computed,drawn*1.15,'%r measured far wider than it draws'%text)
 def test_the_font_file_is_read_rather_than_assumed(self):
  font=engine.detect()['font_file']
  m=engine.font_metrics(font)
  self.assertIsNotNone(m)
  self.assertGreater(m['units'],0)
  self.assertTrue(m['advances'])
  self.assertIn(ord('A'),m['cmap'])
  self.assertGreater(engine.measure_text('mmmm',60,font),engine.measure_text('iiii',60,font))
 def test_an_unreadable_face_falls_back_instead_of_raising(self):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  fake=Path(box.name)/'not-a-font.ttf';fake.write_bytes(b'this is not a font at all')
  self.assertIsNone(engine.font_metrics(fake))
  self.assertIsNone(engine.measure_text('abc',40,fake))
  self.assertIsNone(engine.measure_text('abc',40,None))
  # The wrap still returns every word, using the average-width fallback.
  wrapped=engine.wrap_text('un deux trois quatre cinq six sept huit',300,40,fake)
  self.assertEqual(wrapped.replace(chr(10),' ').split(),
                   'un deux trois quatre cinq six sept huit'.split())
 def test_no_wrapped_line_exceeds_the_column_it_was_wrapped_to(self):
  font=engine.detect()['font_file']
  for text in ['Perimetre publie, pieces sous 20 EUR incluses',
               'mmmmmmmmmm mmmmmmmmmm mmmmmmmmmm','anticonstitutionnellement']:
   for width,size in [(900,48),(660,37),(400,60)]:
    wrapped=engine.wrap_text(text,width,size,font)
    self.assertEqual(wrapped.replace(chr(10),' ').split(),text.split())
    for line in wrapped.split(chr(10)):
     if len(line.split())>1:
      self.assertLessEqual(engine.measure_text(line,size,font),width,repr(line))
 def test_a_machine_that_cannot_draw_stops_instead_of_shipping_a_silent_ad(self):
  """Exit 3, with the missing part named, and nothing written.

  This is the case Homebrew's macOS ffmpeg actually produces: libx264 and aac
  present, libfreetype absent, so every encode succeeds and no character can be put
  on screen. Rendering anyway would deliver an ad with the words missing, which
  passes a duration check and fails in front of a viewer."""
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  root=Path(box.name);(root/'examples').mkdir()
  shutil.copytree(BUILD/'src/motion/scripts',root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copy2(RENDER_EXAMPLE,root/'examples/motion-project.render.json')
  crippled={'ffmpeg':'/usr/bin/ffmpeg','ffprobe':'/usr/bin/ffprobe','filters':[],
            'missing_filters':['drawtext','subtitles'],'freetype':False,'fonts':370,
            'font_file':None,'engine':'ffmpeg-python-reference','javascript_required':False,
            'encoders':{'libx264':True,'aac':True},'usable':False,
            'reason':'missing filters: drawtext, subtitles; ffmpeg built without '
                     'libfreetype, so no text can be drawn'}
  argv=['render_motion.py',str(root/'examples/motion-project.render.json'),
        '--root',str(root),'--apply']
  with unittest.mock.patch.object(renderer.engine,'detect',return_value=crippled), \
       unittest.mock.patch.object(sys,'argv',argv), \
       unittest.mock.patch('sys.stdout',io.StringIO()) as out,        unittest.mock.patch('sys.stderr',io.StringIO()):
   code=renderer.main()
  self.assertEqual(code,3)
  self.assertIn('drawtext',out.getvalue())
  self.assertFalse((root/'exports').exists(),'it wrote an export it could not draw')
 def test_a_gradient_is_the_same_gradient_on_the_next_run(self):
  """`gradients` defaults to a random seed, so two renders of one manifest differed
  in every byte and the hash written into the manifest meant nothing."""
  self.assertEqual(engine.stable_seed('s1'),engine.stable_seed('s1'))
  self.assertNotEqual(engine.stable_seed('s1'),engine.stable_seed('s2'))
  d=self.design();m=self.manifest()
  lay=engine.layout_for(self.fmt('9:16'),d)
  scene=next(s for s in m['scenes'] if (s.get('background') or {}).get('kind')=='gradient')
  args,_c,_l=engine.scene_inputs(scene,{},3.0,30,lay)
  self.assertTrue(any('seed=' in str(a) for a in args),args)


class MotionRenderTests(unittest.TestCase):
 """The one-shot, end to end, measured out of the files it wrote."""
 SLUG='chauffe-eau-prix-ecrit'
 @classmethod
 def setUpClass(cls):
  if not RENDERABLE:raise unittest.SkipTest('this ffmpeg cannot draw: '+WHY_NOT)
  cls.box=tempfile.TemporaryDirectory();cls.root=Path(cls.box.name)
  shutil.copytree(BUILD/'src/motion/scripts',cls.root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  (cls.root/'examples').mkdir()
  shutil.copy2(RENDER_EXAMPLE,cls.root/'examples/motion-project.render.json')
  made=subprocess.run([sys.executable,str(cls.root/'scripts/make_fixture_assets.py'),
                       '--out',str(cls.root/'fixtures')],capture_output=True,text=True)
  assert made.returncode==0,made.stderr
  cls.report=cls.render(['--apply','--contact-sheet'])
 @classmethod
 def render(cls,extra):
  run=subprocess.run([sys.executable,'scripts/render_motion.py',
                      'examples/motion-project.render.json','--root','.']+extra,
                     cwd=str(cls.root),capture_output=True,text=True)
  assert run.returncode==0,(run.stdout or '')+(run.stderr or '')
  return json.loads(run.stdout)
 @classmethod
 def tearDownClass(cls):
  if hasattr(cls,'box'):cls.box.cleanup()
 def manifest(self):
  return json.loads((self.root/'examples/motion-project.render.json').read_text(encoding='utf-8'))
 def test_the_one_shot_runs_from_a_directory_that_is_not_the_project(self):
  """`--root` has to be the only thing that decides where files are.

  It was not. `resolve_assets` walked `assets[]` and nothing else, so `voice.file`,
  `music.file` and `sfx[].file` reached ffmpeg as the relative strings the manifest
  wrote, and ffmpeg resolves those against the working directory of the process. The
  run died on the audio with `--root` correct and every file present. No test here
  could see it: all of them ran with the working directory already set to the
  project, which is the one arrangement that hides it."""
  elsewhere=tempfile.TemporaryDirectory();self.addCleanup(elsewhere.cleanup)
  out=self.root/('exports/9x16/%s.mp4'%self.SLUG)
  before=out.stat().st_size if out.is_file() else 0
  run=subprocess.run([sys.executable,str(self.root/'scripts/render_motion.py'),
                      str(self.root/'examples/motion-project.render.json'),
                      '--root',str(self.root),'--apply','--formats','9:16'],
                     cwd=elsewhere.name,capture_output=True,text=True)
  self.assertEqual(run.returncode,0,(run.stdout or '')+(run.stderr or ''))
  self.assertNotIn('Traceback',run.stderr,'a traceback is not a report')
  self.assertTrue(out.is_file())
  self.assertGreater(out.stat().st_size,120000)
  m,_f=inspector.measure(out)
  self.assertEqual(m['audio_streams'],1,'it rendered, but without the audio')
  self.assertEqual(m['decode_errors'],0)
  self.assertEqual(before and m['width'],before and 1080)
 def test_a_sound_file_that_climbs_out_of_the_project_is_refused(self):
  """The pictures were checked for this and the three sound fields were not, so a
  manifest could name a file anywhere on the machine and have it read into an ad."""
  for field,put in (('voice',lambda m,p:m['voice'].__setitem__('file',p)),
                    ('music',lambda m,p:m['music'].__setitem__('file',p)),
                    ('sfx',lambda m,p:m['sfx'][0].__setitem__('file',p))):
   m=self.manifest();put(m,'../'*6+'Windows/win.ini')
   bad=self.root/('examples/escape-%s.json'%field)
   bad.write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8')
   run=subprocess.run([sys.executable,'scripts/render_motion.py',str(bad),
                       '--root','.','--apply','--formats','9:16'],
                      cwd=str(self.root),capture_output=True,text=True)
   self.assertEqual(run.returncode,2,field+': '+(run.stdout or '')+(run.stderr or ''))
   self.assertIn('climbing out',run.stdout,field)
 def test_a_render_that_fails_reports_instead_of_printing_a_traceback(self):
  """An exit status nobody chose and a stack trace on the terminal is not a result.
  The failure is stated and `rendered` says plainly that nothing was delivered."""
  m=self.manifest();m['music']['file']='fixtures/absent-bed.wav'
  bad=self.root/'examples/absent.json'
  bad.write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8')
  run=subprocess.run([sys.executable,'scripts/render_motion.py',str(bad),
                      '--root','.','--apply','--formats','9:16'],
                     cwd=str(self.root),capture_output=True,text=True)
  self.assertIn(run.returncode,(2,4),(run.stdout or '')+(run.stderr or ''))
  self.assertNotIn('Traceback',run.stderr)
  self.assertIn('absent-bed.wav',run.stdout)
 def test_a_second_art_direction_is_a_different_film_from_the_same_engine(self):
  """The look has to live in the manifest, not in the code.

  A design system nobody has ever pointed somewhere else is an assumption. This one
  renders the shipped editorial example: light ground, dark ink, one cold accent,
  tighter leading, a static camera, and a softened plane behind a sharp one. Same
  engine, same schema, same command."""
  # Its own project directory. Rendering it into the shared one would overwrite
  # `.motion-work/9x16` and the resume state, and the tests that run after would then
  # be measuring this film instead of theirs.
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  root=Path(box.name);(root/'examples').mkdir()
  shutil.copytree(BUILD/'src/motion/scripts',root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copy2(BUILD/'src/motion/examples/motion-project.editorial.json',
               root/'examples/motion-project.editorial.json')
  made=subprocess.run([sys.executable,str(root/'scripts/make_fixture_assets.py'),
                       '--out',str(root/'fixtures')],capture_output=True,text=True)
  self.assertEqual(made.returncode,0,made.stderr)
  # All three ratios, not one. The manifest declares three compositions, and a
  # manifest that composes three and exports one is refused by its own validator,
  # correctly. It also makes this the second proof that the three are compositions.
  run=subprocess.run([sys.executable,'scripts/render_motion.py',
                      'examples/motion-project.editorial.json','--root','.','--apply'],
                     cwd=str(root),capture_output=True,text=True)
  self.assertEqual(run.returncode,0,(run.stdout or '')+(run.stderr or ''))
  other=json.loads(run.stdout)
  self.assertEqual(other['verdict'],'pass',json.dumps(other['findings']))
  self.assertEqual({e['ratio'] for e in other['exports']},{'9:16','4:5','16:9'})
  self.assertEqual({e['size'] for e in other['exports']},
                   {'1080x1920','1080x1350','1920x1080'})
  out=root/next(e['path'] for e in other['exports'] if e['ratio']=='9:16')
  self.assertTrue(out.is_file())
  m,_f=inspector.measure(out)
  self.assertEqual((m['width'],m['height']),(1080,1920))
  self.assertEqual(m['decode_errors'],0)
  self.assertEqual(m['audio_streams'],1)
  self.assertEqual(m['freeze_regions'],0)
  # The two films do not look alike. Compared on the mean grey of one frame, because
  # a light art direction and a dark one cannot land in the same place.
  def grey(path,at):
   probe=root/('grey-%s.png'%hashlib.sha256((str(path)+at).encode()).hexdigest()[:8])
   subprocess.run(['ffmpeg','-v','error','-ss',at,'-i',str(path),'-frames:v','1',
                   '-vf','scale=8:8','-pix_fmt','gray','-y',str(probe)],
                  check=True,capture_output=True)
   raw=subprocess.run(['ffmpeg','-v','error','-i',str(probe),'-pix_fmt','gray',
                       '-f','rawvideo','-'],capture_output=True).stdout
   return sum(raw)/max(1,len(raw))
  light=grey(out,'5')
  dark=grey(self.root/('exports/9x16/%s.mp4'%self.SLUG),'5')
  self.assertGreater(light-dark,60,
                     'the editorial direction rendered as dark as the first one, so the '
                     'palette is not reaching the film: %.1f vs %.1f'%(light,dark))
  # And the manifest it just rewrote still describes the files it actually wrote.
  check=subprocess.run([sys.executable,'scripts/check_motion_project.py',
                        'examples/motion-project.editorial.json','--root','.'],
                       cwd=str(root),capture_output=True,text=True)
  self.assertEqual(check.returncode,0,check.stdout+check.stderr)
  self.assertEqual(json.loads(check.stdout),{'errors':0,'warnings':0})
 def test_the_fixture_is_a_real_ad_length(self):
  scenes=self.manifest()['scenes']
  total=max(float(s['end']) for s in scenes)
  self.assertGreaterEqual(total,12.0);self.assertLessEqual(total,20.0)
  self.assertGreaterEqual(len(scenes),4)
 def test_three_real_files_at_the_three_declared_sizes(self):
  want={'9:16':(1080,1920),'4:5':(1080,1350),'16:9':(1920,1080)}
  self.assertEqual(self.report['verdict'],'pass',json.dumps(self.report['findings']))
  seen={}
  for export in self.report['exports']:
   path=self.root/export['path']
   self.assertTrue(path.is_file(),export['path'])
   self.assertGreater(path.stat().st_size,120000,'%s is too small to be a real ad'%export['path'])
   m,_f=inspector.measure(path)
   seen[export['ratio']]=(m['width'],m['height'])
   self.assertEqual(m['decode_errors'],0,export['path'])
   self.assertAlmostEqual(m['duration_seconds'],16.0,delta=0.15)
   self.assertEqual(m['audio_streams'],1)
   self.assertEqual(m['freeze_regions'],0,'%s is a still, not motion'%export['path'])
  self.assertEqual(seen,want)
 def test_the_exports_are_not_the_same_picture_three_times(self):
  """A crop of one master would put the same pixels in the same order. Compare the
  frame each format shows at the same second."""
  frames=[]
  for ratio in ('9x16','4x5','16x9'):
   out=self.root/('probe-'+ratio+'.png')
   subprocess.run(['ffmpeg','-v','error','-ss','5','-i',
                   str(self.root/('exports/%s/%s.mp4'%(ratio,self.SLUG))),
                   '-frames:v','1','-y',str(out)],check=True,capture_output=True)
   frames.append(hashlib.sha256(out.read_bytes()).hexdigest())
  self.assertEqual(len(set(frames)),3)
 def test_every_export_is_normalised_to_the_declared_loudness(self):
  target=self.manifest()['loudness_target']
  for export in self.report['exports']:
   m,_f=inspector.measure(self.root/export['path'])
   self.assertIsNotNone(m['loudness_lufs'],export['path'])
   self.assertAlmostEqual(m['loudness_lufs'],float(target['value']),delta=1.5)
   self.assertLessEqual(m['true_peak_dbfs'],float(target['true_peak'])+0.5)
 def test_contact_sheets_and_control_frames_exist_to_be_looked_at(self):
  for ratio in ('9x16','4x5','16x9'):
   sheet=self.root/('exports/%s/%s-contact-sheet.png'%(ratio,self.SLUG))
   self.assertTrue(sheet.is_file(),str(sheet))
   self.assertGreater(sheet.stat().st_size,20000)
   frames=sorted((self.root/('exports/%s/%s-frames'%(ratio,self.SLUG))).glob('*.png'))
   self.assertGreaterEqual(len(frames),4)
 def test_the_manifest_is_updated_from_the_files_and_not_from_the_plan(self):
  m=self.manifest()
  self.assertEqual(m['state'],'measured')
  self.assertEqual(m['engine']['name'],'ffmpeg-python-reference')
  self.assertFalse(m['engine']['javascript_required'])
  self.assertEqual(len(m['exports']),3)
  for export in m['exports']:
   path=self.root/export['path']
   self.assertTrue(path.is_file(),export['path'])
   self.assertEqual(export['sha256'],renderer.digest_of(path))
   measured=inspector.measure(path)[0]
   self.assertEqual((export['measurements']['width'],export['measurements']['height']),
                    (measured['width'],measured['height']))
   self.assertEqual(export['measurements']['size_bytes'],path.stat().st_size)
   self.assertEqual(export['state'],'measured')
 def test_the_updated_manifest_still_validates_against_its_own_files(self):
  run=subprocess.run([sys.executable,'scripts/check_motion_project.py',
                      'examples/motion-project.render.json','--root','.'],
                     cwd=str(self.root),capture_output=True,text=True)
  self.assertEqual(run.returncode,0,run.stdout+run.stderr)
  self.assertEqual(json.loads(run.stdout)['errors'],0)
 def test_a_preview_renders_nothing_and_changes_nothing(self):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  root=Path(box.name)
  shutil.copytree(BUILD/'src/motion/scripts',root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  (root/'examples').mkdir()
  shutil.copy2(RENDER_EXAMPLE,root/'examples/motion-project.render.json')
  before=(root/'examples/motion-project.render.json').read_bytes()
  subprocess.run([sys.executable,'scripts/render_motion.py',
                  'examples/motion-project.render.json','--root','.'],
                 cwd=str(root),capture_output=True,text=True)
  self.assertFalse((root/'exports').exists())
  self.assertEqual((root/'examples/motion-project.render.json').read_bytes(),before)
 def test_a_truncated_clip_is_not_mistaken_for_a_finished_one(self):
  clip=self.root/'.motion-work/9x16/scene-00.mp4'
  self.assertTrue(clip.is_file())
  frames=engine.scene_frames(3.2+0.35,30)
  self.assertTrue(renderer.complete_clip(clip,frames))
  self.assertFalse(renderer.complete_clip(clip,frames+1))
  half=self.root/'half.mp4';half.write_bytes(clip.read_bytes()[:len(clip.read_bytes())//2])
  self.assertFalse(renderer.complete_clip(half,frames))
  self.assertFalse(renderer.complete_clip(self.root/'nothing-here.mp4',frames))
 def test_resume_reuses_the_clips_that_survived_and_rebuilds_the_rest(self):
  work=self.root/'.motion-work/9x16'
  keep=work/'scene-01.mp4';broken=work/'scene-02.mp4'
  before=keep.stat().st_mtime_ns
  broken.write_bytes(broken.read_bytes()[:2048])
  (work/'scene-03.mp4').unlink()
  (self.root/('exports/9x16/%s.mp4'%self.SLUG)).unlink()
  report=self.render(['--apply','--resume','--formats','9:16'])
  self.assertEqual(report['verdict'],'pass')
  self.assertEqual(keep.stat().st_mtime_ns,before,'a finished clip was rebuilt anyway')
  self.assertTrue(renderer.complete_clip(broken,engine.scene_frames(3.2+0.3,30)))
  m,_f=inspector.measure(self.root/('exports/9x16/%s.mp4'%self.SLUG))
  self.assertAlmostEqual(m['duration_seconds'],16.0,delta=0.15)
 def test_rendering_the_same_manifest_twice_produces_the_same_bytes(self):
  """A hash in the manifest is worth nothing if the next render changes every byte.

  Two things made this false and neither was visible in any output. `gradients`
  defaults to a random seed, so every run drew a different background. And
  `sidechaincompress` reads two inputs whose framing varies between runs, so the
  ducking diverged and the audio encoded differently every time."""
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  runs=[]
  for n in ('first','second'):
   root=Path(box.name)/n
   (root/'examples').mkdir(parents=True)
   shutil.copytree(BUILD/'src/motion/scripts',root/'scripts',
                   ignore=shutil.ignore_patterns('__pycache__'))
   shutil.copy2(BUILD/'src/common/scripts/check_artifact.py',root/'scripts')
   shutil.copy2(RENDER_EXAMPLE,root/'examples/motion-project.render.json')
   made=subprocess.run([sys.executable,str(root/'scripts/make_fixture_assets.py'),
                        '--out',str(root/'fixtures')],capture_output=True,text=True)
   self.assertEqual(made.returncode,0,made.stderr)
   run=subprocess.run([sys.executable,'scripts/render_motion.py',
                       'examples/motion-project.render.json','--root','.','--apply',
                       '--formats','9:16'],cwd=str(root),capture_output=True,text=True)
   self.assertEqual(run.returncode,0,(run.stdout or '')+(run.stderr or ''))
   runs.append(root)
  for rel in ['fixtures/texture-loop.mp4','fixtures/product-still.png',
              '.motion-work/9x16/audio.m4a',
              'exports/9x16/%s.mp4'%self.SLUG]:
   digests={renderer.digest_of(r/rel) for r in runs}
   self.assertEqual(len(digests),1,'%s differs between two identical renders'%rel)
 def test_an_asset_outside_the_project_is_refused(self):
  box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
  root=Path(box.name);(root/'examples').mkdir()
  shutil.copytree(BUILD/'src/motion/scripts',root/'scripts',
                  ignore=shutil.ignore_patterns('__pycache__'))
  m=json.loads(RENDER_EXAMPLE.read_text(encoding='utf-8'))
  m['assets'][0]['path']='../outside/secret.png'
  (root/'examples/motion-project.render.json').write_text(json.dumps(m),encoding='utf-8')
  run=subprocess.run([sys.executable,'scripts/render_motion.py',
                      'examples/motion-project.render.json','--root','.','--apply'],
                     cwd=str(root),capture_output=True,text=True)
  self.assertNotEqual(run.returncode,0)
  self.assertFalse((root/'exports').exists())

if __name__=='__main__':unittest.main()
