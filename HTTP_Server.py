import socket
import os 

Server_Host="0.0.0.0"
Server_Port=3009

s=socket. socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)

s.bind(( Server_Host, Server_Port ))
s.listen(5)

print(f"Listing on port {Server_Port}...")

mime_types = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
}

while True:
    Client_Socket , Client_Address =s.accept()
    try:
        request=Client_Socket.recv(1500).decode() 
        print("Request:",request)
        header=request.split('\n')
        if len(header) > 0:
            first_component=header[0].split()
            if len(first_component)>=2:
                http_component=first_component[0]
                path=first_component[1]
                if http_component=="GET":
                    if path == "/" :
                        path="/index.html"

                    file_path = os.path.join(path.strip("/"))

                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        ext = os.path.splitext(file_path)[1]
                        mime_type = mime_types.get(ext,"application/octet-stream")

                        with open(file_path,"rb") as fin:
                            content=fin.read()
                            
                        response = f"HTTP/1.1 200 OK\nContent-Type:{mime_type}\n\n".encode()+ content
                    
                    else:
                        response="HTTP/1.1 404 Not Found \n\nFile not found.".encode()
                
                else :
                    response="HTTP/1.1 405 Method Not Allowed\n\nAllow: GET".encode()
            
            else:
                response="HTTP/1.1 400 Bad Request \n\nInvalid request.".encode()
        
        else:
            response = "HTTP/1.1 400 Bad Request \n\nInvalid request.".encode()
        
        Client_Socket.sendall(response)
    
    except Exception as e:
        print("Error:",e)
        response="HTTP/1.1 500 Internal Server Error\n\nSomething went worng.".encode()
        Client_Socket.sendall(response)

    finally:
        Client_Socket.close()