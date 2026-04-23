import Pyro5.server

@Pyro5.server.expose
class PyroService(object):


    @Pyro5.server.oneway
    def hello_word_onew_way(self):
        print("Recebi um pedido de Hello word (oneway)")
        return

    def hello_word(self):
        print("Recebi um pedido de Hello word")
        return "P1 Hello, World!"

daemon = Pyro5.server.Daemon(host="localhost", port=9091)
uri = daemon.register(PyroService())
print(uri)
ns = Pyro5.core.locate_ns()
ns.register("leader", uri) # NameSever - ns
daemon.requestLoop()