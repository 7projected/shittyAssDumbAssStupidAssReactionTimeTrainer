import pygame, sys, random as rand, assets.info as info, time

# Setup pygame
pygame.init()
windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()
iconTexture = pygame.image.load("assets/icon.png")
pygame.display.set_icon(iconTexture)
pygame.display.set_caption("Reaction Time Trainer")
fps = 60
font = pygame.font.Font('assets/font.ttf', 32)
sprites = []

class Timer:
    timers = []
    
    def __init__(self, duration):
        self.duration = duration
        self.start_time = time.time()

        self.addToTimers()

    def addToTimers(self):
        Timer.timers.append(self)

    def getTimeLeft(self):
        elapsed_time = time.time() - self.start_time
        time_left = max(0, self.duration - elapsed_time)
        return time_left
            
    def ended(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.duration

class HitBox:
    list = []
    
    def __init__(self, position=(0,0), size=(64,64),hitsNeeded=1):
        self.position = position
        self.hitsLeft = hitsNeeded
        self.size = size
        self.outline = pygame.image.load("assets/squareOutline.png")
        self.inline = pygame.Surface(self.size)
        self.inline.fill(info.hitboxColor)
        
        self.displayText  = font.render(str(self.hitsLeft), True, info.fontColor)
        self.textRect = self.displayText.get_rect()
        self.textRect.center = ((self.position[0] + self.size[0] / 2), (self.position[1] + self.size[1] / 2))

        self.hovering = False

        self.addToList()
    
    def addToList(self):
        sprites.append(self)
        HitBox.list.append(self)

    def removeFromList(self):
        sprites.remove(self)
        HitBox.list.remove(self)
        
    def checkMousePos(self):
        mousePos = pygame.mouse.get_pos()
        
        if mousePos[0] >= self.position[0] and mousePos[0] <= self.position[0] + self.size[0] and mousePos[1] >= self.position[1] and mousePos[1] <= self.position[1] + self.size[1]:
            self.hovering = True
        else:
            self.hovering = False  

    def input(self):
        self.checkMousePos()
        if self.hovering:
            self.hitsLeft -= 1

    def draw(self):
        self.displayText = font.render(str(self.hitsLeft), True, info.fontColor)
        
        self.outline = pygame.transform.scale(self.outline, self.size)
        screen.blit(self.inline, self.position)
        screen.blit(self.outline, self.position)
        screen.blit(self.displayText, self.textRect)

        if self.hitsLeft <= 0:
            Scene.score += 1
            self.removeFromList()

class Spawn:
    def check():
        # this checks if there is an empty one
        currentAmount = 0
        
        for hitbox in HitBox.list:
            currentAmount += 1
        
        return currentAmount

    def spawn():
        spawnPos = (rand.randint(0, 1280 - info.hitBoxSize), rand.randint(0,720 - info.hitBoxSize))
        max = info.maxHits
        size =info.hitBoxSize
        hitsNeeded = rand.randint(1, info.maxHits)
        hb = HitBox(spawnPos, (size,size), hitsNeeded)

class Button:
    buttons = []
    
    def __init__(self, position=(0,0), size=(200,50), text=("button")):
        self.position = position
        self.size = size
        self.text = text
        self.rect = pygame.Surface(self.size)
        self.rect.fill(info.buttonColor)
        self.pressed = False
        self.hovering = False
        
        self.addToList()
        
    def addToList(self):
        Button.buttons.append(self)
    
    def mouse(self):
        mousePos = pygame.mouse.get_pos()
        
        if mousePos[0] >= self.position[0] and mousePos[0] <= self.position[0] + self.size[0] and mousePos[1] >= self.position[1] and mousePos[1] <= self.position[1] + self.size[1]:
            self.hovering = True
        else:
            self.hovering = False
    
    def click(self):
        self.mouse()
        if self.hovering:
            self.pressed = True
        else:
            self.pressed = False
        
    def draw(self):
        self.displayText  = font.render(str(self.text), True, info.fontColor)
        self.textRect = self.displayText.get_rect()
        self.textRect.center = (((self.position[0] + self.size[0] / 2)), ((self.position[1] + self.size[1] / 2)))
        screen.blit(self.rect, self.position)
        screen.blit(self.displayText, self.textRect)

class GUI:
    ResultsScreenMainMenuButton = Button((1280 / 2 - 100, 720/2 + 80), (200,50), "Main Menu")
    MainMenuPlayButton = Button((1280/2 - 100, 720/2), (200,50), "Play")
    
    def ResultsLogic():
        if GUI.ResultsScreenMainMenuButton.pressed:
            Scene.showMenu()
    
    def Results():
        displayText  = font.render(str("Score is: " + str(Scene.score)), True, info.fontColor)
        textRect = displayText.get_rect()
        textRect.center = ((1280 / 2), (720 / 2))
        
        GUI.ResultsScreenMainMenuButton.draw()
        
        screen.blit(displayText, textRect)
        
        for box in HitBox.list:
            box.removeFromList()
    
    def MainMenuLogic():
        if GUI.MainMenuPlayButton.pressed:
            Scene.play()
        
    def MainMenu():
        displayText  = font.render(str("Shitty Ass ReactionTime Trainer"), True, info.fontColor)
        textRect = displayText.get_rect()
        textRect.center = ((1280 / 2), (720 / 2 - 100))

        screen.blit(displayText, textRect)
        
        GUI.MainMenuPlayButton.draw()
        
        for box in HitBox.list:
            box.removeFromList()

class Scene:
    score = 0
    playTimer = Timer(0)
    current = "main_menu" # PLAY, RESULTS, MAIN_MENU
    
    def play():
        Scene.playTimer = Timer(info.playTime)
        Scene.current = "play"
    
    def showResults():
        Scene.playTimer = Timer(0)
        Scene.current = "results"
    
    def showMenu():
        Scene.playTimer = Timer(0)
        Scene.current = "main_menu"
        Scene.score = 0
    
    def control():
        if Scene.playTimer.ended() and Scene.current == "play":
            Scene.showResults()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in HitBox.list:
                box.input()
            for button in Button.buttons:
                button.click()
    
    # LOGIC
    
    if Scene.current == "results":
        GUI.ResultsLogic()
    if Scene.current == "main_menu":
        GUI.MainMenuLogic()
    
    Scene.control()
    
    if Spawn.check() == 0 and Scene.current == "play":
        Spawn.spawn()

    screen.fill(info.backgroundColor)
    
    # RENDER
    
    if Scene.current == "results":
        GUI.Results()
    if Scene.current == "main_menu":
        GUI.MainMenu()
    
    for sprite in sprites:
        sprite.draw()
    
    pygame.display.update()
    clock.tick(fps)