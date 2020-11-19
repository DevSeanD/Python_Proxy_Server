"""
Sean Dever
11/11/20
Proxy Server
This proxy server uses the command curl. curl is available on mac os and linux. It can be installed on windows as well. I do not create a client, instead I use the webbrower as the client.

The simple command "curl URL > filename.html" will download the html file at that url and pipe the output to the filename.html file. The remaining work involves creating a tcp server.

***The HOST value must be updated to your IP or local address
    For IP I like to use the command "ifconfig | grep inet". This command runs ifconfig and then piping the output to grep to parse for "inet".
"""
import socket
import os #needed inorder to execute curl

class tcpWebServer:
    rootDir = './/'
    HOST = '192.168.1.89' #add your IP or local host(127.0.0.1)


    def configure(self,port,homePage):
        self.PORT = port
        self.pageNotFound = '404.html'

    def get_content_type(self,exten):
        if exten.find(".html") >= 0 or exten.find(".htm") >= 0: #the only file extension needed for now
                print("if statement works")
                return "text/html"
        return "text/html" #default case

    def handle_request(self,connec,request):
        requestFileName = "/" + request
        parts = request.split()
        requestFileName = parts[1]
        requestFileName = requestFileName[1:]
        fullFileName = tcpWebServer.rootDir+requestFileName
        print("Request: ", fullFileName)

        if not os.path.exists(requestFileName):
            os.system("wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains example.com " + requestFileName)

        fileExten = request.split('.')[-1]
        print(fileExten)
        contentType = self.get_content_type(fileExten)
        data = self.load_binary(requestFileName + "/index.html")
        httpStatusCode = 200
        self.server_response(connec,httpStatusCode,self.get_message(httpStatusCode),data,contentType)

    def get_message(self,code):
        codeMessages = {200: "OK", 404: "Not Found"}
        return codeMessages[code]

    def load_file(self,file):
        f = open(file)
        data = f.read()
        return data

    def load_binary(self,file):
        with open(file,'rb') as file:
            return file.read()

    def server_response(self,connec,code,message,content,contentType):
        response = 'HTTP/1.1' + str(code) + " " + message + '\r\n'
        response += 'Content-Type: ' + contentType + '\r\n'
        response += 'Content-Length: ' +str(len(content)) + '\r\n'
        response += '\r\n'

        connec.send(response.encode() + content)

    def start_server(self):
        listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        listen_socket.bind((self.HOST, self.PORT))
        listen_socket.listen(1)
        print('Listening on IP {} and Port {}'.format(self.HOST,self.PORT))

        while True:
            try:
                client_connec,client_addr = listen_socket.accept()
                request = client_connec.recv(1024)
                request = request.decode()
                print("From Client: ",request)
                self.handle_request(client_connec,request)
                client_connec.close()
            except IOError:
                print("Error: ",IOError)


if __name__ == "__main__":
    PORT = 8082
    homePage='/google.html'

    webServer = tcpWebServer()
    webServer.configure(PORT,homePage)

    webServer.start_server()
