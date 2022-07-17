import pygame
import random

# Constants
WIDTH, HEIGHT = 500, 535 # Height extra for score display
BLOCK = 20
FPS = 10

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Create surface window
pygame.display.set_caption("Snake Game") # Name of tab

# RGB Pixels
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)

# Make grid
def createGrid():
    for x in range(0, WIDTH, BLOCK):
        for y in range(0, HEIGHT - 35, BLOCK):
            grid = pygame.Rect(x, y, BLOCK, BLOCK)
            pygame.draw.rect(WIN, WHITE, grid, 1)

# Snake head
class SnakeOne(pygame.sprite.Sprite):
    # Initialize snake
    def __init__(self, x, y, direction): # make player later...
        super().__init__()
        self.image = pygame.Surface([BLOCK, BLOCK])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = [self.x, self.y]
        self.direction = direction
    # Move snake
    def move(self):
        if self.direction == "Right":
            self.x = self.x + 20
            self.rect.move_ip(20, 0)
        elif self.direction == "Left":
            self.x = self.x - 20
            self.rect.move_ip(-20, 0)
        elif self.direction == "Up":
            self.y = self.y - 20
            self.rect.move_ip(0, -20)
        elif self.direction == "Down":
            self.y = self.y + 20
            self.rect.move_ip(0, 20)
    # Get direction
    def getDirection(self):
        return self.direction
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    # Change direction
    def changeDirection(self, newDirection):
        self.direction = newDirection

# Snake tail
class TailSegment(pygame.sprite.Sprite):
    # Tail segment
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK, BLOCK])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.prevX = 0
        self.prevY = 0
        self.rect.center = [self.x, self.y]
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getPrevX(self):
        return self.prevX
    def getPrevY(self):
        return self.prevY
    def move(self, direction, position):
        if direction == "X":
            self.prevX = self.x
            self.prevY = self.y
            self.x = self.x + position
        elif direction == "Y":
            self.prevX = self.x
            self.prevY = self.y
            self.y = self.y - position

# Food or point class
class Food(pygame.sprite.Sprite):
    # Point sprite
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK, BLOCK])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = [self.x, self.y]
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setCoordinates(self, newX, newY):
        self.x = newX
        self.y = newY

# Display score
def showScore(x, y, score, highScore):
    font = pygame.font.Font('freesansbold.ttf', 30)
    scoreDisplay = font.render("SCORE: " + str(score), True, YELLOW)
    WIN.blit(scoreDisplay, (x, y))
    highScoreDisplay = font.render("BEST: " + str (highScore), True, YELLOW)
    WIN.blit(highScoreDisplay, (x + 340, y))

# Menu screen
def menuScreen():
    font = pygame.font.Font('freesansbold.ttf', 60)
    startDisplay = font.render("START", True, GREEN)
    start_rect = startDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    WIN.blit(startDisplay, start_rect)
    exitDisplay = font.render("EXIT", True, GREEN)
    exit_rect = exitDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
    WIN.blit(exitDisplay, exit_rect)

# Dead screen
def defeatScreen(score, highScore):
    font = pygame.font.Font('freesansbold.ttf', 60)
    scoreDisplay = font.render("SCORE: " + str(score), True, YELLOW)
    score_rect = scoreDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 - 150))
    WIN.blit(scoreDisplay, score_rect)
    highScoreDisplay = font.render("BEST: " + str(highScore), True, YELLOW)
    highScore_rect = highScoreDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    WIN.blit(highScoreDisplay, highScore_rect)
    tryDisplay = font.render("TRY AGAIN", True, GREEN)
    try_rect = tryDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    WIN.blit(tryDisplay, try_rect)
    exitDisplay = font.render("EXIT", True, GREEN)
    exit_rect = exitDisplay.get_rect(center=(WIDTH/2, HEIGHT/2 + 150))
    WIN.blit(exitDisplay, exit_rect)

