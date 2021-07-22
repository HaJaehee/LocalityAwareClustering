
def main():
    clustered_file = open("../korea-37-router-clustered.imn", 'r')
    ip_replacement_file = open("../korea-37-router-clustered-ip-rep.imn", 'w')

    while True:
        line = clustered_file.readline()
        if not line: break
        if "ip address" in line:
            line_split = line.split("ip address ")
            ip_before_mod = line_split[1]
            ip_fields = ip_before_mod.split(".")
            ip_after_mod = ip_fields[0] + "." + ip_fields[2] + "." + ip_fields[1] + "." + ip_fields[3]
            line_after_mod = "\t ip address "+ip_after_mod
            line = line_after_mod
        ip_replacement_file.write(line)

    clustered_file.close()
    ip_replacement_file.close()


if __name__ == "__main__" :
    main ()