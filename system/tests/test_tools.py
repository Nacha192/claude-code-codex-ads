import importlib.util,json,tempfile,unittest
from pathlib import Path
BUILD=Path(__file__).resolve().parents[1]
ROOT=BUILD.parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
checker=load('checker',BUILD/'src/common/scripts/check_artifact.py')
brain=load('brain',BUILD/'src/common/scripts/init_brain.py')
installer=load('installer',BUILD/'install.py')

class ToolTests(unittest.TestCase):
 def brief(self):return {'schema_v':'1.0.0','kind':'brief','offer':'A fictional repair service','country':'FR','ad_language':'fr-FR','objective':'qualified inquiries','window':{'start':'2026-08-01','end':'2026-08-31'}}
 def creative(self):return {'schema_v':'1.0.0','kind':'creative','hook':'A clearer repair quote','ad_language':'en-GB','cta':'See the process','claims':[{'text':'Written scope included','proof_ids':['E1']}],'evidence':[{'id':'E1','type':'product_observed','source':'synthetic-fixture','supports':'Written scope is included'}]}
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
 def test_storyboard_kind_is_no_longer_accepted(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product'}]};self.assertTrue(checker.check(d)[0])
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
  for fixture in [self.brief,self.creative,self.generation]:
   d=fixture();d['notes']='authorization: Bearer '+'A'*32;self.assertTrue(checker.check(d)[0])
 def test_credential_nested_in_evidence(self):
  d=self.creative();d['evidence'][0]['source']='api_key='+'B'*24;self.assertTrue(checker.check(d)[0])
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
   file=target/'meta-ads-static-codex/SKILL.md';file.write_text('user edit',encoding='utf-8')
   with self.assertRaises(ValueError):installer.install('codex',target_root=target,apply=True)
   self.assertEqual(file.read_text(),'user edit')
 def test_installer_project_and_modes(self):
  with tempfile.TemporaryDirectory() as t:
   for runtime,mode in [('codex','solo'),('claude','team')]:
    plans=installer.install(runtime,mode,project=t,apply=True);self.assertEqual(len(plans),1)
    self.assertTrue((Path(plans[0]['target'])/'SKILL.md').is_file())
 def test_symlinked_ancestor_allowed_but_target_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();alias=root/'alias'
   try:alias.symlink_to(real,target_is_directory=True)
   except OSError as e:self.skipTest('Symlink privilege unavailable: '+str(e))
   installer.install('codex','solo',target_root=alias/'skills',apply=True)
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=alias,apply=True)
 def test_symlinked_skill_destination_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);real=root/'real';real.mkdir();target=root/'skills';target.mkdir()
   try:(target/'meta-ads-static-codex').symlink_to(real,target_is_directory=True)
   except OSError as e:self.skipTest('Symlink privilege unavailable: '+str(e))
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=target,apply=True)
 def test_installer_rejects_bad_runtime(self):
  with self.assertRaises(ValueError):installer.install('unknown')
if __name__=='__main__':unittest.main()
