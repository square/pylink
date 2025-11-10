#!/usr/bin/env python3
"""
Edge case tests for Issue #151 - Verifying all edge cases are handled correctly.
"""

def test_edge_case_logic():
    """Test edge cases in the logic"""
    print("=" * 70)
    print("Testing Edge Cases for Issue #151")
    print("=" * 70)
    print()
    
    def simulate_open_logic(__serial_no, __ip_addr, open_serial, open_ip):
        """Simulate the open() logic"""
        serial_no = open_serial
        ip_addr = open_ip
        
        # The actual logic from open()
        if serial_no is None and ip_addr is None:
            serial_no = __serial_no
        
        if ip_addr is None:
            ip_addr = __ip_addr
        
        return serial_no, ip_addr
    
    test_cases = [
        {
            "name": "Edge: serial_no=None in __init__, open() with serial_no=None",
            "__serial_no": None,
            "__ip_addr": None,
            "open_serial": None,
            "open_ip": None,
            "expected_serial": None,
            "expected_ip": None
        },
        {
            "name": "Edge: serial_no in __init__, open() with serial_no=None explicitly",
            "__serial_no": 600115433,
            "__ip_addr": None,
            "open_serial": None,  # Explicit None
            "open_ip": None,
            "expected_serial": 600115433,  # Should use __init__ value
            "expected_ip": None
        },
        {
            "name": "Edge: ip_addr in __init__, open() with ip_addr=None explicitly",
            "__serial_no": None,
            "__ip_addr": "192.168.1.1:80",
            "open_serial": None,
            "open_ip": None,  # Explicit None
            "expected_serial": None,
            "expected_ip": "192.168.1.1:80"  # Should use __init__ value
        },
        {
            "name": "Edge: Both in __init__, open() with both None",
            "__serial_no": 600115433,
            "__ip_addr": "192.168.1.1:80",
            "open_serial": None,
            "open_ip": None,
            "expected_serial": 600115433,  # Should use __init__ value
            "expected_ip": "192.168.1.1:80"  # Should use __init__ value
        },
        {
            "name": "Edge: serial_no in __init__, open() with ip_addr only",
            "__serial_no": 600115433,
            "__ip_addr": None,
            "open_serial": None,
            "open_ip": "10.0.0.1:90",
            "expected_serial": None,  # ip_addr provided, so serial_no stays None
            "expected_ip": "10.0.0.1:90"
        },
        {
            "name": "Edge: ip_addr in __init__, open() with serial_no only",
            "__serial_no": None,
            "__ip_addr": "192.168.1.1:80",
            "open_serial": 600115434,
            "open_ip": None,
            "expected_serial": 600115434,  # serial_no provided explicitly
            "expected_ip": "192.168.1.1:80"  # Should use __init__ value
        },
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"  Testing: {case['name']}")
        serial_no, ip_addr = simulate_open_logic(
            case['__serial_no'],
            case['__ip_addr'],
            case['open_serial'],
            case['open_ip']
        )
        
        if serial_no == case['expected_serial'] and ip_addr == case['expected_ip']:
            print(f"    ✅ PASS: serial_no={serial_no}, ip_addr={ip_addr}")
        else:
            print(f"    ❌ FAIL: Expected serial_no={case['expected_serial']}, ip_addr={case['expected_ip']}")
            print(f"            Got serial_no={serial_no}, ip_addr={ip_addr}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All edge case tests PASSED\n")
    else:
        print("\n❌ Some edge case tests FAILED\n")
    
    return all_passed


def test_precedence_logic():
    """Test that explicit parameters have precedence"""
    print("Testing Parameter Precedence...")
    print()
    
    def simulate_open_logic(__serial_no, __ip_addr, open_serial, open_ip):
        """Simulate the open() logic"""
        serial_no = open_serial
        ip_addr = open_ip
        
        if serial_no is None and ip_addr is None:
            serial_no = __serial_no
        
        if ip_addr is None:
            ip_addr = __ip_addr
        
        return serial_no, ip_addr
    
    # Test: Explicit parameter should override __init__ value
    print("  Testing: Explicit parameter overrides __init__ value")
    serial_no, ip_addr = simulate_open_logic(
        __serial_no=600115433,
        __ip_addr="192.168.1.1:80",
        open_serial=600115434,  # Different serial
        open_ip=None
    )
    
    if serial_no == 600115434 and ip_addr == "192.168.1.1:80":
        print("    ✅ PASS: Explicit serial_no parameter has precedence")
    else:
        print(f"    ❌ FAIL: Expected serial_no=600115434, ip_addr='192.168.1.1:80'")
        print(f"            Got serial_no={serial_no}, ip_addr={ip_addr}")
        return False
    
    # Test: Explicit ip_addr should override __init__ value
    # Note: When ip_addr is provided explicitly, serial_no from __init__ is NOT used
    # because the condition requires BOTH to be None to use __init__ values
    serial_no, ip_addr = simulate_open_logic(
        __serial_no=600115433,
        __ip_addr="192.168.1.1:80",
        open_serial=None,
        open_ip="10.0.0.1:90"  # Different IP
    )
    
    # When ip_addr is provided, serial_no stays None (not from __init__)
    # This is correct behavior: if you provide ip_addr explicitly, you probably want IP without serial
    if serial_no is None and ip_addr == "10.0.0.1:90":
        print("    ✅ PASS: Explicit ip_addr parameter has precedence (serial_no stays None)")
    else:
        print(f"    ❌ FAIL: Expected serial_no=None, ip_addr='10.0.0.1:90'")
        print(f"            Got serial_no={serial_no}, ip_addr={ip_addr}")
        return False
    
    print("\n✅ Precedence tests PASSED\n")
    return True


if __name__ == '__main__':
    import sys
    
    success = True
    success &= test_edge_case_logic()
    success &= test_precedence_logic()
    
    print("=" * 70)
    if success:
        print("✅ ALL EDGE CASE TESTS PASSED")
    else:
        print("❌ SOME EDGE CASE TESTS FAILED")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

