from pyautogui import locateCenterOnScreen, ImageNotFoundException, click, doubleClick, moveTo, locateOnScreen, locateAllOnScreen, scroll
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

RESTART_INTERVAL = 5400
HIBERNATION_INTERVAL = 5400  # 1.5 hours in seconds

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
    findClick(COLLECTALL, confidence = .75)
    findClick(CONFIRM)
    sleep(2.2)
    findClick(GEM, confidence = .58)
    findClick(NEXUSCOLLECT)
    sleep(1.5)
    findClick(COLLECTNEXUS)

    
def collectFood():
    """Collects all the food available on screen until no more is found (recursive)"""
    try:
        food_found = list(locateAllOnScreen(FOOD, confidence = .6))
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
        (FIREOASIS_ISLAND, LIGHT),
        (LIGHT_ISLAND, PSYCHIC),
        (PSYCHIC_ISLAND, FAERIE),
        (FAERIE_ISLAND, BONE),
        (BONE_ISLAND, MAGICALSANCTUM),
        (MAGICALSANCTUM_ISLAND, NEXUS),
        (NEXUS_ISLAND, AMBER),
        (AMBER_ISLAND, WUBLIN),
        (MIRROR_PLANT_ISLAND, MIRROR_COLD),
        (MIRROR_COLD_ISLAND, MIRROR_AIR),
        (MIRROR_AIR_ISLAND, MIRROR_WATER),
        (MIRROR_WATER_ISLAND, MIRROR_EARTH),
    ]

    findClick(MAP)
    #sleep(2)

    for current_island, next_button in island_sequence:
        if isOnScreen(current_island):
            findClick(next_button)
            print("current detected island: "+ current_island)    
            print("next island: "+ next_button) 
            sleep(waitingTime) 
            findClick(GO)
            sleep(2)
    
    # Special case
    if isOnScreen(WUBLIN_ISLAND):         
        print("WUBLINN")         
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




timeUntillRetry = 60 * 10

def retry():
    done = 0
    if isOnScreen(USE):
        print("USING")
        findClick(OK)
        sleep(timeUntillRetry)
        findClick(PLAY)
        done = 1
       

    if isOnScreen(TIMEOUT):
        print("TIMEOUT")
        findClick(OK)
        sleep(timeUntillRetry)
        findClick(PLAY)
        done = 1
        

    

    if isOnScreen(PLAY):
        sleep(timeUntillRetry)
        findClick(PLAY)
        
    if done == 0 :
        findClick(CONTINUE)
        findClick(OK)
        findClick(PLAY)

    
def closeNoti():
    findClick(NOTI)
    findClick(NOTI2)

def closeMailbox():
    if isOnScreen(MAILBOX):
        print("MAILBOX")
        findClick(CLOSE)

def shutdown_pc():
    print("Shutting down PC...")
    if os.name == 'nt':  # For Windows
        os.system('shutdown /s /t 1')
    else:  # For Unix-based systems
        os.system('sudo shutdown -h now')

def breed():
    if isOnScreen(BREED, confidence = .6):
        findClick(BREED)
        sleep(2)
        findClick(ZAP)
        sleep(4)
        findClick(ZAP_TO, confidence = .7)
        sleep(2)
        findClick(CONFIRM)
        sleep(3)
        findClick(BREEDER, confidence = .68)
        sleep(4)
        findClick(BREEDREAL, confidence = .7)
        sleep(3)
        findClick(RETRY)
        sleep(3)
        findClick(CONFIRM_BREEDING, confidence = .7)
        sleep(3)
        findClick(WAIT, confidence = .7)
        sleep(3)

def main():
    """Closes notification, Then Main Loop."""
    print("started")
    #keyboard.press_and_release("alt+tab")
    sleep(2)

    #for i in range(9):
    #    scroll(-10)
    # closeNotification()
    # print("close notif")

    iteration_count = 0
    start_time = time.time()

    while True:
        if iteration_count % 10:
            retry()
            closeNoti()
            closeMailbox()
        if keyboard.is_pressed('q'):
            break

        sleep(1)
        breed();
        collectAll()
        collectFood()#: if
            #rebake()
        print("collected")

        changeMap()
        print("map changed")
        sleep(2.5)


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

