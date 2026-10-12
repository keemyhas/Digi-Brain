# Cross-Platform Parity Tests for Digi-Brain Installers
# Covers REQ-1.6, REQ-4.7

import os
import shutil
import subprocess
import tempfile
import unittest

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTALL_SH = os.path.join(REPO_DIR, "installer", "install.sh")
INSTALL_PS1 = os.path.join(REPO_DIR, "installer", "install.ps1")
BASH_PATH = r"C:\Program Files\Git\bin\bash.exe"

class TestInstallerParity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="digi_parity_")
        self.sh_target = os.path.join(self.test_dir, "sh_target")
        self.ps1_target = os.path.join(self.test_dir, "ps1_target")
        os.makedirs(self.sh_target, exist_ok=True)
        os.makedirs(self.ps1_target, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def _to_posix_path(self, win_path):
        drive, rest = os.path.splitdrive(win_path)
        d = drive.replace(":", "").lower()
        return f"/{d}" + rest.replace("\\", "/")

    def test_default_installation_parity(self):
        # 1. Run install.sh with --defaults
        posix_target = self._to_posix_path(self.sh_target)
        posix_sh = self._to_posix_path(INSTALL_SH)
        cmd_sh = [BASH_PATH, posix_sh, posix_target, "--defaults"]
        res_sh = subprocess.run(cmd_sh, capture_output=True, text=True)
        self.assertEqual(res_sh.returncode, 0, f"install.sh failed: {res_sh.stderr}")

        # 2. Run install.ps1 with -Defaults
        cmd_ps = ["powershell", "-ExecutionPolicy", "Bypass", "-File", INSTALL_PS1,
                  "-Target", self.ps1_target, "-Defaults"]
        res_ps = subprocess.run(cmd_ps, capture_output=True, text=True)
        self.assertEqual(res_ps.returncode, 0, f"install.ps1 failed: {res_ps.stderr}")

        # 3. Compare file lists
        sh_files = set()
        for root, _, files in os.walk(os.path.join(self.sh_target, ".agents")):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), os.path.join(self.sh_target, ".agents"))
                sh_files.add(rel.replace("\\", "/"))

        ps_files = set()
        for root, _, files in os.walk(os.path.join(self.ps1_target, ".agents")):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), os.path.join(self.ps1_target, ".agents"))
                ps_files.add(rel.replace("\\", "/"))

        self.assertEqual(sh_files, ps_files, f"File tree mismatch! Diff: {sh_files ^ ps_files}")

        # 4. Compare key file contents (e.g. brain.md, BOOT-CHECKLIST.md, skills-map.md)
        for check_rel in ["memory/brain.md", "BOOT-CHECKLIST.md", "skills-map.md"]:
            f_sh = os.path.join(self.sh_target, ".agents", check_rel.replace("/", os.sep))
            f_ps = os.path.join(self.ps1_target, ".agents", check_rel.replace("/", os.sep))

            with open(f_sh, "r", encoding="utf-8") as f:
                c_sh = f.read().replace("\r\n", "\n").strip()
            with open(f_ps, "r", encoding="utf-8") as f:
                c_ps = f.read().replace("\r\n", "\n").strip()

            self.assertEqual(c_sh, c_ps, f"Content mismatch in {check_rel}!")

        # 5. Compare root AGENTS.md bootstrap pointer
        root_sh_agents = os.path.join(self.sh_target, "AGENTS.md")
        root_ps_agents = os.path.join(self.ps1_target, "AGENTS.md")
        self.assertTrue(os.path.exists(root_sh_agents), "install.sh did not create root AGENTS.md")
        self.assertTrue(os.path.exists(root_ps_agents), "install.ps1 did not create root AGENTS.md")
        with open(root_sh_agents, "r", encoding="utf-8") as f:
            c_sh_root = f.read().replace("\r\n", "\n").strip()
        with open(root_ps_agents, "r", encoding="utf-8") as f:
            c_ps_root = f.read().replace("\r\n", "\n").strip()
        self.assertEqual(c_sh_root, c_ps_root, "Content mismatch in root AGENTS.md!")

if __name__ == "__main__":
    unittest.main()
