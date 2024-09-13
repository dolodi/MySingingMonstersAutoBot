from pyautogui import locateCenterOnScreen, ImageNotFoundException, click, doubleClick, moveTo, locateOnScreen, locateAllOnScreen, scroll, keyDown, keyUp
from time import sleep
from os import listdir
from constants import *
import keyboard
import os
import sys
import subprocess
from typing import List, Tuple
import datetime
import time

RESTART_INTERVAL = 2000
HIBERNATION_INTERVAL = 2000  # not 1.5 hours in seconds

def restart_pc():
    print("Restarting the PC...")
    if os.name == 'nt':  # For Windows
        os.system('shutdown /r /t 1')
    else:  # For Unix-based systems (Linux, macOS)
        os.system('sudo shutdown -r now')


def hibernate_pc():
    if os.name == 'nt':  # Windows
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:  # Linux and macOS
        os.system("systemctl suspend")

# Define the hour at which the script should shut down (24-hour format)
SHUTDOWN_HOUR = 3  # For example, 10 PM
SHUTDOWN_HOUR_END = 4


def check_shutdown_time():
    current_time = datetime.datetime.now()
    if  SHUTDOWN_HOUR <= current_time.hour < SHUTDOWN_HOUR_END:
        print(f"It's {current_time.strftime('%H:%M')}. Initiating shutdown.")
        shutdown_pc()
        return True
    return False

# Constants
ITERATIONS_BEFORE_SHUTDOWN = 100  # Adjust this number as needed
COOLDOWN_TIME = 3600  # 1 hour in seconds, adjust as needed
# CODE BY ADRIAN MONTES
#pip install pyautogui
#pip install opencv_python

"""got a collect key"""
#close notification
#collect button
#setting locate on screen confidence to .5 will allow to collect jumping images
#this could mean lighting tourches

# first open the game, wait close button to be on screen
#if not already in game open it from desktop else throw error

# isFoodCollected = False
waitingTime = 2.5;

def findClick(image : str, time = .5, confidence = .86) -> None:
    """Given an image will click on the centered location
    
    :param image: Image to find on screen
    :param time: The time to wait after clicking on image
    :param confidence: How closely the image must match the findings on screen
    :return: None"""
    try:
        location = locateCenterOnScreen(image = image, confidence = confidence)
        if location:
            
            click(location)
            sleep(time)
    except ImageNotFoundException:
        # print("Not found: " + image)
        return None

def isOnScreen(image, confidence = .86):
    try:
        item = locateOnScreen(image = image, confidence = confidence)
        if item:
            return True
    except ImageNotFoundException:
        return False
    return False

def checkAvoidIslands():
    """If currenly on an avoided island, click next. Checks all islands in avoid islands folder again """
    islands = listdir("AvoidIslands")
    for island in islands:
        if isOnScreen(island):
            findClick(NEXT)
            checkAvoidIslands()

#Currenty unused
def openGame():
    """Opens game and ensures it's open before continuing"""
    pass
    #check if opened later    
    
def collectDaily():
    try:
        coordinates = locateCenterOnScreen(COLLECT)
        moveTo(coordinates)
        sleep(.5)
        click()
    except ImageNotFoundException:
        return None
         
# DO NOTIFS ELSEWHERE
# then confirm if there then hit close on any notifications
# def closeNotification():
#     """Closes notifications that appear at the begging"""
#     try:
#         coordinates = locateCenterOnScreen("Images\\close.png")
#         click(coordinates)
#         return coordinates
#     except ImageNotFoundException:
#         return None

def mirrorSwitch(maps = 0):
    findClick(MAP)
    findClick(MIRROR)

def collectAll():
    """Finds and clicks on CollectAll, Confirm, then looks for gems"""
    findClick(COLLECT, confidence = .7)

    if isOnScreen(COLLECTALL, confidence = .75):
        findClick(COLLECTALL, confidence = .75)
        findClick(CONFIRM)
    sleep(2)
    findClick(GEM, confidence = .6)
    findClick(GEM2, confidence = .6)

    if isOnScreen(NEXUSCOLLECT, confidence = .7):
        findClick(NEXUSCOLLECT, confidence = .7)
        sleep(1.5)
        findClick(COLLECTNEXUS, confidence = .7)

    
