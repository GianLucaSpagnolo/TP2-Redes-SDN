import json


def read_field(rule, field):
    if field in rule:
        return rule[field]
    return None


def main():
    file = open('config.json')
    config = json.load(file)
    file.close()
    rules = config["rules"]

    for rule in rules:
        print(rule)
        print("Port: ", read_field(rule, "dst_port"))
        print("Source IP: ", read_field(rule, "src_ip"))
        print("Destination IP: ", read_field(rule, "dst_ip"))
        print("Transport Protocol: ", read_field(rule, "transport_protocol"))
        print("IP Protocol: ", read_field(rule, "ip_version"))
        print("\n")

main()