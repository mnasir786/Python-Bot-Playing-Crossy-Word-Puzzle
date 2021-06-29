import pyautogui, time, os
from itertools import permutations
pyautogui.FAILSAFE=False
PLAY = 'play'
NEXT = 'next'
CLOSEPANEL1='closepanel1'
CLOSEPANEL2='closepanel2'
ALPHASAMPLE= 'alpha_sample'
GetBONUS = 'getbonus'
ARROW = 'arrow'

comeOutOfLoop=False

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)

Top_Left = pyautogui.locateOnScreen(imPath('top_left_corner.png'),confidence=0.9)
Top_Right = pyautogui.locateOnScreen(imPath('top_right_corner.png'),confidence=0.9)

leftx=0
if Top_Left is not None:
    leftx = int(Top_Left[0])

x_width = int((Top_Right[0]-leftx))
screenWidth, screenHeight = pyautogui.size()
GAME_REGION = [leftx,int(Top_Right[1]),x_width,screenHeight*2-int(Top_Right[1])]

alphay_start = int(GAME_REGION[3]/2+GAME_REGION[1])
alphay_ht = int(GAME_REGION[3]/2-1)
upper_start = GAME_REGION[1]
ALPHA_REGION = [GAME_REGION[0],alphay_start,GAME_REGION[2],alphay_ht]
UPPER_REGION = [GAME_REGION[0],upper_start,GAME_REGION[2],alphay_ht]

print(GAME_REGION)

def PressButtonLEFTTOP(btnName,dregion):
    PLAY_COORDS=pyautogui.locateOnScreen(imPath(btnName+'.png'),region=dregion ,confidence=0.8)
    print(PLAY_COORDS)
    if PLAY_COORDS is not None:
        topRightX = PLAY_COORDS[0] #+ PLAY_COORDS[2] / 2
        topRightY = PLAY_COORDS[1] #+ PLAY_COORDS[3] / 2
        pyautogui.moveTo(x=topRightX / 2, y=topRightY / 2)
        pyautogui.doubleClick(x=topRightX / 2, y=topRightY / 2)
def PressButton(btnName,dregion):
    PLAY_COORDS=pyautogui.locateOnScreen(imPath(btnName+'.png'),region=dregion ,confidence=0.9)
    print(PLAY_COORDS)
    isPressed=False
    if PLAY_COORDS is not None:
        topRightX = PLAY_COORDS[0] + PLAY_COORDS[2] / 2
        topRightY = PLAY_COORDS[1] + PLAY_COORDS[3] / 2
        pyautogui.moveTo(x=topRightX / 2, y=topRightY / 2)
        pyautogui.doubleClick(x=topRightX / 2, y=topRightY / 2)
        isPressed = True
    return  isPressed
def inRangeX(old,new):
    oldxP=old[0] +old[2]
    oldxN = old[0] - old[2]
    xPoint = new[0]
    # print(f'oldxp {oldxP} oldxN {oldxN} and new {xPoint} ')
    if xPoint<=oldxP and xPoint>=oldxN:
        return True
    else:
        return  False

def inRangeY(old,new):
    oldxP=old[1] +old[3]
    oldxN = old[1] - old[3]
    xPoint = new[1]
    # print(f'oldxp {oldxP} oldxN {oldxN} and new {xPoint} ')
    if xPoint<=oldxP and xPoint>=oldxN:
        return True
    else:
        return  False
def inRange(list,element):
    for oldcoord in list:
        if inRangeX(element, oldcoord) and inRangeY(element, oldcoord):
            return False
            # print('inRange inRangeX and inRangeY true')
        else:
            continue
    return True
def GetUniqueButtonPositions(PLAY_COORDSS):
    newCoord = []
    count = 0
    for ind in PLAY_COORDSS:
        if count == 0:
            count = 1
            newCoord.append(ind)
            # print('lenth was 0')
        elif inRange(newCoord, ind):
            newCoord.append(ind)
            # print('can apped true')
        else:
            # print('can append False')
            continue
    return newCoord
def GetAllCombinations(newCoord,ccount):
    # size of combination is set to ccount
    a = list(permutations(newCoord, ccount))
    # y = [[].join(i) for i in a]
    return a
def MoveTo(coords,dt=1):
    if coords is not None:
        topRightX = coords[0] + coords[2] / 2
        topRightY = coords[1] + coords[3] / 2
        pyautogui.moveTo(x=topRightX / 2, y=topRightY / 2, duration=dt)
        time.sleep(dt)

btnCheckIndex=0
def MakeLetterWords(Combo4,dt,lttrs):
    global comeOutOfLoop
    global btnCheckIndex
    for combi in Combo4:
        MoveTo(combi[0],dt)
        pyautogui.mouseDown()

        for wl in range(1,lttrs):
            MoveTo(combi[wl], dt)
            if comeOutOfLoop:
                break

        pyautogui.mouseUp()
        print('combinationdone')

        if btnCheckIndex==0:
            if PressButton(NEXT, ALPHA_REGION):
                comeOutOfLoop = True
        elif btnCheckIndex==1:
            PressButton('keepplaying', ALPHA_REGION)
        elif btnCheckIndex==2:
            PressButtonLEFTTOP(ARROW, GAME_REGION)
        else:
            btnCheckIndex=0


        if comeOutOfLoop:
            break
        # PressButton('keepplaying', GAME_REGION)
        # PressButtonLEFTTOP(ARROW, GAME_REGION)
        # time.sleep(dt)

def ApplyAllCombinations(newCoord):
    print('alphaCounts:'+str(len(newCoord)))
    global comeOutOfLoop
    if len(newCoord) <= 3:
        Combo = GetAllCombinations(newCoord, 3)
        MakeLetterWords(Combo, 0.001, 3)
    else:
        for set in range(3,len(newCoord)+1):
            Combo = GetAllCombinations(newCoord, set)
            MakeLetterWords(Combo, 0.001, set)
            if comeOutOfLoop:
                break


def FindAlphaBets(dregion):
    print(dregion)
    PLAY_COORDSS=pyautogui.locateAllOnScreen(imPath(ALPHASAMPLE+'.png'),region=dregion ,confidence=0.45)
    centre=pyautogui.center(dregion)
    pyautogui.doubleClick(x=centre[0]/2,y=centre[1]/2)
    newCoord= GetUniqueButtonPositions(PLAY_COORDSS)
    ApplyAllCombinations(newCoord)

def CheckButtons():
    PressButton(PLAY, ALPHA_REGION)
    PressButton(NEXT, ALPHA_REGION)
    PressButton(GetBONUS, ALPHA_REGION)
    PressButton(CLOSEPANEL1, UPPER_REGION)
    PressButton(CLOSEPANEL2, UPPER_REGION)
    PressButtonLEFTTOP(ARROW, GAME_REGION)
while True:
    print('Press Ctrl-C to quit.')
    try:
        # time.sleep(1)
        comeOutOfLoop=False
        CheckButtons()
        FindAlphaBets(ALPHA_REGION)
        # break
    except KeyboardInterrupt:
        print('\n')



