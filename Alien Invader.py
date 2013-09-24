import turtle
import random
import math

score = 0

class LaserCannon(turtle.Turtle):

    def __init__(self):
        super(LaserCannon, self).__init__()

        # Register events.  Note the function we register for 'q' is
        # a turtle function.
        turtle.onscreenclick(self.aim,1)
        turtle.onkey(self.shoot,"s")
        turtle.onkey(seeYaLater,'q')
        

    def aim(self,x,y):
        # Change the heading of the laser turtle to point towards (x,y)
        heading = self.towards(x,y)
        self.setheading(heading)

    def shoot(self):
        # Create a new bomb.  No need to store the bomb in a variable here.
        Bomb(self.heading(), speed=6)


# A BoundedTurtle is a turtle which knows when it reaches the edge of our board.
# It also uses events to keep itself moving.
class BoundedTurtle(turtle.Turtle):
      def __init__(self, speed):
          super(BoundedTurtle, self).__init__()
          self.speed = speed

      def out_of_bounds(self):
          xpos,ypos = self.position()
          out = False
          if xpos < -200 or xpos > 200:
              out = True
          if ypos < 0 or ypos > 200:
              out = True
          return out
      def end_of_screen(self):
          xpos,ypos = self.position()
         # print ("xpos" + str(xpos))
         # print ("ypos" + str(ypos))
          out = False
          if ypos < 0:
              out = True
          return out
                 
      def move(self):
          self.forward(self.speed)
          if self.out_of_bounds():
              self.remove()
          else:
              turtle.ontimer(self.move,200)
          if self.end_of_screen():
              points(1)
              global score
              #print score
              
                
      def remove(self):
          self.hideturtle()

class Alien(BoundedTurtle):

    # We want to store the aliens in a list, and for that we use a static list.
    alienList = []
    @staticmethod
    def getAliens():
        return [x for x in Alien.alienList if x.alive]
        
    def __init__(self, speed):
        super(Alien, self).__init__(speed)
        self.tracer(0)
        self.up()
        self.shape('turtle')

        # The initial position is near the top of the screen
        self.goto(random.randint(-199,199), 190)
        # The initial heading is downwards
        self.setheading(random.randint(250,280))
        self.tracer(1)

        # Filter the global alien list for only those aliens that are alive
        Alien.alientList = [x for x in Alien.alienList if x.alive]
        # Add ourself to the list
        self.alive = True
        Alien.alienList.append(self)

        # Register the initial movement event
        turtle.ontimer(self.move,200)
                    
    def remove(self):
        self.alive = False
        self.hideturtle()
    
class Bomb(BoundedTurtle):

    def __init__(self, init_heading, speed):
        super(Bomb, self).__init__(speed)
        self.color('red','red')
        self.shape('circle')
        self.shapesize(0.4, 0.4)
        self.setheading(init_heading)
        self.up()
        # Start the bomb moving
        turtle.ontimer(self.move,100)
        
    def move(self):
        # First, move the bomb by calling the parent method
        super(Bomb, self).move()

        # Now check for hitting an alien
        for i in Alien.getAliens():
            if self.distance(i) < 5:
                i.remove()
                self.remove()
                points(0)
                global score
                #print score
                
                return
#also checking if hitting an alien game adds ten points
#or reaches the bottom the game subtracts 10
            
    def distance(self,other):
        p1 = self.position()
        p2 = other.position()
        a = p1[0]-p2[0]
        b = p1[1]-p2[1]
        dist = math.sqrt(a**2 + b**2)
        return dist


class AlienInvaders(object):
    def __init__(self):
        turtle.setworldcoordinates(-200,0,200,200)

    def play(self):
        cannon = LaserCannon()
        turtle.ontimer(self.add_alien,2000)
        turtle.listen()

        # Start the event loop.
        turtle.mainloop()

    def add_alien(self):
        # Only add an alien if there are fewer than 5 currently on the board
        if len(Alien.getAliens()) < 5:
            Alien(speed=1)
        turtle.ontimer(self.add_alien,2000)

def seeYaLater():
    global score
    print("Score: "+str(score))
    turtle.bye
    exit(1)

def points(change):
    global score
    if change == 1:
        score = score-10
    else:
        score = score+10

a = AlienInvaders()
a.play()
