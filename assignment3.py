def convertHexToDecimal(HexList):
    i = 0
    for HexByte in HexList:
        newDecimalInt = int(HexByte,16)
        HexList[i] = newDecimalInt
        i += 1
    result = '.'.join(str(i) for i in HexList)
    return(result)

    print("_" * 48)

frame1HexList = []
frame2HexList = []
frame3HexList = []


UpperLayerProtocolDict = {
    "0800": "IPv4",
    "87DD": "IPv6",
    "0806": "ARP"
}

ProtocolsEncapsulatedByIPv4Dict= {
    "01": "ICMP",
    "02": "IGMP",
    "06": "TCP",
    "11": "UDP"
}

PortNumbersEncapsulatedByTcpUdpDict = {
    "0014": "FTP",
    "0016": "SSH",
    "0017": "TELNET",
    "0019": "Email SMTP",
    "0035": "DNS",
    "0050": "HTTP",
    "008F": "IMAP",
    "00A1": "SNMP",
    "00B3": "BGP",
    "0208": "RIP",
    "01BB": "HTTPS",
    "0387": "VMware Remote Console"
}

mac_address_length = 6
ipv4_header_length = 20

def getFrameInformation(frame_file, hex_list):
    with open(frame_file) as frame:
        hex_list.extend(frame.read().split())
        # this block below gets src and dest mac address
        DestinationMac = '-'.join(hex_list[:mac_address_length])
        SourceMac = '-'.join(hex_list[mac_address_length : 2 * mac_address_length])
        print("\n\n\n")
        print(frame_file.center(48))
        print("-" * 48)
        print("Ethernet Protocol".center(48))
        print("Destination MAC: {:>28}".format(DestinationMac.upper())) # for debug
        print("Source MAC: {:>33}".format(SourceMac.upper())) # for debug
        
        # this block gets the upper layer protocol 
        upperLayerProtocolHex = hex_list[12] + hex_list[13] 
        protocol = UpperLayerProtocolDict[upperLayerProtocolHex]
        print("-" * 48)
        print("{} Protocol".format(protocol).center(48))
        
        # This block gets the IP header information, gets everything after the 14'th item
        # upperLayerInformation = hex_list[14 : 14 + ipv4_header_length]
        upperLayerInformation = hex_list[14:]

        #calls thed IPv4 frame information function
        if protocol == "IPv4":
            getIPv4FrameInformation(upperLayerInformation)
        elif protocol == "IPv6":
            getIPv6FrameInformation(upperLayerInformation)
        else:
            getARPFrameInformation(upperLayerInformation)
            

def getIPv4FrameInformation(IPv4Frame):
    
    SrcIpAddr = convertHexToDecimal(IPv4Frame[12:16])
    DestIpAddr = convertHexToDecimal(IPv4Frame[16:20])
    print("Source IPv4 Address: {:>20}".format(SrcIpAddr))
    print("Destination IPv4 Address: {:>16}".format(DestIpAddr))
    
    
    protocol = ProtocolsEncapsulatedByIPv4Dict[IPv4Frame[9]]
    print("-" * 48)
    print("{} Protocol".format(protocol).center(48))
    
    ProtocolEncapsulatedByIPv4ByteList = IPv4Frame[20:]


    if protocol == "TCP":
        tcpHeader(ProtocolEncapsulatedByIPv4ByteList)

    elif protocol == "UDP":
        udpHeader(ProtocolEncapsulatedByIPv4ByteList)

    
    
def getIPv6FrameInformation(IPv6Frame):
    None
    
    
def getARPFrameInformation(ARPFrame):
    None
    
    
def tcpHeader(tcpFrame):
    SrcPort = ''.join(tcpFrame[:2])
    DestPort = ''.join(tcpFrame[2:4])
    
    print("Source Port: {:>18} ".format(int(SrcPort, 16)))
    print("Destination Port: {:>15} ".format(int(DestPort, 16)))
    
    port = PortNumbersEncapsulatedByTcpUdpDict[SrcPort.upper()]
    
    print("-" * 48)
    print("\n{} Protocol\n".format(port).center(48))
    print("-" * 48)
    
def udpHeader(udpFrame):
    SrcPort = ''.join(udpFrame[2:4])
    DestPort = ''.join(udpFrame[:2])
    
    print("Source Port: {:>22} ".format(int(DestPort, 16)))
    print("Destination Port: {:>14} ".format(int(SrcPort, 16)))
    
    port = PortNumbersEncapsulatedByTcpUdpDict[SrcPort.upper()]
    
    print("-" * 48)
    print("\n{} Protocol\n".format(port).center(48))
    print("-" * 48)

getFrameInformation('assignment3/frame1.txt', frame1HexList)
# getFrameInformation('assignment3/frame2.txt', frame2HexList)
getFrameInformation('assignment3/frame3.txt', frame3HexList)