def collectFood():
    """Collects all the food available on screen until no more is found (recursive)"""
    try:
        food_found = list(locateAllOnScreen(FOOD, confidence = .62))
        print("number of food detected: "+ str(len(food_found)))   
    except ImageNotFoundException:
        return None
    except Exception as e:
        print(e)
    else:
        food_locations = []
        for located in food_found:
            if len(food_locations) == 0:
                food_locations.append(located)
                continue
            if not (located[0] - 10 <= food_locations[len(food_locations)-1][0] <= located[0] + 10):
                food_locations.append(located)
        
        for location in food_locations:
            click(location)
        if len(food_locations) != 0:
            return True
    
def rebake():
    """Clicks on last collected Bakery then rebakes all"""
    findClick(BAKERY, confidence = .7)
    sleep(1.5)
    findClick(RETRY)
    findClick(CONFIRM)
    sleep(1.5)
    
def changeMap():
    """Navigates through all islands in My Singing Monsters"""
    
    # Define the sequence of islands and their corresponding next island button
    island_sequence: List[Tuple[str, str]] = [
        (PLANT_ISLAND, COLD),
        (COLD_ISLAND, AIR),
        (AIR_ISLAND, WATER),
        (WATER_ISLAND, EARTH),
        (EARTH_ISLAND, SHUGABUSH),
        (SHUGABUSH_ISLAND, ETHEREAL),
        (ETHEREAL_ISLAND, ETHEREALWORKSHOP),
        (ETHEREALWORKSHOP_ISLAND, FIREHAVEN),
        (FIREHAVEN_ISLAND, FIREOASIS),
        (FIREOASIS_ISLAND, MYTHICAL),
        (MYTHICAL_ISLAND, LIGHT),
        (LIGHT_ISLAND, PSYCHIC),
        (PSYCHIC_ISLAND, FAERIE),
        (FAERIE_ISLAND, BONE),
        (BONE_ISLAND, MAGICALSANCTUM),
        (MAGICALSANCTUM_ISLAND, NEXUS),
        (NEXUS_ISLAND, AMBER),
        (AMBER_ISLAND, WUBLIN),
        (WUBLIN_ISLAND, CELESTIAL),
        (MIRROR_PLANT_ISLAND, MIRROR_COLD),
        (MIRROR_COLD_ISLAND, MIRROR_AIR),
        (MIRROR_AIR_ISLAND, MIRROR_WATER),
        (MIRROR_WATER_ISLAND, MIRROR_EARTH),
    ]

    findClick(MAP)
    sleep(3) # dont fucking remove this 

    usinng = 0
    if isOnScreen(MIRROR_PLANT_ISLAND):
        print("muori")     
        findClick(MIRROR_COLD)
        sleep(2)
        findClick(GO)
        sleep(5)

    if isOnScreen(MIRROR_AIR_ISLAND):
        print("muori")     
        findClick(MIRROR_WATER)
        sleep(2)
        findClick(GO)
        sleep(5)

    if isOnScreen(MIRROR_WATER_ISLAND):
        print("muori2")     
        findClick(MIRROR_EARTH)
        sleep(2)
        findClick(GO)
        sleep(5)

     # Special case
    if isOnScreen(CELESTIAL_ISLAND):         
        print("LAST")         
        findClick(MIRROR)         
        sleep(waitingTime)         
        findClick(MIRROR_PLANT) 


    # Special case for the last island
    if isOnScreen(MIRROR_EARTH_ISLAND):
        findClick(UNMIRROR)
        sleep(2)
        findClick(PLANT)
        sleep(2)
        findClick(GO)
        sleep(5)

    for current_island, next_button in island_sequence:
        if isOnScreen(current_island):
            findClick(next_button)
            print("current detected island: "+ current_island)    
            print("next island: "+ next_button) 
            sleep(waitingTime) 
            findClick(GO)
            usinng = 1
            sleep(2)




    # IF NOT ISLANDS SELECTED
    if usinng == 0:
        for current_island, next_button in island_sequence:
            if isOnScreen(next_button):
                findClick(next_button)
                print("defaulting to first available island: "+ next_button)    
                sleep(waitingTime) 
                findClick(GO)
                sleep(2)




timeUntillRetry = 60 * 10

def retry():
    done = 0
    if isOnScreen(USE):
        print("USING")
        findClick(OK)
        sleep(timeUntillRetry)
        findClick(PLAY)

       

    if isOnScreen(TIMEOUT):
        print("TIMEOUT")
        findClick(OK)
        sleep(timeUntillRetry)
        findClick(PLAY)

        

    else:
        findClick(CONTINUE)
        findClick(OK)

        if isOnScreen(PLAY):
            sleep(timeUntillRetry)
            findClick(PLAY)
        

        
 

    
