# Digi-Brain Multi-Pass Comprehensive Test Runner
# Implements focused testing for:
#   Pass 1: Security and reliability (Foundation & Safety)
#   Pass 2: Memory intelligence and product maturity (Cognition, Export, Migration & Benchmarks)

import argparse
import json
import os
import platform
import sys
import time
import unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

PASS1_MODULES = [
    "test_installer_security",
    "test_installer_parity",
    "test_authorization",
]

PASS2_MODULES = [
    "test_retrieval",
    "test_persona_export",
    "test_migration",
]


def load_suite(pass_number=None):
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if pass_number == 1:
        # Pass 1: Security and reliability
        # Installer hardening, verification parity, rollback, cross-platform, authorization, memory integrity safeguards
        for mod in PASS1_MODULES:
            suite.addTests(loader.loadTestsFromName(mod))
        # Add memory integrity safeguard tests
        from test_memory_integrity import TestMemoryIntegrity
        suite.addTest(TestMemoryIntegrity("test_append_only_integrity_rejects_deletion"))
        suite.addTest(TestMemoryIntegrity("test_poison_instruction_rejection"))
        suite.addTest(TestMemoryIntegrity("test_untrusted_content_authority_gating"))
        suite.addTest(TestMemoryIntegrity("test_inference_cannot_claim_universal_scope"))

    elif pass_number == 2:
        # Pass 2: Memory intelligence and product maturity
        # Provenance, contradiction/supersession, staged context retrieval, session recovery, persona export, migration
        for mod in PASS2_MODULES:
            suite.addTests(loader.loadTestsFromName(mod))
        # Add memory provenance, supersession, and contradiction tests
        from test_memory_integrity import TestMemoryIntegrity
        suite.addTest(TestMemoryIntegrity("test_valid_entry_append"))
        suite.addTest(TestMemoryIntegrity("test_supersession_preserves_history"))
        suite.addTest(TestMemoryIntegrity("test_contradiction_detection_and_disputed_handling"))

    else:
        # All tests
        suite = loader.discover(start_dir=tests_dir, pattern="test_*.py")

    return suite


def main():
    parser = argparse.ArgumentParser(description="Digi-Brain Test Runner")
    parser.add_argument("--pass-num", "--pass", type=int, choices=[1, 2], help="Run specific pass (1: Security & Reliability, 2: Memory Intelligence)")
    parser.add_argument("--run-benchmark", action="store_true", help="Execute comparative memory benchmark after tests")
    args = parser.parse_args()

    title = "DIGI-BRAIN COMPREHENSIVE TEST SUITE RUNNER"
    if args.pass_num == 1:
        title = "PASS 1: SECURITY AND RELIABILITY TEST RUNNER"
    elif args.pass_num == 2:
        title = "PASS 2: MEMORY INTELLIGENCE & PRODUCT MATURITY TEST RUNNER"

    print("======================================================================")
    print(f"           {title}                 ")
    print("======================================================================")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python:   {sys.version.split()[0]}")
    print(f"Target:   Pass {args.pass_num if args.pass_num else 'ALL (Combined Pass 1 + Pass 2)'}")
    print(f"Time:     {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("----------------------------------------------------------------------")

    start_time = time.time()
    suite = load_suite(args.pass_num)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("======================================================================")
    print("                      TEST EXECUTION SUMMARY                          ")
    print("======================================================================")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed:          {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed:          {len(result.failures)}")
    print(f"Errors:          {len(result.errors)}")
    print(f"Skipped:         {len(result.skipped)}")
    print(f"Total Duration:  {elapsed:.2f} seconds")
    print("======================================================================")

    if not result.wasSuccessful():
        print("OVERALL STATUS: FAIL")
        sys.exit(1)

    print("OVERALL STATUS: PASS")

    if args.run_benchmark or args.pass_num == 2:
        print("\n======================================================================")
        print("           RUNNING CONTROLLED MEMORY BENCHMARK HARNESS               ")
        print("======================================================================")
        from benchmarks.run_benchmark import DigiBrainBenchmark
        scenarios_file = os.path.join(repo_root, "benchmarks", "scenarios.json")
        benchmark = DigiBrainBenchmark(scenarios_file)
        bench_results = benchmark.run_all()
        print(f"Scenarios Evaluated: {len(benchmark.scenarios)}")
        print(f"Digi-Brain Completion Rate: {bench_results['Condition_C_Digi_Brain']['task_completion_rate'] * 100:.1f}%")
        print(f"Digi-Brain Constraint Compliance: {bench_results['Condition_C_Digi_Brain']['constraint_compliance'] * 100:.1f}%")
        print(f"Digi-Brain Memory Recall: {bench_results['Condition_C_Digi_Brain']['memory_recall'] * 100:.1f}%")
        print(f"Digi-Brain Irrelevant Retrieval: {bench_results['Condition_C_Digi_Brain']['irrelevant_retrieval_rate'] * 100:.1f}%")
        print("BENCHMARK EXECUTION: COMPLETE")

    sys.exit(0)

if __name__ == "__main__":
    main()
