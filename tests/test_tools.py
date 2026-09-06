import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
checker=load('checker',ROOT/'src/common/scripts/check_artifact.py')
brain=load('brain',ROOT/'src/common/scripts/init_brain.py')
installer=load('installer',ROOT/'install.py')

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
 def test_storyboard_measured_overrun(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product','voice':'demo','measured_voice_seconds':3}]};self.assertTrue(checker.check(d)[0])
 def test_nan_and_bool_times(self):
  for value in [float('nan'),True]:
   d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':value,'end':2,'visual':'product'}]};self.assertTrue(checker.check(d)[0])
 def test_unmeasured_voice_warns(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':3,'visual':'product','voice':'demo'}]};e,w=checker.check(d);self.assertFalse(e);self.assertTrue(w)
 def test_brain_preview_and_preserve(self):
  with tempfile.TemporaryDirectory() as t:
   result=brain.initialize(t);self.assertFalse((Path(t)/'.ads-brain').exists())
   brain.initialize(t,True);self.assertEqual((Path(t)/'.ads-brain/.gitignore').read_text(),'*\n');p=Path(t)/'.ads-brain/brand.json';original=p.read_bytes()
   with self.assertRaises(ValueError):brain.initialize(t,True)
   self.assertEqual(p.read_bytes(),original);self.assertEqual(json.loads(original)['status'],'intake_required')
 def test_install_preview_idempotence_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   target=Path(t)/'skills';installer.install('codex',target_root=target);self.assertFalse(target.exists())
   installer.install('codex',target_root=target,apply=True)
   plans=installer.install('codex',target_root=target,apply=True);self.assertTrue(all(x['action']=='already-identical' for x in plans))
   file=target/'meta-ads-codex/SKILL.md';file.write_text('user edit',encoding='utf-8')
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
   try:(target/'meta-ads-codex').symlink_to(real,target_is_directory=True)
   except OSError as e:self.skipTest('Symlink privilege unavailable: '+str(e))
   with self.assertRaises(ValueError):installer.install('codex','solo',target_root=target,apply=True)
 def test_installer_rejects_bad_runtime(self):
  with self.assertRaises(ValueError):installer.install('unknown')
if __name__=='__main__':unittest.main()