def closeNoti():
    findClick(NOTI, confidence = .75)
    findClick(NOTI2, confidence = .75)

def closeMailbox():
    if isOnScreen(MAILBOX, confidence = .75):
        print("MAILBOX")
        findClick(CLOSE, confidence = .75)

def shutdown_pc():
    print("Shutting down PC...")
    if os.name == 'nt':  # For Windows
        os.system('shutdown /s /t 1')
    else:  # For Unix-based systems
        os.system('sudo shutdown -h now')

def breed(order = 1, nobreed = 0):
    if isOnScreen(BREED, confidence = .7) and nobreed == 0:
        findClick(BREED, confidence = .7)
        sleep(2)

        if isOnScreen(CLACKULA, confidence = .79):  # clackula or magic repetetitive
            print("not ckackuka")
            findClick(WAIT, confidence = .7)
            sleep(3)
            if isOnScreen(CONFIRM, confidence = .7):
                nobreed = 1
                findClick(CONFIRM, confidence = .7)
                sleep(3)
            else :
                if order == 1:
                    findClick(BREEDER, confidence = .78)
                else:
                    findClick(BREEDER2, confidence = .78)
                sleep(4)
                if isOnScreen(BREEDREAL, confidence = .74):
                    findClick(BREEDREAL, confidence = .74)

                if isOnScreen(BREEDREALPROMOMYTHIC, confidence = .74):
                    findClick(BREEDREALPROMOMYTHIC, confidence = .74)

                sleep(3)
                findClick(RETRY, confidence = .74)
                sleep(3)
                findClick(CONFIRM_BREEDING, confidence = .74)
                sleep(3)
                findClick(WAIT, confidence = .74)
                sleep(3)
                if isOnScreen(CONFIRM, confidence = .7):
                    nobreed = 1
                    findClick(CONFIRM, confidence = .7)
                    sleep(2)


        findClick(ZAP, confidence = .74)
        #sleep(3)
        #findClick(ZAP_AMBER, confidence = .74)
        sleep(5)
        if isOnScreen(ZAP_TO, confidence = .68):
            findClick(ZAP_TO, confidence = .74)
            sleep(3)
            
            if isOnScreen(CONFIRM_WUBLIN, confidence = .74):
                print("NOT NATTY")
                findClick(CONFIRM, confidence = .74)
                sleep(3)
            else:   # else if is rare or some else
                print("RARE maybe")
                findClick(CONFIRM, confidence = .74)
                sleep(3)
                findClick(CLOSE_ZAP, confidence = .74)
                sleep(3)
                findClick(WAIT, confidence = .74)
                sleep(3)
                if isOnScreen(CONFIRM, confidence = .7):
                    nobreed = 1
                    findClick(CONFIRM, confidence = .7)
                    sleep(2)
           

            if isOnScreen(CONFIRM_WUBLIN, confidence = .74):
                findClick(CLOSE, confidence = .74)
            else:
                findClick(CONFIRM, confidence = .74) #changed here if rare
                # sleep(3)
                # findClick(CLOSE, confidence = .7)
                # sleep(3)
                # findClick(WAIT, confidence = .7)
                
                # if isOnScreen(CONFIRM, confidence = .7):
                #     findClick(CONFIRM, confidence = .7)
                #     sleep(2)
                # else:
                #     scroll(-1)
                #     scroll(1)
                    
            sleep(3)
            if order == 1:
                findClick(BREEDER, confidence = .78)
            else:
                findClick(BREEDER2, confidence = .78)
            sleep(4)
            if isOnScreen(BREEDREAL, confidence = .74):
                findClick(BREEDREAL, confidence = .74)

            if isOnScreen(BREEDREALPROMOMYTHIC, confidence = .74):
                findClick(BREEDREALPROMOMYTHIC, confidence = .74)

            sleep(3)
            findClick(RETRY, confidence = .74)
            sleep(3)
            findClick(CONFIRM_BREEDING, confidence = .7)
            sleep(3)
            findClick(WAIT, confidence = .7)
            sleep(3)
            if isOnScreen(CONFIRM, confidence = .7):
                nobreed = 1
                findClick(CONFIRM, confidence = .7)
                sleep(2)
        else:
            findClick(CLOSE_ZAP, confidence = .7)
            sleep(3)
            findClick(WAIT, confidence = .7)
            sleep(3)
            if isOnScreen(CONFIRM, confidence = .7):
                nobreed = 1
                findClick(CONFIRM, confidence = .7)
                sleep(2)
            else:
                scroll(-1)
                scroll(1)
                sleep(3)
        return nobreed
    return nobreed

