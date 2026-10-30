import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPTS=Path(__file__).resolve().parents[1]
GIT=shutil.which('git')

class DecisionGuards(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='decision-guard-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.repo=self.root/'repo';self.repo.mkdir()
        self.git('init','-q','-b','main');self.git('config','user.email','fixture@example.invalid');self.git('config','user.name','Fixture')
        (self.repo/'f').write_text('baseline');(self.repo/'removed').write_text('baseline')
        self.git('add','.');self.git('commit','-qm','baseline');self.base=self.git('rev-parse','HEAD')
        (self.repo/'f').write_text('intervention');(self.repo/'removed').unlink();self.git('add','-A');self.git('commit','-qm','intervention')
        self.head=self.git('rev-parse','HEAD')

    def git(self,*args):return subprocess.check_output([GIT,'-c','core.fsmonitor=false','-C',str(self.repo),*args],text=True).strip()
    def call(self,*args,cwd=None,env=None):return subprocess.run(['bash',str(SCRIPTS/args[0]),*args[1:]],cwd=cwd or self.repo,env=env,text=True,capture_output=True)
    def pin(self):self.assertEqual(self.call('pin_intervention.sh').returncode,0)
    def refused(self,result):self.assertNotEqual(result.returncode,0);self.assertNotIn('intervention commit dropped',result.stdout);self.assertEqual(self.git('rev-parse','HEAD'),self.head)

    def test_missing_pin_refused(self):self.refused(self.call('decide.sh','revert'))
    def test_dirty_tracked_refused(self):
        self.pin();(self.repo/'f').write_text('unsaved');self.refused(self.call('decide.sh','revert'));self.assertEqual((self.repo/'f').read_text(),'unsaved')
    def test_staged_changes_refused(self):
        self.pin();(self.repo/'new').write_text('unsaved');self.git('add','new');self.refused(self.call('decide.sh','revert'))
    def test_stale_head_refused(self):
        self.pin();self.git('commit','--allow-empty','-qm','other work');self.head=self.git('rev-parse','HEAD');self.refused(self.call('decide.sh','revert'))
    def test_untracked_baseline_collision_refused(self):
        self.pin();(self.repo/'removed').write_text('untracked private content');self.refused(self.call('decide.sh','revert'));self.assertEqual((self.repo/'removed').read_text(),'untracked private content')
    def test_subdirectory_refused(self):
        self.pin();p=self.repo/'sub';p.mkdir();self.refused(self.call('decide.sh','revert',cwd=p))
    def test_wrong_repository_refused(self):
        self.pin();p=self.root/'other';p.mkdir();subprocess.run([GIT,'init','-q',str(p)],check=True)
        self.refused(self.call('decide.sh','revert',cwd=p))
    def test_success_preserves_untracked_metrics(self):
        self.pin();(self.repo/'metrics.txt').write_text('keep evidence');r=self.call('decide.sh','revert');self.assertEqual(r.returncode,0,r.stderr);self.assertIn('intervention commit dropped',r.stdout);self.assertEqual(self.git('rev-parse','HEAD'),self.base);self.assertEqual((self.repo/'metrics.txt').read_text(),'keep evidence')
    def test_keep_consumes_pin_without_changing_head(self):
        self.pin();r=self.call('decide.sh','keep');self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(self.git('rev-parse','HEAD'),self.head);self.refused(self.call('decide.sh','revert'))
    def test_reset_failure_is_not_success(self):
        self.pin();b=self.root/'bin';b.mkdir();wrapper=b/'git'
        wrapper.write_text('#!/bin/sh\nif [ "$1" = reset ]; then exit 23; fi\nexec '+GIT+' "$@"\n');wrapper.chmod(0o755)
        env={**os.environ,'PATH':str(b)+os.pathsep+os.environ['PATH']}
        self.refused(self.call('decide.sh','revert',env=env))
    def test_invalid_decision_is_two(self):self.assertEqual(self.call('decide.sh','pin').returncode,2)

if __name__=='__main__':unittest.main()
