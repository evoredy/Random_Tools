import sys
import json

def parse_log_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    num_lines = len(lines)
    callerID_packets = []
    current_packet = {}
    packet_counter = 1
    for line in lines:
        if line.startswith("DATE"):
            current_packet["DATE"] = line.strip().split('=')[1]
        elif line.startswith("TIME"):
            current_packet["TIME"] = line.strip().split('=')[1]
        elif line.startswith("NMBR"):
            current_packet["NMBR"] = line.strip().split('=')[1]
        elif line.startswith("NAME"):
            current_packet["NAME"] = line.strip().split('=')[1]
            if len(current_packet) == 4:
                current_packet = {"packet_number": packet_counter, **current_packet}
                callerID_packets.append(current_packet)
                current_packet = {}
                packet_counter += 1

    return callerID_packets

def save_packets_to_file(packets, output_filename):
    data = {"callerID_packets": packets}
    with open(output_filename, 'w') as file:
        json.dump(data, file, indent=4)

def print_packets(packets):
    for packet in packets:
        packet = {"packet_number": packet["packet_number"], **packet}
        json_packet = json.dumps(packet, indent=4)
        print(json_packet)

if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Please provide the log filename and optionally the output filename as arguments.')
    else:
        filename = sys.argv[1]
        packets = parse_log_file(filename)

        if len(sys.argv) == 3:
            output_filename = sys.argv[2]
            save_packets_to_file(packets, output_filename)
            print(f"Packets saved to '{output_filename}' successfully.")
        else:
            print_packets(packets)
