import asyncio
from asyncio import transports


class ClientProtocol(asyncio.Protocol):
    login: str
    server: 'Server'
    transport: transports.Transport

    def __init__(self, server: 'Server'):
        self.server = server
        self.login = None

    def data_received(self, data: bytes):
        decoded = data.decode()
        print(f"-------{decoded}")

        if self.login is None:
            # login: User
            print(self.server.clients[0].login)
            if decoded.startswith("login:"):
                self.login = decoded.replace("login:", "").replace("\r\n", "")
                for client in self.server.clients:
                    if client == self.server.clients[-1]:
                        self.transport.write(
                            f"Hello, {self.login}!".encode()
                        )
                        self.send_history()
                    elif client.login == self.login:
                        self.transport.write(
                            f"Login <{self.login}> is already taken!".encode()
                        )
                        # self.server.clients.pop(-1)
                        self.transport.close()
                        # self.connection_lost(client)
            else:
                print("Please login first!")
        else:
            self.send_message(decoded)

        for i, client in enumerate(self.server.clients):
            print(f"{i} - {client.login}")

    def send_message(self, message):
        format_string = f"<{self.login}> {message}\n"
        # save messages to list in Server
        self.server.messages.append(format_string)
        encoded = format_string.encode()

        for client in self.server.clients:
            if client.login != self.login:
                client.transport.write(encoded)

    def send_history(self):
        last_messages = self.server.messages[-10:]

        for message in last_messages:
            self.transport.write(message.encode())

    def connection_made(self, transport: transports.Transport):
        self.transport = transport
        self.server.clients.append(self)
        print("Connection on")

    def connection_lost(self, exception):
        self.server.clients.remove(self)
        print("Connection lost")


class Server:
    clients: list
    messages: list

    def __init__(self):
        self.clients = []
        self.messages = []

    def create_protocol(self):
        return ClientProtocol(self)

    async def start(self):
        loop = asyncio.get_running_loop()

        coroutine = await loop.create_server(
            self.create_protocol,
            "127.0.0.1",
            8888,
        )
        print("Server is running")
        await coroutine.serve_forever()


process = Server()
try:
    asyncio.run(process.start())
except KeyboardInterrupt:
    print("Server was shut down by yours")
