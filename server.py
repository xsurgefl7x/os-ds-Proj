import Pyro4
import queue
from queue import Queue
from threading import * 

obj = Semaphore()
@Pyro4.expose
@Pyro4.behavior(instance_mode="single") #register object to be processes concurrently.
class Dispatcher(object):
        def __init__(self):
                self.data = queue.Queue()
                self.resultqueue = queue.Queue()
                self.clients = []
                self.datalist = []
                self.resultlist= []

        def putWork(self, item):
                obj.acquire()
                self.data.put(item)
                self.datalist.append(item)
                #print(self.datalist)
                print("item in queue")
                obj.release()
        def getwork(self, timeout = 5):
                while True:
                        try:
                                return self.datalist.pop()
                        except IndexError:
                                pass
        def putResult(self, item):
                obj.acquire()
                self.resultqueue.put(item)
                self.resultlist.append(item)
                print("item in results queue")
                obj.release()
        def getResult(self, client, timeout=5):
                while True:
                        try: 
                                return self.resultlist.pop()
                        except IndexError:
                                pass
        def workqueueSize(self):
                return self.data.qsize()
        def resultQueueSize(self):
                return self.resultqueue.qsize()
        def getpid(self, pid, counter):
                self.clients.append(pid)
                newPid = self.clients.index(pid)
                return newPid

daemon = Pyro4.Daemon(host="127.0.0.1", port=55555) #insert ip address of server, since it will be static
                                                                                                        #added static port

uri = daemon.register(Dispatcher(),"server")
ns = Pyro4.locateNS()
ns.register('obj',uri)
print(uri)

daemon.requestLoop()
