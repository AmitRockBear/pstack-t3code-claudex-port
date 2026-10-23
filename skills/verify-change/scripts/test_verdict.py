import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from subprocess import CompletedProcess

spec = importlib.util.spec_from_file_location('verdict', Path(__file__).with_name('verdict.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VerdictTests(unittest.TestCase):
    def record(self, directory: str, label: str) -> Path:
        out = Path(directory) / 'verdict.json'
        code = module.main(['record', '--repo', 'o/r', '--pr', '7', '--head', 'abc1234def', '--label', label, '--out', str(out)])
        self.assertEqual(code, 0)
        return out

    def test_matching_claim_at_same_head_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.record(directory, 'verified')
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'clean', '--head', 'abc1234']), 0)

    def test_clean_claim_on_partial_verdict_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.record(directory, 'partially-verified')
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'clean', '--head', 'abc1234def']), 1)
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'partially-verified', '--head', 'abc1234def']), 0)

    def test_moved_head_fails_even_for_matching_label(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.record(directory, 'verified')
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'verified', '--head', 'fff9999']), 1)

    def test_malformed_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'bad.json'
            out.write_text(json.dumps({'repo': 'o/r', 'pr': 7, 'head': 'abc', 'label': 'clean', 'measured_at': 'x'}))
            with self.assertRaises(ValueError):
                module.load(out)

    def carry(self, prior: Path, name: str = 'assessed.json', head: str = 'def5678') -> Path:
        out = prior.parent / name
        self.assertEqual(module.main(['carry-forward', '--record', str(prior), '--head', head,
            '--base', 'base123', '--base-branch', 'main', '--reason', 'Only a tested label changed; other paths are unchanged.',
            '--out', str(out)]), 0)
        return out

    def test_carry_preserves_original_proof_and_accepts_assessed_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            prior = self.record(directory, 'verified')
            before = prior.read_bytes()
            out = self.carry(prior)
            original, assessed = module.load(prior), module.load(out)
            self.assertEqual(prior.read_bytes(), before)
            self.assertEqual((assessed.head, assessed.measured_at), (original.head, original.measured_at))
            self.assertEqual(assessed.assessment.prior_record, str(prior.resolve()))
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'verified',
                '--head', 'def5678', '--base', 'base123', '--base-branch', 'main']), 0)

    def test_carried_evidence_rejects_later_head_base_and_destination_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.carry(self.record(directory, 'verified'))
            for head, base, branch in [('fff9999', 'base123', 'main'), ('def5678', 'newbase', 'main'), ('def5678', 'base123', 'other')]:
                with self.subTest(head=head, base=base, branch=branch):
                    self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'verified',
                        '--head', head, '--base', base, '--base-branch', branch]), 1)

    def test_carry_does_not_clear_a_partial_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.carry(self.record(directory, 'partially-verified'))
            self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'verified',
                '--head', 'def5678', '--base', 'base123', '--base-branch', 'main']), 1)

    def test_repeated_carry_keeps_the_original_measurement(self):
        with tempfile.TemporaryDirectory() as directory:
            original = self.record(directory, 'verified')
            first = self.carry(original)
            second = self.carry(first, 'second.json', 'ghi8901')
            a, b = module.load(original), module.load(second)
            self.assertEqual((b.head, b.measured_at, b.label), (a.head, a.measured_at, a.label))
            self.assertEqual(b.assessment.prior_record, str(first.resolve()))

    def test_check_reads_live_base_for_carried_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            out = self.carry(self.record(directory, 'verified'))
            with patch.object(module, 'current_head', return_value='def5678'), patch.object(module.subprocess, 'run',
                return_value=CompletedProcess([], 0, json.dumps({'baseRefOid': 'base123', 'baseRefName': 'main'}))) as query:
                self.assertEqual(module.main(['check', '--record', str(out), '--claim', 'verified']), 0)
                self.assertIn('baseRefOid,baseRefName', query.call_args.args[0])

    def test_carry_rejects_blank_reason_and_overwriting_its_source(self):
        with tempfile.TemporaryDirectory() as directory:
            prior = self.record(directory, 'verified')
            before = prior.read_bytes()
            for reason, out in [('', prior.parent / 'new.json'), ('Assessed unchanged paths', prior)]:
                with self.subTest(reason=reason, out=out), self.assertRaises(SystemExit):
                    module.main(['carry-forward', '--record', str(prior), '--head', 'def5678', '--base', 'base123',
                        '--base-branch', 'main', '--reason', reason, '--out', str(out)])
            self.assertEqual(prior.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
