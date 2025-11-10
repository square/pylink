# Issues Directory Structure

This directory contains documentation and tests for resolved pylink-square issues.

## Structure

```
issues/
├── 151/                    # Issue #151: USB JLink selection by Serial Number
│   ├── README.md           # Complete issue and solution documentation
│   ├── ISSUE_151_SOLUTION.md  # Detailed solution analysis
│   ├── TEST_RESULTS_ISSUE_151.md  # Test results
│   ├── test_issue_151.py   # Basic functional tests
│   ├── test_issue_151_integration.py  # Integration tests
│   └── test_issue_151_edge_cases.py   # Edge case tests
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

---

## Conventions

- Each issue has its own numbered directory (e.g., `151/`)
- The issue's README.md contains all relevant information
- Tests must be executable independently from the issue directory
- All files related to an issue are in its directory
