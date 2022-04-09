import queue, threading, time

def dzialaj_w_tle ():
    while 1:
        print("dzialam")


def tez ():
    while 1:
        print("tez dzialam")

t1 = threading.Thread(target=dzialaj_w_tle)
t2 = threading.Thread(target=tez)  # WE RE PASSING FUNCTION OBJECT NOT IT"S EXECUTION

t1.start()
t2.start()

t1.join()
t2.join()
