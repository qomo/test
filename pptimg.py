#!/usr/bin/python 
# -*- coding: utf-8 -*-
import pygame
import Image 
import sys

def get_shear_points(img_name, shear_pos=[]):
    # 这段子程序用于预览或选择将要剪切变换的投影照片， 图中四个x表示将要剪切的四边形的四个顶点，左键确认，右键从新手动选择四个顶点。
    # shear_pos: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], x和y是0到1范围的相对坐标
    black = [0, 0, 0]  # Define some colors
    white = [255,255,255]
    blue = [0,255,0]
    red = [255,0,0]

    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('PPT image shear')
    background = pygame.Surface(screen.get_size())
    background.fill(black)
    clock = pygame.time.Clock()
    origin_position = [0,0]
    # 加载图片，并按screen尺寸显示
    origin_image = pygame.image.load(img_name).convert()
    new_image = pygame.transform.smoothscale(origin_image, (800, 600))
    # 加载指示图片
    #dir_image = pygame.image.load('dirimg.png').convert()
    #dir_image = pygame.transform.smoothscale(dir_image, (50, 50))
    #dir_image.set_colorkey(white)
    
    done = False    #若为True表示完成取点
    while done == False:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:     # 如果退出取点框，返回空值
                return None
            if event.type==pygame.MOUSEBUTTONDOWN:  
                mouse_buttons = pygame.mouse.get_pressed()  # 获得鼠标按键信息
                if mouse_buttons==(0, 0, 1):    
                    # 如果右键按下，清空shear_pos，从新取点
                    shear_pos = []
                if mouse_buttons==(1, 0, 0) and len(shear_pos)<4:  
                    # 如果左键按下且取点数不够四个，添加当前鼠标位置到shear_pos
                    mouse_position = pygame.mouse.get_pos()
                    shear_pos.append(mouse_position)
                if mouse_buttons==(1, 0, 0) and len(shear_pos)==4:
                    # 如果左键按下且取点数足够四个，结束取点
                    done = True
        screen.blit(new_image, origin_position)
        #screen.blit(dir_image, (50, 50))    
        # 标注已经选取点
        for cout,point in enumerate(shear_pos):
            #font = pygame.font.Font(None, 25)
            #text = font.render(str(cout+1), True, red)
            #screen.blit(text, point)
            pygame.draw.rect(screen, blue, [point[0]-20, point[1]-20, 40, 40], 5)
        if len(shear_pos) == 4: # 标注中点
            x = sum([i[0] for i in shear_pos])/4
            y = sum([i[1] for i in shear_pos])/4
            pygame.draw.rect(screen, blue, [x-20,y-20,40,40], 5)
        pygame.display.flip()
    pygame.quit()
    # 将鼠标位置转换为相对坐标
    shear_pos = [(float(mouse_position[0])/800, float(mouse_position[1])/600) for mouse_position in shear_pos]
    return shear_pos

def trans_img(shear_pos, imgname):
    # 这段子程序用于裁剪变换一个图片的四边形区域为矩形
    if shear_pos == None:
        return None
    im = Image.open(imgname)
    im_size = im.size

    # 判断调整顶点顺序
    x_m = sum([i[0] for i in shear_pos])/4
    y_m = sum([i[1] for i in shear_pos])/4
    for point in shear_pos:
        if point[0]<=x_m and point[1]<=y_m:
            x0 = int(point[0] * im_size[0] )
            y0 = int(point[1] * im_size[1] )
        if point[0]<=x_m and point[1]>=y_m:
            x1 = int(point[0] * im_size[0] )
            y1 = int(point[1] * im_size[1] )
        if point[0]>=x_m and point[1]>=y_m:
            x2 = int(point[0] * im_size[0] )
            y2 = int(point[1] * im_size[1] )
        if point[0]>=x_m and point[1]<=y_m:
            x3 = int(point[0] * im_size[0] )
            y3 = int(point[1] * im_size[1] )


    new_size_x = im_size[0]
    new_size_y = int(float(im_size[1])/im_size[0] * new_size_x)
    newim = im.transform((new_size_x,new_size_y), Image.QUAD, (x0,y0,x1,y1,x2,y2,x3,y3))
    newim.save("new_" + imgname)

if __name__ == "__main__":
    for i in range(1,len(sys.argv)):
        filename = sys.argv[i]
        if filename[-4:] in ['.jpg',]:
            a = get_shear_points(filename, [])
            trans_img(a, filename)
