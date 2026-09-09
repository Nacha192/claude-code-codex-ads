import copy,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile,unittest,zipfile
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
EXAMPLE=BUILD/'src/motion/examples/motion-project.example.json'
FFMPEG=shutil.which('ffmpeg') and shutil.which('ffprobe')

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

if __name__=='__main__':unittest.main()
