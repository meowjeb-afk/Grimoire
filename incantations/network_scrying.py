"""
Network Scrying Module
Handles network diagnostics, port scanning, and ping operations.
"""
import socket
import psutil
import subprocess
import platform

class NetworkScrying:
    def __init__(self):
        """
        Initializes the Network Scrying engine.
        """
        print("[NetworkScrying] Engine initialized.")

    def get_local_network_map(self):
        """
        Gets basic info about local network interfaces.
        Returns a list of dicts with name, ip, and netmask.
        """
        interfaces = []
        for name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    interfaces.append({
                        "name": name, 
                        "ip": addr.address, 
                        "netmask": addr.netmask
                    })
        return interfaces

    def ping_target(self, host):
        """
        Pings a host and returns the latency or error status.
        """
        print(f"[Processing] Pinging {host}...")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        try:
            result = subprocess.run(
                ['ping', param, '1', host], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                # Extract average time from Windows output format
                output = result.stdout
                if "Average" in output:
                    latency = output.split("Average =")[-1].strip()
                    return f"Online ({latency})"
                return "Online"
            return "Offline / Unreachable"
        except subprocess.TimeoutExpired:
            return "Timeout - Host Unreachable"
        except Exception as e:
            return f"Error: {e}"

    def scan_ports(self, host, ports=None):
        """
        Scans a list of common ports on a target host.
        Returns a list of open port numbers.
        """
        if ports is None:
            ports = [21, 22, 80, 443, 3306, 5432, 8080, 8443]
        
        print(f"[Processing] Scanning ports on {host}...")
        open_ports = []
        socket.setdefaulttimeout(0.5)  # 500ms timeout per port
        
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    if s.connect_ex((host, port)) == 0:
                        open_ports.append(port)
            except Exception:
                pass
        
        print(f"[Success] Found {len(open_ports)} open ports: {open_ports}")
        return open_ports
