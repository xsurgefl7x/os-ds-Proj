import Pyro4
import os
import socket


def getPid(o, pid, counter):
        newPid = o.getpid(pid, counter)
        return newPid

def placecalls(o, pid):
        print("Placing database calls....")
        calls = [[pid, "Create", "Water", 1200, 12, 1.00],
                [pid, "Create", "Backpack", 1201, 5, 20.00],
                [pid, "DB"],
                [pid, "Change", "Water", "Name", "Bottled Water"],
                [pid, "Search", "Bottled Water"]]
        for i in range(5):
                o.putWork(calls[i])

def collectresults(o, pid):
        print("Getting back results....")
        counter = 0
        while counter != 5:
                try:
                        result = o.getResult(pid)
                except:
                        pass
                else:
                        counter = counter + 1
                        print(result)

def main():
        o = Pyro4.Proxy("PYRO:server@127.0.0.1:55555") #enter ip address of server.        print("This program simulates a client making calls and changes to a datab$        placecalls(o)
        counter = 0
        pid = os.getpid()
        pid = getPid(o, pid, counter)
        placecalls(o, pid)
        collectresults(o, pid)

if __name__ == "__main__":
    main()