def main():
    # Start
    pygame.init()
    
    mouse = pygame.mouse.get_pos()
    # Menu
    inMenu = True
    while inMenu:
        menuScreen()
        pygame.display.update()
        for event in pygame.event.get(): # Check for events occurring in game
            if event.type == pygame.QUIT: # Exit out loop
                pygame.quit()
                inMenu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] <= WIDTH / 2 + 100 and mouse[0] >= WIDTH / 2 - 100:
                    if mouse[1] >= HEIGHT / 2 + 50 and mouse[1] <= HEIGHT - 100:
                        pygame.quit()
                    elif mouse[1] <= HEIGHT / 2 - 50 and mouse[1] >= 100:
                        inMenu = False
                
    # Declare clock object
    clock = pygame.time.Clock()
    # Set loop
    run = True
    # Set score
    score = 0
    highScore = 0

    # Make snake head and tail
    snakes_list = pygame.sprite.Group()
    snakeOne = SnakeOne(90, 250, "Right")
    snakes_list.add(snakeOne)
    snakeOneTail = [TailSegment(70, 250), TailSegment(50, 250)]
    for segment in snakeOneTail:
        snakes_list.add(segment)
    
    # Initial point
    apple = Food(410, 250)
    snakes_list.add(apple)

    # Game loop
    while run:
        createGrid()
        clock.tick(FPS) # Run event for loop at 10 FPS
        moveInput = True
        for event in pygame.event.get(): # Check for events occurring in game
            if event.type == pygame.QUIT: # Exit out loop
                run = False 
            if event.type == pygame.KEYDOWN: # Check player input
                if moveInput:
                    if event.key == pygame.K_a:
                        if snakeOne.getDirection() != "Right":
                            snakeOne.changeDirection("Left")
                            moveInput = False
                    if event.key == pygame.K_d:
                        if snakeOne.getDirection() != "Left":
                            snakeOne.changeDirection("Right")
                            moveInput = False
                    if event.key == pygame.K_w:
                        if snakeOne.getDirection() != "Down":
                            snakeOne.changeDirection("Up")
                            moveInput = False
                    if event.key == pygame.K_s:
                        if snakeOne.getDirection() != "Up":
                            snakeOne.changeDirection("Down")
                            moveInput = False
        snakes_list.update()
        # Erase traces of the snake
        WIN.fill(BLACK)
        # Draw the snake
        snakes_list.draw(WIN)
        # Redraw grid
        createGrid()
        showScore(5, 505, score, highScore)
        # Move snake and save previous position
        prevX = snakeOne.getX()
        prevY = snakeOne.getY()
        snakeOne.move()
        # Tail logic
        for index in range(len(snakeOneTail)):
            if index == 0:
                prevTailX = snakeOneTail[index].getX()
                prevTailY = snakeOneTail[index].getY()
                if snakeOneTail[index].getX() < prevX:
                    snakeOneTail[index].move("X", 20)
                    snakeOneTail[index].rect.move_ip(20, 0)
                elif snakeOneTail[index].getX() > prevX:
                    snakeOneTail[index].move("X", -20)
                    snakeOneTail[index].rect.move_ip(-20, 0)
                elif snakeOneTail[index].getY() < prevY:
                    snakeOneTail[index].move("Y", -20)
                    snakeOneTail[index].rect.move_ip(0, 20)
                elif snakeOneTail[index].getY() > prevY:
                    snakeOneTail[index].move("Y", 20)
                    snakeOneTail[index].rect.move_ip(0, -20)
            else:
                if snakeOneTail[index].getX() < snakeOneTail[index - 1].getPrevX():
                    snakeOneTail[index].move("X", 20)
                    snakeOneTail[index].rect.move_ip(20, 0)
                    prevTailX = prevTailX + 20
                elif snakeOneTail[index].getX() > snakeOneTail[index - 1].getPrevX():
                    snakeOneTail[index].move("X", -20)
                    snakeOneTail[index].rect.move_ip(-20, 0)
                    prevTailX = prevTailX - 20
                elif snakeOneTail[index].getY() < snakeOneTail[index - 1].getPrevY():
                    snakeOneTail[index].move("Y", -20)
                    snakeOneTail[index].rect.move_ip(0, 20)
                    prevTailX = prevTailX - 20
                elif snakeOneTail[index].getY() > snakeOneTail[index - 1].getPrevY():
                    snakeOneTail[index].move("Y", 20)
                    snakeOneTail[index].rect.move_ip(0, -20)
                    prevTailX = prevTailX + 20
        # Lose conditions
        if snakeOne.getX() > WIDTH or snakeOne.getX() < 0 or snakeOne.getY() > HEIGHT - 35 or snakeOne.getY() < 0:
            run = False
            WIN.fill(BLACK)
        for segment in snakeOneTail:
            if snakeOne.getX() == segment.getX() and snakeOne.getY() == segment.getY():
                run = False
                WIN.fill(BLACK)
        
        # Defeat screen
        while run == False:
            defeatScreen(score, highScore)
            pygame.display.update()
            for event in pygame.event.get(): # Check for events occurring in game
                if event.type == pygame.QUIT: # Exit out loop
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] <= WIDTH / 2 + 100 and mouse[0] >= WIDTH / 2 - 100:
                        if mouse[1] >= HEIGHT / 2 and mouse[1] <= HEIGHT / 2 + 100:
                            snakes_list.empty()
                            snakeOne = SnakeOne(90, 250, "Right")
                            snakes_list.add(snakeOne)
                            snakeOneTail = [TailSegment(70, 250), TailSegment(50, 250)]
                            for segment in snakeOneTail:
                                snakes_list.add(segment)
                            apple = Food(410, 250)
                            snakes_list.add(apple)
                            score = 0
                            WIN.fill(BLACK)
                            # snakes_list.draw(WIN)
                            run = True
                        elif mouse[1] <= HEIGHT - 100 and mouse[1] > HEIGHT / 2 + 100:
                            pygame.quit()

        # Apple eaten
        if apple.getX() == snakeOne.getX() and apple.getY() == snakeOne.getY():
            score += 1
            randX = random.randrange(0, 500, 20) + 10
            randY = random.randrange(0, 500, 20) + 10
            

            index = 0
            while index < (score + 1):
                for segment in snakeOneTail:
                    if randX == segment.getX() and randY == segment.getY() or (randX == apple.getX() and randY == apple.getY()):
                        randX = random.randrange(0, 500, 20) + 10
                        randY = random.randrange(0, 500, 20) + 10
                        index = -1
                index = index + 1
            apple.rect.update(randX - 10, randY - 10, 20, 20)
            apple.setCoordinates(randX, randY)
            if score > highScore:
                highScore += 1
            snakeOneTail.append(TailSegment(snakeOneTail[score].getPrevX(), snakeOneTail[score].getPrevY()))
            snakes_list.add(snakeOneTail[score + 1])
        # Update display
        pygame.display.update()
    pygame.quit() # Exit out

if __name__ == "__main__": # We only run the main function if the file was run directly
    main()

