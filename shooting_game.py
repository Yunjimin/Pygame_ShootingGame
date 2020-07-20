import pygame
import sys
from time import sleep
import os
import random

padWidth = 480
padHeight = 640
rockImage = ["rock01.png","rock02.png","rock03.png","rock04.png","rock05.png",\
             "rock06.png","rock07.png","rock08.png","rock09.png","rock10.png",\
             "rock11.png","rock12.png","rock13.png","rock14.png","rock15.png",\
             "rock16.png","rock17.png","rock18.png","rock19.png","rock20.png",\
             "rock21.png","rock22.png","rock23.png","rock24.png","rock25.png",
             "rock26.png","rock27.png","rock28.png","rock29.png","rock30.png" ] 

explosionSound= ["explosion01.wav","explosion02.wav","explosion03.wav","explosion04.wav"]

current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

#운석을 맞춘 갯수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font(os.path.join(image_path, "NanumGothic.ttf"), 20)
    text = font.render('파괴한 운석 수 :' + str(count), True, (255,255,255))
    gamePad.blit(text, (10,0))

#운석이 화면 아래로 통과한 갯수
def writePassed(count):
    global gamePad
    font = pygame.font.Font(os.path.join(image_path, "NanumGothic.ttf"), 20)
    text = font.render("놓친 운석 수 :" + str(count), True, (255,0,0))
    gamePad.blit(text, (330,0))

#게임 메시지 출력
def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font(os.path.join(image_path, "NanumGothic.ttf"), 40)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text,textpos)
    pygame.display.update()
    pygame.mixer.music.stop()  #배경 음악 정지
    gameoverSound.play()        #게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1) #배경 음악 재생
    runGame()

# 전투기가 운석과 충돌 했을 때 메시지 출력
def crash():
    global gamePad
    writeMessage("전투기 파괴!!")

# 게임 오버 메시지 보이기
def gameOver():
    global gamePad
    writeMessage("게임 오버!!")

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj,(x,y))


def initGame():
    global gamePad, clock , background , fighter , missile , explosion , missileSound, gameoverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("PyShooting") #게임 이름
    background = pygame.image.load(os.path.join(image_path, "background.png")) # 배경그림
    fighter =  pygame.image.load(os.path.join(image_path, "fighter.png")) # 전투기 그림
    missile = pygame.image.load(os.path.join(image_path, "missile.png")) # 미사일 그림
    explosion = pygame.image.load(os.path.join(image_path, "explosion.png")) # 폭발 그림
    pygame.mixer.music.load(os.path.join(image_path, "music.wav")) #배경 음악
    pygame.mixer.music.play(-1) #배경 음악 재생
    missileSound = pygame.mixer.Sound(os.path.join(image_path, "missile.wav")) #미사일 사운드
    gameoverSound = pygame.mixer.Sound(os.path.join(image_path, "gameover.wav")) #게임오버 사운드
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock , background , fighter , missile , explosion, missileSound, gameoverSound
   
    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치 (x , y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # 무기 좌표 리스트
    missileXY =[]

    rock = pygame.image.load(os.path.join(image_path, random.choice(rockImage))) # 운석 그림
    rockSize = rock.get_rect().size #운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(os.path.join(image_path, random.choice(explosionSound))) 

    #운석 초기 위치 설정
    rockX = random.randrange(0, padWidth-rockWidth)
    rockY = 0
    rockSpeed = 2

    #전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0 #맞힌갯수
    rockPassed = 0 #피한갯수

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()     #게임 프로그램 종료
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  # 왼쪽이동
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT: # 오른쪾 이동
                    fighterX += 5
                elif event.key == pygame.K_SPACE: # 미사일 발사
                    missileSound.play() #미사일 사운드 재생
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX,missileY])


            if event.type in [pygame.KEYUP]:  # 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0


        drawObject(background, 0, 0)   #배경화면 그리기

        #전투기 위치 재조정 (밖으로 못나가게)
        x += fighterX
        if x < 0:
            x=0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 전투기가 운석과 충돌 했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                    crash()

        drawObject(fighter, x, y) # 비행기를 게임 화면의 (x,y)좌표에 그림

        #미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i,bxy in enumerate(missileXY): #미사일 요소에 대해 반복함
                bxy[1] -= 10 #총알의 y좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]
                
                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0 : #미사일 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy) #미사일 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx,by in missileXY:
                drawObject(missile, bx, by)
        
        #운석 맞춘 점수 표시
        writeScore(shotCount)


        rockY += rockSpeed  # 운석 아래로 움직임

        #운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #새로운 운석( 랜덤)
            rock = pygame.image.load(os.path.join(image_path, random.choice(rockImage)))
            rockSize = rock.get_rect().size 
            rockWidth = rockSize[0]
            rockHeight = rockSize[1] 
            rockX = random.randrange(0, padWidth-rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: # 운석 3개 놓치면 게임 오버 
            gameOver()

        writePassed(rockPassed)

        #운석을 맞춘 경우
        if isShot:
            #운석폭발
            drawObject(explosion, rockX, rockY)
            destroySound.play() #운석 폭발 사운드 재생
            #새로운 운석( 랜덤)
            rock = pygame.image.load(os.path.join(image_path, random.choice(rockImage)))
            rockSize = rock.get_rect().size 
            rockWidth = rockSize[0]
            rockHeight = rockSize[1] 
            rockX = random.randrange(0, padWidth-rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(os.path.join(image_path, random.choice(explosionSound)))  
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.05
            if rockSpeed >= 10:
                rockSpeed = 10
            

        drawObject(rock, rockX, rockY) # 운석그리기


        pygame.display.update() # 게임화면을 다시그림

        clock.tick(60) # 게임화면의 초당 프레임수

    pygame.quit()  #pygame 종료

initGame()
runGame()