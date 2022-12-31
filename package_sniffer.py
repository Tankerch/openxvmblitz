import scapy.all

pkg = scapy.all.sniff(
    filter="dst host 192.168.0.104 and src host 34.120.204.93", count=2)

pkg.nsummary()
