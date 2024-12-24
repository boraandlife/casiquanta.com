
import os
import sys
import signal

print_input = [""]
def xprint(text, pi):
	pi[0] = text

def db_set():
	print("""
	[1] List Users
	[2] Add Users (Coming Soon)
	[3] Remove Users (Coming Soon)
	[3] Back -->
		""")

	ch = input("[?] : ")

	if ch == '1':
		with open("./instance/db_users.txt", "r") as f:
			file = f.read()
			xprint(file, print_input)
def set_ip():
	input("\n[IP] : ")

def redirect_switch():
	print("""
	[1] Switch On
	[2] Switch Off
	[3] Back -->
		""")

	ch = input("\n[?]: ")

	if ch == "1":
		os.system("screen python3 cqweb.py")
		#os.system('gnome-terminal -x python3 cqweb.py')
	if ch == '2':
		try:
			for line in os.popen("pgrep -f cqweb"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
		except:
			xprint("ProcessLookup Error, no significant problem detected.\n Redirecting to menu...", print_input)

	if ch == '3':
		xprint("Returning to main!", print_input)

def redirect_port():
	print("""
	[1] Static Port (Works After Res)
	[2] Dynamic Port (Sets & Restarts)
	[3] Back -->
	
		""")
	ch = input("\n[?]: ")

	if ch == '1':
		set_port()
	if ch == '2':
		set_port()
		
		try:
			for line in os.popen("pgrep -f cqweb"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
				os.system('screen python3 cqweb.py')
		except:
			xprint("ProcessLookup Error, no significant problem detected.\n Redirecting to menu...", print_input)
			
	if ch == '3':
		print("Returning to main!")

def set_port():
	port_val = input("\n[PORT] : ")
	with open('./instance/pinfo.txt', 'w+') as f:
		f.write(port_val)
		xprint("SET PORT TO : " + port_val, print_input)

    
def prog_exit():
	for line in os.popen("pgrep -f xweb"):
		fields = line.split()
		pid = fields[0]
		os.kill(int(pid), signal.SIGKILL)

def redirect_panel():
	os.system("screen -r")

def wterm():
	ch = None
	print("""
		[1] Python Package Manager
		[2] Terminal Com.
		[3] Back -->

		""")

	ch = input("[?] : ")

	if ch == '1':
		command = input("Enter the package name : ")

		try:
			os.system(f'pip install {command}')
		except:
			xprint("Error Flag ~ Probably invalid syntax...\n Returning to main!",print_input)
	if ch == '2':
		command = input("Enter the command : ")
		try:
			os.system(f'{command}')
		except:
			xprint("Error Flag ~ Probably invalid syntax...\n Returning to main!", print_input)



def edit_ban():
	choices = ['1', '2', '3']
	print("""
		[1] List IPs
		[2] Ban an IP
		[3] Remove an IP
		[4] Back -->

		""")

	ch = input("[?] : ")
	print(" ")
	if ch in choices:
		if ch == '1':
			with open("./instance/ssi.txt","r") as f:
				content = f.read()
				c_list = content.split("@")
			for ip in c_list:
				xprint(ip + "\n", print_input)

		if ch == '2':
			ip = input("[IP] : ")
			c_ip = ip.split(".")
			if len(c_ip) == 4:
				with open('./instance/ssi.txt',"a") as f:
					f.write(str(ip) + "@")
					f.close()
					xprint("Banned conn : " + ip, print_input)
			else:
				xprint("Invalid IP", print_input)


		if ch == '3':
			write_cond = False
			ip = input("[IP] : ")
			c_ip = ip.split(".")
			if len(c_ip) == 4:
				with open("./instance/ssi.txt","r") as f:
					content = f.read()
					
					content2 = content.replace(str(ip) + "@", "")
					
					
					write_cond = True
				if write_cond:
					with open("./instance/ssi.txt","w") as f:
				
						f.write(content2)
						f.close()

						xprint("Removed Adress : " + ip, print_input)

				



def cqterm():
	while True:
		os.system("clear")
		print("""

		███╗   ███╗██╗   ██╗ ██████╗ ███╗   ██╗    ████████╗███████╗ ██████╗██╗  ██╗
		████╗ ████║██║   ██║██╔═══██╗████╗  ██║    ╚══██╔══╝██╔════╝██╔════╝██║  ██║
		██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║       ██║   █████╗  ██║     ███████║
		██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║       ██║   ██╔══╝  ██║     ██╔══██║
		██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║       ██║   ███████╗╚██████╗██║  ██║
		╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝       ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝
		                                                                           
			""")

		print("""
		[1] State On/Off
		[2] Panel
		[3] Change IP Adress (Coming Soon)
		[4] Change Port 
		[5] Ban List 
		[6] Admin List (Coming Soon)
		[7] Database ( Building )
		[8] Terminal
		[9] Exit System
			""")

		
		print("".join(print_input))




		setup = input("[?]: ")
		if setup == '1':
			redirect_switch()
		if setup == '2':
			redirect_panel()
		if setup == '3':
			set_ip()
		if setup == '4':
			redirect_port()
		if setup == '5':
			edit_ban()
		if setup == '6':
			print("Admin List")
		if setup == '7':
			db_set()
		if setup == '8':
			wterm()
		if setup == '9':
			prog_exit()
			sys.exit()

	
	


cqterm()
