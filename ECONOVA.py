#import thư viện
import sys
import pygame as pg
from pygame.locals import *
import random
import os

pg.init()
#set màu
gray=(100,100,100)
green=(76,208,56)
yellow=(255,232,0)
red=(200,0,0)
white=(255,255,255)
#thay đổi icon:
icon=pg.image.load('icon/Logo.png')
pg.display.set_icon(icon)
#tạo cửa sổ game
rộng=900
cao=900
size=(rộng, cao)
scr=pg.display.set_mode((size))
#thay đổi tiêu đề:
pg.display.set_caption('EcoNova')
#khởi tạo biến
gameover=False
speed=2
score=0
#đường xe chạy
đường=rộng-rộng/5
biên=10
biêndài=50
#lane đường:
trái=90
giữa_trái=trái+rộng/5
giữa_phải=giữa_trái+rộng/5
phải=giữa_phải+rộng/5
lanes=[trái+90, giữa_trái+90, giữa_phải+90, phải+90]
#đường
road=(100,0,đường,cao)
làntrái=(90,0,biên,cao)
lànphải=(rộng-90,0,biên, cao)
lanemovey=0
#vị trí ban đầu
playerx=đường/2
playery=(cao*5/6)

#đối tượng rác
# Đường dẫn đến thư mục chứa hình ảnh rác
trash_folder = "assets/trash/1"
trash_images = os.listdir(trash_folder)
class Trash(pg.sprite.Sprite):
    def __init__(self,image,x,y):
        pg.sprite.Sprite.__init__(self)
        # Chọn ngẫu nhiên một hình ảnh
        random_image = random.choice(trash_images)
        image_path = os.path.join(trash_folder, random_image)
        image = pg.image.load(image_path)
        #scale hình
        scale= (rộng/7) /image.get_rect().width
        newwidth=image.get_rect().width*scale
        newheight=image.get_rect().height*scale
        self.image = pg.transform.scale(image,(newwidth,newheight))
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)

class Bin(pg.sprite.Sprite): #Lớp Bin
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        #scale hình
        image=pg.image.load(r'assets/ctpt.png')
        scale= (rộng/7) /image.get_rect().width
        newwidth=image.get_rect().width*scale
        newheight=image.get_rect().height*scale
        self.image = pg.transform.scale(image,(newwidth,newheight))
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)

