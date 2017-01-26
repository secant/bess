
##Make sure every test input has a new module -- no reusing modules between tests.
fw0 = ACL(rules=[{'src_ip': '172.12.0.0/16', 'drop': False}])
CRASH_TEST_INPUTS.append([fw0, 1, 1])

fw1 = ACL(rules=[{'src_ip': '172.12.0.0/16', 'drop': False}, {'dst_ip': '192.168.32.4/32', 'dst_port': 4455, 'src_ip': '134.54.33.2/32', 'drop':False}, {'src_ip':'133.133.133.0/24', 'src_port': 43, 'dst_ip':'96.96.96.155/32', 'dst_port':9, 'drop':False}])
CRASH_TEST_INPUTS.append([fw1, 1, 1])


fw2 = ACL(rules=[{'src_ip':'0.0.0.0/0', 'drop':False}])
CRASH_TEST_INPUTS.append([fw2, 1, 1])

## Format for these:: it will read in all the packets, and then check the expected output. Specify which ports you expect the input and output on.

fw3 = ACL(rules=[{'src_ip':'0.0.0.0/0', 'drop':False}])
test_packet = gen_packet(scapy.TCP, '22.22.22.22', '22.22.22.22')
OUTPUT_TEST_INPUTS.append([fw3, [{'input_port':0, 'input_packet':test_packet, 'output_port':0, 'output_packet':test_packet}]])

