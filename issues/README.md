# Issues Directory Structure

This directory contains documentation and tests for resolved pylink-square issues, bug reports, feature requests, and related analysis documents.

## Structure

```text
issues/
├── 151/                    # Issue #151: USB JLink selection by Serial Number
│   ├── README.md           # Complete issue and solution documentation
│   ├── ISSUE_151_SOLUTION.md  # Detailed solution analysis
│   ├── TEST_RESULTS_ISSUE_151.md  # Test results
│   ├── test_issue_151.py   # Basic functional tests
│   ├── test_issue_151_integration.py  # Integration tests
│   └── test_issue_151_edge_cases.py   # Edge case tests
├── 171/                    # Issue #171: Related to issue #237
│   └── README.md           # Issue documentation
├── 233/                    # Issue #233: Bug report
│   └── README.md           # Bug report documentation
├── 234/                    # Issue #234
│   └── README.md           # Issue documentation
├── 237/                    # Issue #237: Incorrect usage of return value in flash_file
│   └── README.md           # Issue documentation
├── 249/                    # Issue #249: rtt_start() fails to auto-detect RTT control block
│   └── README.md           # Bug report documentation
├── 252/                    # Issue #252: Reset Detection via SWD/JTAG Connection Health
│   ├── README.md           # Complete documentation with use case examples
│   └── example_*.py        # 6 complete example scripts
├── docs/                   # General documentation (not tied to specific issues)
│   ├── README.md           # Documentation index
│   ├── README_PR_fxd0h.md  # PR documentation for RTT improvements
│   ├── RTT2PTY_EVALUATION.md  # Evaluation of rtt2pty replication
│   ├── test_rtt_connection_README.md  # RTT connection test documentation
│   └── TROUBLESHOOTING.md  # General troubleshooting guide
├── tests/                  # General test scripts (not tied to specific issues)
│   ├── README.md           # Test scripts index
│   ├── test_rtt_connection.py  # Comprehensive RTT connection test
│   ├── test_rtt_diagnostic.py  # RTT diagnostic script
│   ├── test_rtt_simple.py      # Simple RTT verification test
│   └── test_rtt_specific_addr.py  # RTT test with specific address
├── tools/                  # Utility scripts and tools (not tied to specific issues)
│   ├── README.md           # Tools index
│   └── verify_installation.py  # Pylink installation verification script
├── 237_171_ANALYSIS.md     # Executive summary for issues #237 and #171
├── IMPACT_ANALYSIS_237_171.md  # Impact analysis for issues #237 and #171
├── ISSUES_ANALYSIS.md      # General analysis of easy-to-resolve issues
├── BUG_REPORT_TEMPLATE.md  # Template for bug reports
└── README.md               # This file
```

## Usage

Each issue has its own directory containing:

- **README.md**: Complete documentation of the problem, solution, and usage
- **Test files**: Python scripts that validate the solution
- **Additional documentation**: Detailed analysis if necessary

### Running Tests for an Issue

```bash
cd issues/151
python3 test_issue_151.py
python3 test_issue_151_integration.py
python3 test_issue_151_edge_cases.py
```

## Resolved Issues

### Issue #151 - USB JLink selection by Serial Number ✅

**Status**: Resolved  
**Date**: 2025-01-XX  
**Modified files**: `pylink/jlink.py`  
**Tests**: 28/28 passing

**Summary**: The `serial_no` passed to `JLink.__init__()` is now automatically used when `open()` is called without parameters.

See complete details in [issues/151/README.md](151/README.md)

### Issue #171 - Related to Issue #237 ✅

**Status**: Resolved  
**Modified files**: `pylink/jlink.py`

**Summary**: Related to issue #237. See [237_171_ANALYSIS.md](237_171_ANALYSIS.md) for details.

### Issue #233 - Bug Report ✅

**Status**: Documented  
**Modified files**: N/A

**Summary**: Bug report documentation. See [issues/233/README.md](233/README.md) for details.

### Issue #234 ✅

**Status**: Documented  
**Modified files**: N/A

**Summary**: Issue documentation. See [issues/234/README.md](234/README.md) for details.

### Issue #237 - Incorrect usage of return value in flash_file method ✅

**Status**: Resolved  
**Modified files**: `pylink/jlink.py`

**Summary**: Fixed incorrect usage of return value in `flash_file()` method. See [237_171_ANALYSIS.md](237_171_ANALYSIS.md) and [IMPACT_ANALYSIS_237_171.md](IMPACT_ANALYSIS_237_171.md) for details.

### Issue #249 - rtt_start() fails to auto-detect RTT control block ✅

**Status**: Resolved  
**Modified files**: `pylink/jlink.py`

**Summary**: Fixed `rtt_start()` auto-detection failure. Auto-detection now works with improved search range generation. See [issues/249/README.md](249/README.md) for details.

### Issue #252 - Reset Detection via SWD/JTAG Connection Health Monitoring ✅

**Status**: Feature implemented in local fork, ready for PR  
**Date**: 2025-01-XX  
**Modified files**: `pylink/jlink.py`  
**GitHub Issue**: [Issue #252](https://github.com/square/pylink/issues/252)

**Summary**: Added `check_connection_health()` method for firmware-independent reset detection using SWD/JTAG reads (IDCODE, CPUID, registers). Works when CPU is running or halted.

See complete details and examples in [issues/252/README.md](252/README.md)

## Analysis Documents

### Issue-Specific Analysis

- **[237_171_ANALYSIS.md](237_171_ANALYSIS.md)**: Executive summary for issues #237 and #171
- **[IMPACT_ANALYSIS_237_171.md](IMPACT_ANALYSIS_237_171.md)**: Impact analysis for issues #237 and #171
- **[ISSUES_ANALYSIS.md](ISSUES_ANALYSIS.md)**: Analysis of easy-to-resolve issues

### Additional Documentation

- **[BUG_REPORT_TEMPLATE.md](BUG_REPORT_TEMPLATE.md)**: Template for creating bug reports

### General Documentation

See the [docs/](docs/) directory for:

- Pull request documentation
- Evaluation documents
- Testing documentation
- Troubleshooting guides

These documents are not tied to specific GitHub issues but provide valuable context and information about pylink improvements and usage.

### General Test Scripts

See the [tests/](tests/) directory for:

- RTT connection tests
- RTT diagnostic scripts
- Simple verification tests
- Address-specific RTT tests

These test scripts are for general functionality verification and debugging. Issue-specific tests are located in their respective issue directories (e.g., `issues/151/test_issue_151.py`).

### Utility Tools

See the [tools/](tools/) directory for:

- Installation verification scripts
- Development utilities
- General-purpose tools

These tools assist with pylink development and verification but are not tied to specific GitHub issues.

---

## Conventions

- Each issue has its own numbered directory (e.g., `151/`)
- The issue's README.md contains all relevant information
- Tests must be executable independently from the issue directory
- All files related to an issue are in its directory