def load_high_score():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Hàm để lưu high score vào file
def save_high_score(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

# Khởi tạo biến high_score
high_score = load_high_score()

#nhóm đối tượng:
playergroup=pg.sprite.Group()
trashgroup=pg.sprite.Group()
#tạo người hứng rác:
player = Bin(playerx,playery)
playergroup.add(player)

fell=0
#cài đặt fps(khung hình trên giây)
clock=pg.time.Clock()
fps=120

# Biến cờ hiệu để theo dõi trạng thái
game_state = "menu"  # Có thể là "menu" hoặc "playing"

pg.mixer.init()

# Load nhạc nền
pg.mixer.music.load("sound/bg.mp3")


pg.mixer.music.set_volume(0.5)  # Điều chỉnh âm lượng
pg.mixer.music.play(-1)
#SOUND
sound1 = pg.mixer.Sound("sound/fell.wav")
sound2 = pg.mixer.Sound("sound/gameover.mp3")
sound3 = pg.mixer.Sound("sound/gamestart.mp3")
sound4 = pg.mixer.Sound("sound/good.wav")
sound5= pg.mixer.Sound('sound/tăng tốc.mp3')
sound6= pg.mixer.Sound('sound/High.wav')
sound7=pg.mixer.Sound('sound/click.mp3')
sound7.set_volume(0.2)
playing_sound3=False


#set các button cho menu
b1=pg.image.load('assets/TPT.jpg')
b2=pg.image.load('assets/RTC.jpg')
b3=pg.image.load('assets/RTCL.jpg')
b1rect=b1.get_rect()
b2rect=b2.get_rect()
b3rect=b3.get_rect()
buttons = [
    {"image": b1, "rect": pg.Rect(80, 150, 200, 450)},
    {"image": b2, "rect": pg.Rect(330, 150, 200, 450)},
    {"image": b3, "rect": pg.Rect(580, 150, 200, 450)}
]
font = pg.font.Font('freesansbold.ttf', 32)
def draw_button(x, y, image, buttons):
    mouse_pos = pg.mouse.get_pos()
    if buttons.collidepoint(mouse_pos):
        sound7.play()
        scale= (rộng/4) /image.get_rect().width
    else:
        scale= (rộng/3.7) /image.get_rect().width
    newwidth=image.get_rect().width*scale
    newheight=image.get_rect().height*scale
    image= pg.transform.scale(image,(newwidth,newheight))
    rect = image.get_rect()
    x -= rect.width // 2
    y -= rect.height // 2
    scr.blit(image,(x,y))

# Tạo bề mặt lớp phủ
fade_surface = pg.Surface(size)
fade_surface.fill((0, 0, 0))

# Hàm thực hiện hiệu ứng fade
def fade(duration):
    for alpha in range(256):
        fade_surface.set_alpha(alpha)
        scr.fill(white)  # Vẽ nền trắng (bạn có thể thay đổi màu này)
        scr.blit(fade_surface, (0, 0))
        pg.display.update()
        pg.time.delay(10)

# Gọi hàm fade
fade(150)  # Thời gian fade là 100 frame
#vòng lặp xử lý game: ban đầu biến run luôn đúng, chỉ khi người dùng bấm quit(dấu x đỏ) biến run trở thành False -> cửa sổ game đóng
run=True
while run:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
            run=False
        #điều khiển thùng rác
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            # Kiểm tra xem chuột có click vào nút Start Game không
            if 80 <= mouse_x <= 300 and 100 <= mouse_y <= 550:
            # Nếu chuột di chuyển vào nút
                game_state = "playing"
            if 330 <= mouse_x <= 550 and 100 <= mouse_y <= 550:
            # Nếu chuột di chuyển vào nút
                trash_folder="assets/trash/2"
                trash_images=os.listdir(trash_folder)
                game_state = "playing"
            if 580 <= mouse_x <= 810 and 100 <= mouse_y <= 550:
            # Nếu chuột di chuyển vào nút
                trash_folder = "assets/trash/3"
                trash_images=os.listdir(trash_folder)
                game_state = "playing"
        if event.type==KEYDOWN:
            if event.key==K_LEFT and player.rect.center[0]>giữa_trái:
                player.rect.x-=180
            if event.key==K_RIGHT and player.rect.center[0]<phải:
                player.rect.x+=180

        # Kiểm tra va chạm giữa thùng rác và rác
    for tr in trashgroup:
        if pg.sprite.collide_rect(player, tr):
            # Xử lý khi hứng được rác (ví dụ: tăng điểm, xóa rác)
            tr.kill()
            score += 1
            sound4.play()
            if score>0 and score%6==0:
                speed +=1
                sound5.play()
                if speed>30 and score%20==0:
                    speed +=0.5
                    sound5.play()
                #tăng tốc độ

    # Kiểm tra rác có rơi xuống đất không            
    for tr in trashgroup:
        if tr.rect.centery >= cao:
            tr.kill()
                #if pg.sprite.collide_rect(player,tr):
            fell+=1
            sound1.play()
        #nếu rác rơi 3 lần thì thua cuộc
    if fell==3:
        gameover=True
        sound2.play()


    if game_state == "menu":
        scr.fill((0,0,0))
        font = pg.font.Font(None, 54)
        text = font.render(f"Select your Bin to Start", True, (255, 255, 255))
        textrect= text.get_rect()
        textrect.center=(rộng/2,700)
        scr.blit(text,textrect)
        
        # Lấy tọa độ chuột
# Vẽ các nút
        for button in buttons:
            draw_button(button["rect"].x+110, button["rect"].y+200, button["image"], button["rect"])
    
    elif game_state == "playing":
        # Phát nhạc
        if not playing_sound3:
            sound3.play()
            playing_sound3 = True
        #vẽ địa hình cỏ
        scr.fill(green)
        #vẽ đường chạy
        pg.draw.rect(scr,gray,road)
        #vẽ biên 
        pg.draw.rect(scr,yellow,làntrái)
        pg.draw.rect(scr,yellow,lànphải)
        #chỉnh frame hình trên giây
        clock.tick(fps)
        #vẽ vạch trắng trên đường
        lanemovey += speed*2
        #vẽ người hứng rác
        playergroup.draw(scr)
        #vẽ rác
        trashgroup.draw(scr)
        #cho rác rơi
        for tr in trashgroup:
            tr.rect.y+=speed
                #remove rác
            if tr.rect.top>=cao:
                tr.kill()
        font = pg.font.Font(None, 24)
        text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        textrect= text.get_rect()
        textrect.center=(730,50)
        scr.blit(text,textrect)
        #hiển thị điểm
        font=pg.font.Font(pg.font.get_default_font(),16)
        text=font.render('SCORE:'+str(score), True, white)
        textrect= text.get_rect()
        textrect.center=(50,40)
        scr.blit(text,textrect)
        
        #vẽ đường vạch màu trắng
        if lanemovey >= (biêndài*2):
            lanemovey=0
        for y in range(biêndài*(-2),cao,biêndài*2):
            pg.draw.rect(scr,white,(giữa_trái,y+lanemovey,biên,biêndài))
            pg.draw.rect(scr,white,(giữa_phải,y+lanemovey,biên,biêndài))
            pg.draw.rect(scr,white,(giữa_phải+180,y+lanemovey,biên,biêndài))
    
    if len(trashgroup)<3:
        addtrash= True
        for tr in trashgroup:
            if tr.rect.top<tr.rect.height:
                addtrash=False
        if addtrash:
            lane = random.choice(lanes)
            image = random.choice(trash_images)
            tr=Trash(image,lane,cao/-2)
            trashgroup.add(tr)
    
    if gameover:
        pg.draw.rect(scr,red,(0,50,rộng,300))
        font=pg.font.Font(pg.font.get_default_font(),36)
        text=font.render('Game over! Play again? (Y / N) \n SCORE:'+str(score), True, white)
        textrect= text.get_rect()
        textrect.center=(rộng/2,300)
        scr.blit(text,textrect)
        pg.mixer_music.stop()
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            sound6.play()
        # Hiển thị high score trên màn hình
        font = pg.font.Font(None, 36)
        text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        textrect= text.get_rect()
        textrect.center=(rộng/2,150)
        scr.blit(text,textrect)
    
    pg.display.update()
        
    while gameover:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type==QUIT:
                gameover = False
                run=False
            #điều khiển thùng rác
            if event.type==KEYDOWN:
                if event.key== K_y:
                        #reset game
                    gameover = False
                    score = 0
                    speed=2
                    trashgroup.empty()
                    player.rect.center = [playerx,playery]
                    fell=0
                    game_state='menu'
                    pg.mixer_music.play(-1)
                elif event.key == K_n:
                    gameover=False
                    run=False

pg.quit()