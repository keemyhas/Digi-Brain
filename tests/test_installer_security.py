# Automated Security Regression Tests for Digi-Brain Installers
# Covers REQ-1.1, REQ-1.2, REQ-1.3, REQ-1.4, REQ-1.5, REQ-4.2

import os
import shutil
import subprocess
import tempfile
import unittest

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTALL_SH = os.path.join(REPO_DIR, "installer", "install.sh")
INSTALL_PS1 = os.path.join(REPO_DIR, "installer", "install.ps1")
BASH_PATH = r"C:\Program Files\Git\bin\bash.exe"

class TestInstallerSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="digi_sec_test_")
        # Use clean marker path without fingerprint names
        self.marker_file = r"C:\Temp\DIGI_PWNED_MARKER.txt"

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
        if os.path.exists(self.marker_file):
            try:
                os.remove(self.marker_file)
            except OSError:
                pass

    def _to_posix_path(self, win_path):
        drive, rest = os.path.splitdrive(win_path)
        d = drive.replace(":", "").lower()
        return f"/{d}" + rest.replace("\\", "/")

    def test_sh_injection_command_subst_in_answers(self):
        posix_marker = self._to_posix_path(self.marker_file)
        answers_file = os.path.join(self.test_dir, "answers.env")
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write(f'OWNER_NAME=$(touch "{posix_marker}")\n')
            f.write('PROJECT_NAME=SafeProject\n')

        target_dir = os.path.join(self.test_dir, "target_repo")
        os.makedirs(target_dir, exist_ok=True)
        posix_target = self._to_posix_path(target_dir)
        posix_answers = self._to_posix_path(answers_file)
        posix_sh = self._to_posix_path(INSTALL_SH)

        cmd = [BASH_PATH, posix_sh, posix_target, "--defaults", f"--answers-file={posix_answers}"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertFalse(os.path.exists(self.marker_file), "CRITICAL: Command substitution payload executed!")
        self.assertEqual(res.returncode, 0, f"Installer failed unexpectedly: {res.stderr}")

        brain_path = os.path.join(target_dir, ".agents", "memory", "brain.md")
        with open(brain_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("SafeProject", content)

    def test_sh_injection_semicolon_and_backticks(self):
        posix_marker = self._to_posix_path(self.marker_file)
        answers_file = os.path.join(self.test_dir, "answers_semi.env")
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write(f'OWNER_NAME=Ada; `touch {posix_marker}`\n')

        target_dir = os.path.join(self.test_dir, "target_semi")
        os.makedirs(target_dir, exist_ok=True)
        posix_target = self._to_posix_path(target_dir)
        posix_answers = self._to_posix_path(answers_file)
        posix_sh = self._to_posix_path(INSTALL_SH)

        cmd = [BASH_PATH, posix_sh, posix_target, "--defaults", f"--answers-file={posix_answers}"]
        subprocess.run(cmd, capture_output=True, text=True)

        self.assertFalse(os.path.exists(self.marker_file), "CRITICAL: Semicolon/backtick payload executed!")

    def test_sh_rejects_unapproved_key(self):
        answers_file = os.path.join(self.test_dir, "bad_key.env")
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write("MALICIOUS_KEY=evil_value\n")

        target_dir = os.path.join(self.test_dir, "target_bad")
        os.makedirs(target_dir, exist_ok=True)
        posix_target = self._to_posix_path(target_dir)
        posix_answers = self._to_posix_path(answers_file)
        posix_sh = self._to_posix_path(INSTALL_SH)

        cmd = [BASH_PATH, posix_sh, posix_target, "--defaults", f"--answers-file={posix_answers}"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertNotEqual(res.returncode, 0, "Installer accepted unapproved key!")
        self.assertIn("unrecognized configuration key", res.stderr + res.stdout)

    def test_sh_rejects_malformed_answers_line(self):
        answers_file = os.path.join(self.test_dir, "malformed.env")
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write("THIS_IS_NOT_A_VALID_LINE\n")

        target_dir = os.path.join(self.test_dir, "target_malformed")
        os.makedirs(target_dir, exist_ok=True)
        posix_target = self._to_posix_path(target_dir)
        posix_answers = self._to_posix_path(answers_file)
        posix_sh = self._to_posix_path(INSTALL_SH)

        cmd = [BASH_PATH, posix_sh, posix_target, "--defaults", f"--answers-file={posix_answers}"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertNotEqual(res.returncode, 0, "Installer accepted malformed answers line!")
        self.assertIn("malformed line in answers file", res.stderr + res.stdout)

    def test_ps1_rejects_unapproved_key(self):
        answers_file = os.path.join(self.test_dir, "bad_key_ps.env")
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write("UNAPPROVED_KEY=hacked\n")

        target_dir = os.path.join(self.test_dir, "target_bad_ps")
        os.makedirs(target_dir, exist_ok=True)

        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
               "-Target", target_dir, "-Defaults", "-AnswersFile", answers_file]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertNotEqual(res.returncode, 0, "PowerShell installer accepted unapproved key!")
        self.assertIn("unrecognized configuration key", res.stderr + res.stdout)

    def test_ps1_special_characters_and_unicode(self):
        answers_file = os.path.join(self.test_dir, "unicode_ps.env")
        special_name = "Ada & Grace 'Tester' <Dev> ?? [Core]"
        with open(answers_file, "w", encoding="utf-8") as f:
            f.write(f"OWNER_NAME={special_name}\n")

        target_dir = os.path.join(self.test_dir, "target_unicode_ps")
        os.makedirs(target_dir, exist_ok=True)

        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
               "-Target", target_dir, "-Defaults", "-AnswersFile", answers_file]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertEqual(res.returncode, 0, f"Installer failed on Unicode/special chars: {res.stderr}")
        checklist_path = os.path.join(target_dir, ".agents", "BOOT-CHECKLIST.md")
        with open(checklist_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn(special_name, content)

    def test_paths_with_spaces(self):
        target_dir = os.path.join(self.test_dir, "Target Path With Spaces")
        os.makedirs(target_dir, exist_ok=True)

        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
               "-Target", target_dir, "-Defaults"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertEqual(res.returncode, 0, f"Failed on path with spaces: {res.stderr}")
        self.assertTrue(os.path.exists(os.path.join(target_dir, ".agents", "memory", "brain.md")))

    def test_sh_paths_with_spaces(self):
        target_dir = os.path.join(self.test_dir, "Target Sh Spaces")
        os.makedirs(target_dir, exist_ok=True)
        posix_target = self._to_posix_path(target_dir)
        posix_sh = self._to_posix_path(INSTALL_SH)

        cmd = [BASH_PATH, posix_sh, posix_target, "--defaults"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertEqual(res.returncode, 0, f"Failed on POSIX path with spaces: {res.stderr}")
        self.assertTrue(os.path.exists(os.path.join(target_dir, ".agents", "memory", "brain.md")))

    def test_installer_staging_and_rollback(self):
        target_dir = os.path.join(self.test_dir, "target_rollback")
        os.makedirs(target_dir, exist_ok=True)

        cmd1 = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
                "-Target", target_dir, "-Defaults"]
        res1 = subprocess.run(cmd1, capture_output=True, text=True)
        self.assertEqual(res1.returncode, 0)

        marker_in_original = os.path.join(target_dir, ".agents", "memory", "ORIGINAL_TOKEN.txt")
        with open(marker_in_original, "w", encoding="utf-8") as f:
            f.write("MUST_SURVIVE_ROLLBACK")

        bad_answers = os.path.join(self.test_dir, "bad_secret.env")
        with open(bad_answers, "w", encoding="utf-8") as f:
            f.write("DEV_URL=http://localhost:3000\n")
            f.write("SAFETY_INVARIANTS=AKIA1234567890ABCDEF\n")

        cmd2 = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
                "-Target", target_dir, "-Overwrite", "-Defaults", "-AnswersFile", bad_answers]
        res2 = subprocess.run(cmd2, capture_output=True, text=True)

        self.assertNotEqual(res2.returncode, 0, "Installer should have failed on secret detection!")
        self.assertTrue(os.path.exists(marker_in_original), "CRITICAL: Original .agents was wiped on failed install!")

if __name__ == "__main__":
    unittest.main()
