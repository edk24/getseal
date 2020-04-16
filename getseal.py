import cv2
import numpy as np
import PIL.Image as Image
import sys, getopt
import time

def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = (255,255,255,255)
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,color_1)
    return img

def action(inputfile, outputfile):
  np.set_printoptions(threshold=np.inf)
  image=cv2.imread(inputfile)

  hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  low_range = np.array([150, 103, 100])
  high_range = np.array([180, 255, 255])
  th = cv2.inRange(hue_image, low_range, high_range)
  index1 = th == 255
  # save image
  img = np.zeros(image.shape, np.uint8)
  img[:, :] = (255,255,255)
  img[index1] = image[index1]#(0,0,255)
  cv2.imwrite(outputfile, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

  # delete rgb(255,255,255)
  img1 = Image.open(outputfile)
  img1=transparent_back(img1)
  img1.save(outputfile)

if __name__ == "__main__":
  inputfile = ''
  outputfile = ''
  argv = sys.argv[1:]
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print(' -i <inputfile> -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
        print(' -i <inputfile> -o <outputfile>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
  start = time.time()
  action(inputfile, outputfile)
  end = time.time()
  print("耗时: "+str(end-start))


