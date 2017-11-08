#!/usr/bin/python
import logging
import threading
from Queue import Queue
import time
import optparse

logging.basicConfig(level=logging.DEBUG, format='%(message)s',)

class Consumer(threading.Thread):
    fishDropped = 0
    vegDropped = 0

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group,
                                  target=target,
                                  name=name,
                                  verbose=verbose)
        self.args = args;
        self.condition = self.args[0]
        self.counterQueue = self.args[1]
        self.id = name
        self.chefFinished = False
        self.sushi = ''
        return

    def setChefFinishedWork(self, chefFinished):
        self.chefFinished = chefFinished;

    @classmethod
    def droppedNumbers(cls):
        return (cls.fishDropped, cls.vegDropped)

class Human(Consumer):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):

        Consumer.__init__(self, group, target, name, args, kwargs, verbose)
        self.args = args;
        self.preference = self.args[2]
        return

    def run(self):

        while not self.chefFinished and not self.counterQueue.empty():
            self.sushi = self.counterQueue.get(1)
            if self.preference == 'either' or self.sushi == self.preference:
                # start eating, take 3 second
                time.sleep(3)
                logging.debug('Human ' + str(self.id) + ' takes a piece of '
                              + self.sushi + ' from the counter and eats it')
            else:
                if self.sushi == 'fish':
                    Consumer.fishDropped += 1
                else:
                    Consumer.vegDropped += 1
                logging.debug('Human ' + str(self.id) + ' takes a piece of '
                              + self.sushi
                              + ' from the counter and drops it on the floor')

        return

class Cat(Consumer):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Consumer.__init__(self, group, target, name, args, kwargs, verbose)
        self.args = args;
        self.preference = self.args[2]

        return

    def run(self):

        count = 0

        while not self.chefFinished and not self.counterQueue.empty():
            if count == 2:
                break

            self.sushi = self.counterQueue.get(1)
            if self.sushi != self.preference:
                Consumer.fishDropped += 1
                logging.debug('Cat ' + str(self.id) + ' takes a piece of '
                              + self.sushi + ' from the counter and drops it on the floor')
            else:
                # start eating, take 2 second
                time.sleep(2)
                count += 1
                logging.debug('Cat ' + str(self.id) + ' takes a piece of '
                              + self.sushi + ' from the counter and eats it')

        return

class Chef(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group,
                                  target=target,
                                  name=name,
                                  verbose=verbose)
        self.args = args
        self.condition = self.args[0]
        self.counterQueue = self.args[1]
        self.sushiType = self.args[2]
        self.sushiCount = self.args[3]
        self.humanCustomerCount = self.args[4]
        return

    def run(self):
        if self.humanCustomerCount < 1:
            logging.debug('At least one human customer should be in the restaurant')
        else:
            count = 0
            while not self.counterQueue.full():
                if count == self.sushiCount:
                    break

                logging.debug(self.name + ' puts a piece of ' + self.sushiType + ' on the counter')
                self.counterQueue.put(self.sushiType)
                count += 1
                time.sleep(1)
        return

def parseOpt():
    usage = "usage: %prog [options] -a 2 -b 3 -f 4 -v 5 -e 6 -c 7"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-a", "--alice", action="store", type="int", dest="a", default=2)
    parser.add_option("-b", "--bob", action="store", type="int", dest="b", default=2)
    parser.add_option("-f", "--fish", action="store", type="int", dest="f", default=2)
    parser.add_option("-v", "--veg", action="store", type="int", dest="v", default=2)
    parser.add_option("-e", "--either", action="store", type="int", dest="e", default=2)
    parser.add_option("-c", "--cat", action="store", type="int", dest="c", default=2)

    (options, args) = parser.parse_args()

    print 'The number of pieces of raw fish sushi Alice will make: ', options.a
    print 'The number of pieces of vegetarian sushi Bob will make: ', options.b
    print 'The number of human consumers who prefer fish sushi: ', options.f
    print 'The number of human consumers who prefer vegetarian sushi: ', options.v
    print 'The number of human consumers who will eat either: ', options.e
    print 'The number of cats that have managed to get into the restaurant: ', options.c

    return (options.a, options.b, options.f, options.v, options.e, options.c)

def main():
    (a, b, f, v, e, c) = parseOpt()
    humanCustomerCount = f + v + e

    condition = threading.Condition()
    BUF_SIZE = 100
    q = Queue(BUF_SIZE)

    chefs = []
    # Alice
    if a > 0 and humanCustomerCount > 0:
        aliceThread = Chef(name='alice', args=(condition, q,'fish', a, humanCustomerCount))
        aliceThread.start()
        chefs.append(aliceThread)

    # Bob
    if b > 0 and humanCustomerCount > 0:
        bobThread = Chef(name='bob', args=(condition, q,'veg', b, humanCustomerCount))
        bobThread.start()
        chefs.append(bobThread)


    customers = []
    if f > 0:
        for i in range(1, f, 1):
            humanFishThread = Human(name=i, args=(condition, q, 'fish'))
            humanFishThread.start()
            customers.append(humanFishThread)
    time.sleep(1)

    if v > 0:
        for j in range(f+1, f+v, 1):
            humanVegThread = Human(name=j, args=(condition, q, 'veg'))
            humanVegThread.start()
            customers.append(humanVegThread)
    time.sleep(1)

    if e > 0:
        for k in range(f+v+1, f+v+e, 1):
            humanEitherThread = Human(name=k, args=(condition, q, 'either'))
            humanEitherThread.start()
            customers.append(humanEitherThread)
    time.sleep(1)

    if c > 0:
        for i in range(1, c, 1):
            catThread = Cat(name=i, args=(condition, q, 'fish'))
            catThread.start()
            customers.append(catThread)
    time.sleep(1)

    for chef in chefs:
        chef.join()

    for customer in customers:
        customer.setChefFinishedWork(True)
        customer.join()

    (fishDropped, vegDropped) = Consumer.droppedNumbers()
    logging.debug(str(fishDropped) + ' pieces of fish sushi were dropped on the floor')
    logging.debug(str(vegDropped) + ' pieces of vegetarian sushi were dropped on the floor')
    logging.debug('Program completed: all producer and consumer threads finished')
    return

if __name__ == "__main__":
    main()