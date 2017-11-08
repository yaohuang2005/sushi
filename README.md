Sushi! (in Python)

X consumers walk into a sushi restaurant. In the restaurant, there are two chefs, Alice and Bob.
Alice specializes in making sushi with raw fish, Bob in vegetarian sushi.
Consumers can be either humans, or cats. Cats always prefer raw fish, but get full after two
pieces of sushi. (The cats will even eat the rice, as long as there’s fish on it!) On the other
hand, the humans will eat as much sushi as they can. Some humans prefer raw fish, some
vegetarian, and some will consume either.

There is a counter. A maximum of 100 pieces of sushi can fit on a counter. Chefs will prepare
sushi in parallel, each working on their preferred kind. The Chefs take 1s to produce a piece of
sushi. Over the course of the evening, Alice will make A pieces of sushi and Bob will make B.
The consumers will try to grab sushi from the counter as soon as it’s available. If the sushi they
grab is not of their preferred choice, they’ll drop the sushi on the floor without eating it.
Otherwise, humans will spend 3s eating it, during which time, they won’t attempt to grab more
sushi. (Cats are faster. They’ll eat the sushi in 2s.) Then, if they’re still hungry, they’ll try to grab
more sushi from the counter.

The sushi never expires, and will sit on the counter until a consumer grabs it.

It should print out the sequence of actions that takes place, e.g. “Alice puts a piece of fish sushi on the counter”, “Cat 2takes a piece of vegetarian sushi from the counter and drops it on the floor.” 

At the end of the simulation, we would like to know how many sushi pieces were dropped on the floor.
Inputs to the simulation are:
­ The number of pieces of raw fish sushi Alice will make (A)
­ The number of pieces of vegetarian sushi Bob will make (B)
­ The number of human consumers who prefer fish sushi (F)
­ The number of human consumers who prefer vegetarian sushi (V)
­ The number of human consumers who will eat either (E)
­ The number of cats that have managed to get into the restaurant (C)


Instruction: 
1. Ensure your Linux or Mac has Python installation (version 2.7 is good), 
2. Copy the sushi.py to a directory
3, Change directory to that directory by cd command
4. Run command: chmod 755 sushi.py
5. Execute:            ./sushi.py -a 2 -b 3 -f 1
6. Then you will get output on the standout (screen)

You can also get help for the command line options by:   ./sushi.py -h