def hatch(nohatch = 0):
    if isOnScreen(HATCH, confidence = .7) and nohatch == 0:
        findClick(HATCH, confidence = .7)
        sleep(3)
        if isOnScreen(CLACKULA_HATCH, confidence = .74):
            findClick(PLACE, confidence = .7)
        else:
            nohatch = 1
            findClick(CLOSE_HATCH, confidence = .7)
        sleep(3)
        findClick(CONFIRM, confidence = .7)
        sleep(3)
        moveTo(1000, 500)
        keyDown('down')
        sleep(3)
        keyUp('down')
        sleep(3)
        return nohatch
    return nohatch

def conundrum():
    if isOnScreen(CONUNDRUM, confidence = .75):
        findClick(CONUNDRUM, confidence = .75)
        sleep(3)
        findClick(CONUNDRUM_COLLECT, confidence = .75)
        sleep(10)
        scroll(1)
        sleep(3)
        findClick(CLOSE, confidence = .75)
        sleep(3)

def countingStars():
    breed_locations = locateAllOnScreen(BREED, confidence=0.76)

    # Method 1: Convert to a list and use len()
    # breed_list = list(breed_locations)
    # number_of_breeds = len(breed_list)

    # # Method 2: Use sum() with a generator expression
    number_of_breeds = sum(1 for _ in breed_locations)

    # Method 3: Iterate and count manually
    # number_of_breeds = 0
    # for _ in breed_locations:
    #     number_of_breeds += 1

    print(f"Number of BREED occurrences found: {number_of_breeds}")


def spin():

    if isOnScreen(SPIN, confidence = 0.7):
        findClick(SPIN, confidence = 0.7)
        sleep(1)
        moveTo(1000, 500)
        keyDown('up')
        sleep(1)
        keyUp('up')
        sleep(10)
        findClick(COLLECT, confidence = .7)
        sleep(3)
        findClick(CLOSE, confidence = .7)

def main():
    """Closes notification, Then Main Loop."""
    print("started")
    #keyboard.press_and_release("alt+tab")
    if isOnScreen(COLLECTALL, confidence = .7) or isOnScreen(CLOSE, confidence = .7):
        print("alr")
    else:
        sleep(46)
        findClick(PLAY)
    #for i in range(9):
    #    scroll(-10)
    # closeNotification()
    # print("close notif")

    iteration_count = 0
    start_time = time.time()

    print("done pla6")
    

    sleep(2)

    while True:



        # iteration_count = iteration_count + 1
        # print(iteration_count)

        nohatch = 0
        nobreed = 0
        
        spin()
        
        retry()
        closeNoti()
        closeMailbox()

        
        # findClick(BREEDER2, confidence = .76)
        # print("1")
        # sleep(4)
        # findClick(BREEDER, confidence = .76)
        # print("2")
        # print("TRIED")

        # countingStars()
        # sleep(100)

        sleep(0.5)
        # collectDaily()
        if isOnScreen(CLOSE, confidence = .7):
            print("hallah may protect us")
        else:
            moveTo(1000, 500)
            keyDown('down')
            sleep(2)
            keyUp('down')

        collectAll()
        conundrum()

        nohatchdos = hatch(nohatch = nohatch)
        hatch(nohatch = nohatchdos)

        nobreeddos = breed(order = 2, nobreed = nobreed)
        breed(order = 1, nobreed = nobreeddos)  #IF U have 2 breeders (wublins celestials amber)

        if isOnScreen(FOOD, confidence = .6):
            collectFood()#: if
            #rebake()
        print("collected")

        sleep(1)
        changeMap()
        print("map changed")
        sleep(.5)

        

        current_time = time.time()
        if current_time - start_time >= RESTART_INTERVAL:
            print(f"Running for {RESTART_INTERVAL/3600:.2f} hours. Restarting the PC.")
            restart_pc()
            break 
        #current_time = time.time()
        #if current_time - start_time >= HIBERNATION_INTERVAL:
        #    print(f"Running for {HIBERNATION_INTERVAL/3600:.2f} hours. Initiating hibernation.")
        #    hibernate_pc()
        #    break  # Exit the loop after hibernation

        if check_shutdown_time():
            break

        iteration_count = iteration_count + 1

main()

