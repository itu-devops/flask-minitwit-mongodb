import sys

for line in sys.stdin:
    if line.startswith("==> dbserver: Assigned IP address:"):
        with open("db_ip.txt", "w") as fp:
            fp.write(line.split()[-1])
    print(line, end="")
