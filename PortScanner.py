import socket
import threading

def scan_port(host, port):
    try:
        # Create a Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        # Scan the port
        result = s.connect_ex((host, port))
        
        # If the port is open
        if result == 0:
            service = socket.getservbyport(port)  # Get the service associated with the port
            open_ports.append({"Port": port, "Service": service})  # Add the open port to the list
            print(f"Port {port} is open ({service} service)")
        
        # If the port is closed
        else:
            service = socket.getservbyport(port)
            closed_ports.append({"Port": port, "Service": service})
            print(f"Port {port} is closed ({service} service)")
        
        s.close()

    except KeyboardInterrupt:
        print("\nScanning process canceled by the user.")
        exit()

    except socket.gaierror:
        print("Hostname could not be resolved.")
        exit()

    except socket.error:
        print("Could not connect to the server.")
        exit()

def main():
    target_host = input("Enter the target IP address: ")
    target_ports = input("Enter the port range to scan (e.g., 20-80) or custom port (e.g., 8080): ")

    if '-' in target_ports:
        start_port, end_port = map(int, target_ports.split('-'))
        for port in range(start_port, end_port + 1):
            # Start a new thread for parallel scanning
            thread = threading.Thread(target=scan_port, args=(target_host, port))
            thread.start()
    else:
        custom_port = int(target_ports)
        scan_port(target_host, custom_port)

if __name__ == "__main__":
    open_ports = []  # Create an empty list to store open ports
    closed_ports = []  # Create an empty list to store closed ports
    main()
    # Wait for active threads to finish
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()
    print("Open Ports:")
    for port_info in open_ports:
        print(f"Port: {port_info['Port']}, Service: {port_info['Service']}")
    print("Closed Ports:")
    for port_info in closed_ports:
        print(f"Port: {port_info['Port']}, Service: {port_info['Service']}")
