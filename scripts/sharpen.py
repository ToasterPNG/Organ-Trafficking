import numpy as np
import cv2, pygame

kernel = np.array([[-1, -1, -1], [-1, 19.5, -1], [-1, -1, -1]])

def red(image):
    global kernel
    
    view = pygame.surfarray.pixels3d(image)
    view = view.transpose([1, 0, 2])
    img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)

    img_red = img_bgr.copy()
    img_red[:,:,0] = img_red[:,:,1] = 0

    img_sharp = img_bgr.copy()
    img_sharp = cv2.filter2D(img_sharp, -141, kernel)

    result = cv2.addWeighted(img_red, 1, img_sharp, 0.1, 3)

    return pygame.image.frombuffer(result.tostring(), result.shape[1::-1],"BGR")
