import sugar
from module import *
from port import * 

###
# Three kinds of tests:
# Crash tests:  the module is just subjected to load and make sure it doesn't crash.
#               you configure the module and drop it.
#               Format: [module instance, number input ports, number output ports]
# Input/output tests: we push in a packet and check what comes out the other side
#               Format: [module instance, number input ports, number output ports,
#                       [{input_port:, packet:, output_port:, packet}, (you can specify a sequence)]
# Custom tests: Just give the master script a function and it will run it. If your function returns zero,
#               we will assume everything worked okay.
###


while True: #wrap in loop to make sure variable names don't leak into master script

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
    OUTPUT_TEST_INPUTS.append([fw3, 1, 1,
        [{'input_port':0, 'input_packet':test_packet, 'output_port':0, 'output_packet':test_packet}]])

    fw4 = ACL(rules=[{'src_ip':'96.0.0.0/8', 'drop':False}])
    test_packet2 = gen_packet(scapy.TCP, '22.22.22.22', '22.22.22.22')
    test_packet3 = gen_packet(scapy.TCP, '96.22.22.22', '22.22.22.22')
    OUTPUT_TEST_INPUTS.append([fw4, 1, 1,
        [{'input_port':0, 'input_packet':test_packet2, 'output_port':0, 'output_packet':None},
        {'input_port':0, 'input_packet':test_packet3, 'output_port':0, 'output_packet':test_packet3}]])

    ## And feel free to add custom functions to test things...
    def my_bonus_acl_test():
        fw5 = ACL(rules=[{'src_ip': '172.12.0.0/16', 'drop': False}, {'dst_ip': '192.168.32.4/32', 'dst_port': 4455, 'src_ip': '134.54.33.2/32', 'drop':False}, {'src_ip':'133.133.133.0/24', 'src_port': 43, 'dst_ip':'96.96.96.155/32', 'dst_port':9, 'drop':False}])
        src = Source()
        rwtemp = [gen_packet(scapy.UDP, "172.12.0.3", "127.12.0.4"), gen_packet(scapy.TCP, "192.168.32.4", "1.2.3.4")]
        src -> Rewrite(templates=rwtemp) -> fw5 -> Sink()
        bess.resume_all()
        time.sleep(15)
        bess.pause_all()
        return 0

    CUSTOM_TEST_FUNCTIONS.append(my_bonus_acl_test)

    break #run the "loop" just once
