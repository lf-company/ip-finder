import random
import socket
import requests
import colorama
from colorama import Fore, Style
import os
import time  # Import the time module

colorama.init()  # Initialize colorama for colored output

def generate_random_ip():
  """Generate a random IPv4 address."""
  return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def check_ip_status(ip, port):
  """Check if the IP address is online and has a web server on the specified port."""
  try:
    # Attempt to connect to the IP address on the specified port
    with socket.create_connection((ip, port), 0.5):
      # Check for content on the web server
      response = requests.get(f"http://{ip}:{port}", timeout=0.5)
      if response.status_code == 200:
        return True, response.text  # Return True and the content
      else:
        return False, ""  # Return False if no web server response
  except (socket.timeout, socket.error):
    return False, ""  # Return False if connection failed

def random_ip_tool():
  """Continuously generates random IPs and checks their status on a user-specified port."""
  port = input("Enter the port to scan (HTTP): ")
  if port == "":
      port = 80
  else:
      port = int(port)
  while True:
    ip = generate_random_ip()
    status, content = check_ip_status(ip, port)
    if status:
      print(f"{Fore.GREEN}IP: {ip} is online on port {port}{Style.RESET_ALL}")
      with open("ip_http.txt", "a") as file:  # Append to the file
        file.write(f"{ip}\n")
    else:
      print(f"{Fore.RED}IP: {ip} is offline on port {port}{Style.RESET_ALL}")

def user_ip_checker():
  """Checks the status of an IP address provided by the user."""
  ip = input("Enter an IP address to check: ")
  port = input("Enter the port to check (leave blank for default 80): ")
  if port == "":
    port = 80
  else:
    port = int(port)
  status, result = check_ip_status(ip, port)
  if status:
    print(f"{Fore.GREEN}IP: {ip} is online on port {port}{Style.RESET_ALL}")
  else:
    print(f"{Fore.RED}IP: {ip} is offline on port {port}{Style.RESET_ALL}")

def ping_ip():
  """Pings a specified IP address until it goes offline."""
  ip = input("Enter an IP address to ping: ")
  while True:
    status = check_ip_status(ip, 443)  # Check on port 443 for HTTPS
    if status:
      print(f"{Fore.GREEN}IP: {ip} is online on port 443{Style.RESET_ALL}")
    else:
      print(f"{Fore.RED}IP: {ip} is offline. Exiting ping loop.{Style.RESET_ALL}")
      break
    time.sleep(0.001)  # Adjust the ping interval as needed

def https_ip_finder():
  """Scans random IPs for HTTPS websites with content."""
  port = input("Enter the port to scan (HTTPS): ")
  if port == "":
      port = 443
  else:
      port = int(port)
  while True:
    ip = generate_random_ip()
    status = check_ip_status(ip, port)
    if status:
      print(f"{Fore.GREEN}IP: {ip} is online on port {port}{Style.RESET_ALL}")
      with open("ip_https.txt", "a") as file:  # Append to the file
        file.write(f"{ip}\n")
    else:
      print(f"{Fore.RED}IP: {ip} is offline on port {port}{Style.RESET_ALL}")

def brutal_ping():
  """Sends a high volume of ICMP (ping) packets to a specified IP address."""
  ip = input("Enter the IP address to ping brutally: ")
  try:
    # Create a raw socket for ICMP packets
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
      # Construct an ICMP echo request packet
      packet = b'\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
      # Convert the IP address to binary
      target_ip = socket.inet_aton(ip)
      # Send the packet
      while True:
        sock.sendto(packet, (ip, 0))
        print(f"Sent ICMP packet to {ip}")
        time.sleep(0.001)  # Adjust the ping interval as needed

  except Exception as e:
    print(f"Error during brutal ping: {e}")

def keyword_http_scanner():
  """Scans random IPs for HTTP websites containing a user-specified keyword."""
  port = input("Enter the port to scan (HTTP): ")
  if port == "":
      port = 80
  else:
      port = int(port)
  keyword = input("Enter the keyword to search for: ")
  while True:
    ip = generate_random_ip()
    status, content = check_ip_status(ip, port)
    if status:
      if keyword in content:
        print(f"{Fore.GREEN}IP: {ip} is online on port {port} and contains '{keyword}'{Style.RESET_ALL}")
        with open("word_ip.txt", "a") as file:  # Append to the file
          file.write(f"{ip}\n")
      else:
        print(f"{Fore.YELLOW}IP: {ip} is online on port {port} but does not contain '{keyword}'{Style.RESET_ALL}")
    else:
      print(f"{Fore.RED}IP: {ip} is offline on port {port}{Style.RESET_ALL}")

while True:
  #os.system('clear') # Clear the terminal screen - this is causing the issue
  print(Fore.GREEN + """
   
      ?forg ip toolkit/
  """ + Style.RESET_ALL)
  print("\nChoose an option:")
  print("1. Random HTTP IP Scanner")
  print("2. User IP Checker")
  print("3. Ping IP")
  print("4. HTTPS IP Finder")
  print("5. Brutal Ping")
  print("6. Keyword HTTP Scanner")
  print("7. Exit")

  choice = input("Enter your choice: ")

  if choice == '1':
    random_ip_tool()
  elif choice == '2':
    user_ip_checker()
  elif choice == '3':
    ping_ip()
  elif choice == '4':
    https_ip_finder()
  elif choice == '5':
    brutal_ping()
  elif choice == '6':
    keyword_http_scanner()
  elif choice == '7':
    break
  else:
    print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")