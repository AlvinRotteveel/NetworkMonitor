from threading import Thread
import socket
import sys
from struct import *
from agent.database import add_tcp_packet, add_icmp_packet, add_udp_packet


class SocketCapture(Thread):
    """Threaded capture class with stop() method."""
    def __init__(self):
        super(SocketCapture, self).__init__()
        self.daemon = True
        self.cancelled = False
        try:
            self.s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        except:
            pass

    # receive a packet
    def run(self):
        while not self.cancelled:
            packet = self.s.recvfrom(65565)

            #packet string from tuple
            packet = packet[0]

            #parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH', eth_header)
            eth_protocol = socket.ntohs(eth[2])

            #Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8:
                #Parse IP header
                #take first 20 characters for the ip header
                ip_header = packet[eth_length:20+eth_length]

                #now unpack them :)
                iph = unpack('!BBHHHBBH4s4s', ip_header)

                version_ihl = iph[0]
                version = version_ihl >> 4
                ihl = version_ihl & 0xF

                iph_length = ihl * 4

                ttl = iph[5]
                protocol = iph[6]
                s_addr = socket.inet_ntoa(iph[8])
                d_addr = socket.inet_ntoa(iph[9])

                #TCP protocol
                if protocol == 6:
                    t = iph_length + eth_length
                    tcp_header = packet[t:t+20]

                    #now unpack them :)
                    tcph = unpack('!HHLLBBHHH', tcp_header)
                    
                    source_port = tcph[0]
                    dest_port = tcph[1]
                    sequence = tcph[2]
                    acknowledgement = tcph[3]
                    doff_reserved = tcph[4]
                    tcph_length = doff_reserved >> 4

                    h_size = eth_length + iph_length + tcph_length * 4
                    data_size = len(packet) - h_size

                    #get data from the packet
                    data = packet[h_size:]

                    #Save to sqlite
                    add_tcp_packet('tcp', eth_addr(packet[6:12]), eth_addr(packet[0:6]), str(eth_protocol), 'ipv' + str(version),
                               str(ihl), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port),
                               str(sequence), str(acknowledgement), str(tcph_length))

                #ICMP Packets
                elif protocol == 1:
                    u = iph_length + eth_length
                    icmph_length = 4
                    icmp_header = packet[u:u+4]

                    #now unpack them :)
                    icmph = unpack('!BBH', icmp_header)

                    icmp_type = icmph[0]
                    code = icmph[1]
                    checksum = icmph[2]

                    h_size = eth_length + iph_length + icmph_length
                    data_size = len(packet) - h_size

                    #get data from the packet
                    data = packet[h_size:]

                    #Save to sqlite
                    add_icmp_packet('icmp', eth_addr(packet[6:12]), eth_addr(packet[0:6]), str(eth_protocol), 'ipv' + str(version),
                               str(ihl), str(ttl), str(s_addr), str(d_addr), str(icmp_type), str(code), str(checksum))

                #UDP packets
                elif protocol == 17:
                    u = iph_length + eth_length
                    udph_length = 8
                    udp_header = packet[u:u+8]

                    #now unpack them :)
                    udph = unpack('!HHHH', udp_header)

                    source_port = udph[0]
                    dest_port = udph[1]
                    length = udph[2]
                    checksum = udph[3]

                    h_size = eth_length + iph_length + udph_length
                    data_size = len(packet) - h_size

                    #get data from the packet
                    data = packet[h_size:]

                    #Save to sqlite
                    add_udp_packet('udp', eth_addr(packet[6:12]), eth_addr(packet[0:6]), str(eth_protocol), 'ipv' + str(version),
                               str(ihl), str(ttl), str(s_addr), str(d_addr), str(source_port), str(dest_port), str(length),
                               str(checksum))

                #some other IP packet like IGMP
                else:
                    print('Protocol other than TCP/UDP/ICMP')

    def cancel(self):
        """End this thread"""
        self.cancelled = True

    def update(self):
        """Update the counters"""
        pass

#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr(a):
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (a[0], a[1], a[2], a[3], a[4], a[5])
    return b