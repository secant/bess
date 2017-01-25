fw = ACL(rules=[{'src_ip': '172.12.0.0/16', 'drop': False}])

CRASH_TEST_INPUTS.append([fw, 1, 1])
