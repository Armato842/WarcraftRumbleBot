import time
import random
import pyautogui
import numpy as np
import logging
import threading
import os
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import cv2
import mss
import queue
from queue import Queue
import json
import keyboard
from functools import lru_cache
from logging.handlers import RotatingFileHandler
import gc

# Define the base folder for images
base_folder = os.path.join(os.path.dirname(__file__), "data")
# Define the base folder for logs
log_folder = os.path.join(os.path.dirname(__file__), "logs")
#Define the folder for setups
setup_folder = os.path.join(os.path.dirname(__file__),  "setups")

# Ensure the folders exists
if not os.path.exists(setup_folder):
    os.makedirs(setup_folder)
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
# Define the log file path and setup
log_file = os.path.join(log_folder, "bot.log")
setup_file = os.path.join(setup_folder, "saved_setups.json")
default_xp_file = os.path.join(setup_folder, "default_xp.json")
if os.path.exists(log_folder):
   try:
       os.remove(log_file)
       print ("Old log file deleted")
   except Exception as e:
       print(f"Error deleting old log file:{e}")
#Log handler
handler = RotatingFileHandler(log_file, maxBytes=200 * 1024, backupCount=0)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Gold templates
gold_path = os.path.join(base_folder, "gold.png") # Replace with your template file
gold = cv2.imread(gold_path, 0)  # Load in grayscale

gold10=(1222,1108)
gold10_color=[255, 232, 82]

#available_cards
available_cards = { 
    "Abomination":os.path.join(base_folder, "abomination.png"),
    "Ancient of war":os.path.join(base_folder, "ancient_of_war.png"),
    "Anub'arak":os.path.join(base_folder, "anub.png"),
    "Bandits": os.path.join(base_folder, "bandits.png"),
    "Bat Rider": os.path.join(base_folder, "bat_rider.png"),
    "Charlga":os.path.join(base_folder, "charlga.png"),
    "Chimaera":os.path.join(base_folder, "chimaera.png"),
    "Darkspear troll":os.path.join(base_folder, "darkspear_troll.png"),
    "Dire batling":os.path.join(base_folder, "bats.png"),
    "Dryad": os.path.join(base_folder, "dryad.png"), 
    "Emperor Thaurissan":os.path.join(base_folder, "et.png"),
    "Faerie Dragon":os.path.join(base_folder, "faerie_dragon.png"),
    "Fire elemental":os.path.join(base_folder, "fire_elemental.png"),
    "Gargoyle":os.path.join(base_folder, "gargoyle.png"),
    "General Drakkisath":os.path.join(base_folder, "drakkisath.png"),
    "Ghoul": os.path.join(base_folder, "ghoul.png"), 
    "Gryphon rider":os.path.join(base_folder, "gryphon_rider.png"),
    "Harpies":os.path.join(base_folder, "harpies.png"),
    "Harvest golem":os.path.join(base_folder, "harvest_golem.png"),
    "Hogger":os.path.join(base_folder, "hogger.png"),
    "Huntress":os.path.join(base_folder, "huntress.png"),
    "Kobold Miner": os.path.join(base_folder, "kobold.png"),
    "Lich King":os.path.join(base_folder, "lich_king.png"),
    "Malfurion":os.path.join(base_folder, "malfurion.png"),
    "Meat Wagon":os.path.join(base_folder, "meat_wagon.png"),
    "Murlocs tidehunter":os.path.join(base_folder, "murlocs.png"),
    "Old Murk-Eye":os.path.join(base_folder, "murk.png"),
    "Orgrim":os.path.join(base_folder, "orgrim.png"),
    "Plague Farmer":os.path.join(base_folder, "plague_farmer.png"),
    "Priestess":os.path.join(base_folder, "priestess.png"),
    "Prowler":os.path.join(base_folder, "prowler.png"),
    "Rend":os.path.join(base_folder, "rend.png"),
    "Shaman":os.path.join(base_folder, "shaman.png"),
    "Spiders":os.path.join(base_folder, "spiders.png"),
    "Swole Troll": os.path.join(base_folder, "swoletroll.png"),
    "Sylvanas": os.path.join(base_folder, "sylvanas.png"),
    "Thrall": os.path.join(base_folder, "thrall.png"),
    "Vultures": os.path.join(base_folder, "vultures.png"),
    "Witch Doctor": os.path.join(base_folder, "witchdoctor.png"),  
}
templates = {    
    "lvl_11": cv2.imread(os.path.join(base_folder, "lvl_11.png"), cv2.IMREAD_UNCHANGED),
    "lvl_11_resistant": cv2.imread(os.path.join(base_folder, "lvl_11_resistant.png"), cv2.IMREAD_UNCHANGED),
    "lvl_11_armored": cv2.imread(os.path.join(base_folder, "lvl_11_armored.png"), cv2.IMREAD_UNCHANGED),
    "lvl_10": cv2.imread(os.path.join(base_folder, "lvl_10.png"), cv2.IMREAD_UNCHANGED),
    "lvl_10_resistant": cv2.imread(os.path.join(base_folder, "lvl_10_resistant.png"), cv2.IMREAD_UNCHANGED),
    "lvl_10_armored": cv2.imread(os.path.join(base_folder, "lvl_10_armored.png"), cv2.IMREAD_UNCHANGED),
    "lvl_9": cv2.imread(os.path.join(base_folder, "lvl_9.png"), cv2.IMREAD_UNCHANGED),
    "lvl_9_resistant": cv2.imread(os.path.join(base_folder, "lvl_9_resistant.png"), cv2.IMREAD_UNCHANGED),
    "lvl_9_armored": cv2.imread(os.path.join(base_folder, "lvl_9_armored.png"), cv2.IMREAD_UNCHANGED),
    "lvl_8": cv2.imread(os.path.join(base_folder, "lvl_8.png"), cv2.IMREAD_UNCHANGED),
    "lvl_8_resistant": cv2.imread(os.path.join(base_folder, "lvl_8_resistant.png"), cv2.IMREAD_UNCHANGED),
    "lvl_8_armored": cv2.imread(os.path.join(base_folder, "lvl_8_armored.png"), cv2.IMREAD_UNCHANGED), 
}
spell_or_unbound={
    "Blizzard":os.path.join(base_folder, "blizzard.png"),
    "Execute":os.path.join(base_folder, "execute.png"),
    "Polymorph":os.path.join(base_folder, "polymorph.png"),
    "Quillboar":os.path.join(base_folder, "quillboar.png"),
    "Safe pilot":os.path.join(base_folder, "safe_pilot.png"),
    "Skeleton Army":os.path.join(base_folder, "skeleton_army.png"),
    "Whelps":os.path.join(base_folder, "whelp_eggs.png"),
}
game_window = {"top": 140, "left": 27, "width": 1911, "height": 1090}
# This will hold detected enemy units
detected_units_queue = Queue()

def update_combo_1():
    global selected_combo_1, combo_1_cost
    card1 = combo1_card1_var.get()
    card2 = combo1_card2_var.get()
    cost = combo1_cost_var.get()

    # Debugging print
    print(f"Combo 1 Selection: Card1={card1}, Card2={card2}, Cost={cost}")

    if card1 in available_cards and card2 in available_cards:
        selected_combo_1[0] = available_cards[card1]
        selected_combo_1[1] = available_cards[card2]
        combo_1_cost = int(cost) if cost.isdigit() and 1 <= int(cost) <= 10 else 1  # Ensure valid cost
    else:
        print("Error: Selected card(s) not found in available_cards.")

def update_combo_2():
    global selected_combo_2, combo_2_cost
    card1 = combo2_card1_var.get()
    card2 = combo2_card2_var.get()
    cost = combo2_cost_var.get()

    # Debugging print
    print(f"Combo 2 Selection: Card1={card1}, Card2={card2}, Cost={cost}")

    if card1 in available_cards and card2 in available_cards:
        selected_combo_2[0] = available_cards[card1]
        selected_combo_2[1] = available_cards[card2]
        combo_2_cost = int(cost) if cost.isdigit() and 1 <= int(cost) <= 10 else 1  # Ensure valid cost
    else:
        print("Error: Selected card(s) not found in available_cards.")

def update_not_upgradeable():
    global selected_not_upgradeable, not_upgradeable_cost
    selected_not_upgradeable = available_cards[not_upgradeable_var.get()]
    not_upgradeable_cost = int(not_upgradeable_cost_var.get())
    print(f"Updated Not upgradeable: {selected_not_upgradeable}, Cost: {not_upgradeable_cost}")

def update_spell_or_unbound():
    global selected_spell_or_unbound, spell_or_unbound_cost
    selected_spell_or_unbound = spell_or_unbound[spell_or_unbound_var.get()]
    spell_or_unbound_cost = int(spell_or_unbound_cost_var.get())
    print(f"Updated spell or unbound: {selected_spell_or_unbound}, Cost: {spell_or_unbound_cost}")
victory_region=(655,131,600,200)
# Function to detect victory and increment the counter
def update_quest_counter():
    quest_count_var.set(quest_count_var.get() + 1)
    quest_label.config(text=str(quest_count_var.get()))  # Update UI

    check_stop_conditions()

def check_stop_conditions():
    try:
        if remaining_xp <= 0 or quest_count_var.get() >= int(max_quests_var.get()):
             # Step 1: Press Esc key to bring up the quit menu
            keyboard.press_and_release('esc')
            time.sleep(5)

            # Step 2: Try to locate and click the quit_game button
            quit_location = locate_image_with_retries(quit_game, retries=5, confidence=0.7,grayscale=True)

            if quit_location:
                click_direct(*quit_location)
            else:
                print("Could not locate the 'quit_game' button on screen.")
            print("Stopping bot: XP or Quest limit reached.")
            stop_bot()
    except ValueError:
        print("Invalid XP or Quest limit value")

def detect_victory(victory):
    global victory_count
    try:
        location = pyautogui.locateOnScreen(victory, region=victory_region, confidence=0.8)
        if location:
            victory_count += 1
            print(f"Victory detected! Current count: {victory_count}")
            calculate_result(mode="pvp")
            return True
        else:
            print("Victory image not found.")
            return False
    except pyautogui.ImageNotFoundException:
        print("Loss")
        return False
    
def detect_victory_quest(victory):
    global victory_count

    try:
        location = pyautogui.locateOnScreen(victory, region=victory_region, confidence=0.8)
        if location:
            victory_count += 1
            print(f"[QUEST] Victory detected! Count: {victory_count}")
            calculate_result(mode="quest")
            return True
        else:
            print("[QUEST] No victory image found.")
            return False
    except pyautogui.ImageNotFoundException:
        print("[QUEST] Image not found exception")
        return False

def initialize_xp_goal():
    global remaining_xp
    try:
        remaining_xp = int(max_xp_var.get())  # Set initial XP goal
        result_label.config(text=f"Remaining XP: {remaining_xp:,}")
    except ValueError:
        result_label.config(text="Invalid XP Goal")

def calculate_result(mode="pvp"):
    global remaining_xp, temp_xp_reward

    try:
        if mode == "pvp":
            xp = int(exp_for_victory_var.get())
        elif mode == "quest":
            xp = temp_xp_reward
        else:
            print(f"[ERROR] Unknown mode in calculate_result: {mode}")
            return

        remaining_xp = max(0, remaining_xp - xp)
        result_label.config(text=f"Remaining XP: {remaining_xp:,}")
        print(f"[{mode.upper()}] XP deducted: {xp}, Remaining: {remaining_xp}")
        check_stop_conditions()

        if mode == "quest":
            temp_xp_reward = 0  # Reset only for quest flow

    except ValueError:
        result_label.config(text="Invalid XP input")

# Define image filenames 
start_button = os.path.join(base_folder, "Pvpbutton.png")
stop_button = os.path.join(base_folder, "stop_button.png")
quit_game=os.path.join(base_folder, "quit_game.png")
back_button = os.path.join(base_folder, "back_button.png")
miner_card = os.path.join(base_folder, "kobold.png")
chest_card = os.path.join(base_folder, "bandits.png")
rumble_button = os.path.join(base_folder, "rumble_button.png")
victory = os.path.join(base_folder, "victory.png")
purple_quest = os.path.join(base_folder, "purple_quest.png")
world_map_button=os.path.join(base_folder, "world_map_quest.png")
barrack=os.path.join(base_folder, "barrack.png")
barrack_1=os.path.join(base_folder, "barrack_1.png")
barrack_2=os.path.join(base_folder, "barrack_2.png")
start_quest=os.path.join(base_folder, "start_quest.png")
claim_quest=os.path.join(base_folder, "claim_quest.png")
claim_card=os.path.join(base_folder, "claim_card.png")
play_quest=os.path.join(base_folder, "play_quest.png")
lvl_up=os.path.join(base_folder, "lvl_up.png")
quest_image=os.path.join(base_folder, "quest.png")
#selecting_combos
selected_combo_1 = [None, None]
selected_combo_2 = [None, None]
selected_not_upgradeable = None
selected_spell_or_unbound=None
combo_1_cost = 8
combo_2_cost = 4
not_upgradeable_cost = 6
spell_or_unbound_cost = 4
#amount of exp
victory_count = 0

bot_running = threading.Event()

#Map recognition files
map1_image = os.path.join(base_folder, "map_1.png")
map2_image = os.path.join(base_folder, "map_2.png")
map3_image = os.path.join(base_folder, "map_3.png")
map4_image = os.path.join(base_folder, "map_4.png")
map5_image = os.path.join(base_folder, "map_5.png")

#arrow region
#map1
arrow_x_map1=random.randint(602,647)
arrow_y_map1=random.randint(476,516)
map_scroll_x_1=random.randint(1460,1560)
map_scroll_y_1=random.randint(714,820)
#map2
arrow_x_map2=random.randint(1248,1281)
arrow_y_map2=random.randint(381,415)
map_scroll_x_2=random.randint(1440,1540)
map_scroll_y_2=random.randint(708,848)
#map3
arrow_x_map3=random.randint(700,730)
arrow_y_map3=random.randint(247,277)
map_scroll_x_3=random.randint(1410,1512)
map_scroll_y_3=random.randint(506,642)
#map4
arrow_x_map4=random.randint(645,680)
arrow_y_map4=random.randint(39,42)
map_scroll_x_4=random.randint(539,657)
map_scroll_y_4=random.randint(642,710)
#map5
map_scroll_x_5=random.randint(1350,1450)
map_scroll_y_5=random.randint(588,726)
#gold region
gold_region=(830,1099,420,40)


# Screen regions
gold_mine_location = [(874, 385), (1100, 184), (1110, 315), (709, 309)]
hand_region = (770, 930, 500, 170)  # Region where cards appear
gold_region={"top": 1105, "left": 830, "width": 450, "height": 30}#gold_region = (830, 1105, 450, 30) Region of gold bar
switch_region_1=(612,480,55,55)#region switch 1
switch_region_2=(1256,373,75,75)#region switch 2
rumble_region=(970, 990, 250, 100)#rumble region
start_region=(967, 918, 300, 100)#pvp region
stop_region=(820, 990, 260, 100)#stop region
map_region=(1269,948,420,270)#map recognition region
world_map_region=(980,985,250,100)#get back home from quests
quest_region=(650,900, 300, 100) #quest region
back_button_region=(701,1012,230,100)#back region pvp
claim_region=(600,810,700,200)
play_quest_region=(662,847,600,100)
start_quest_region=(805,844,300,200)
play_buttons=[(700,800,890,910),(913,1013,890,910),(1115,1215,890,910)]#play buttons
barrack_region=(27,140,1911,1090)
lvl_up_region=(799,81,320,100)
# Setup Logging
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Global bot running flag (this should be a threading.Event())
bot_running = threading.Event()
#threadpool
executor = ThreadPoolExecutor(max_workers=8)
# Helper Functions
def moveMouse(x, y):
    """Move the mouse to (x, y) with a more human-like movement"""
    
    # Move using a slightly curved path
    pyautogui.moveTo(x, y, duration=random.uniform(0.05, 0.15), tween=pyautogui.easeInOutQuad)

    # Simulate slight jitter at the end of movement
    if random.random() > 0.7:  # 30% chance to add jitter
        pyautogui.moveTo(x + random.uniform(-1, 1), y + random.uniform(-1, 1), duration=0.02)

def click_direct(x, y):
    """Click at (x, y) with human-like delays and behavior"""
    moveMouse(x, y)
    
    # Simulate human reaction time before clicking
    time.sleep(np.random.uniform(0.15, 0.25))
    
    # Click the mouse
    pyautogui.click()
    
    # Random delay after click (humans don't act instantly)
    time.sleep(np.random.uniform(0.1, 0.3))

    # Occasionally add a tiny follow-up movement (simulating hand repositioning)
    if random.random() > 0.8:  # 20% chance
        pyautogui.moveTo(x + random.uniform(-3, 3), y + random.uniform(-3, 3), duration=0.05)

def locate_image_with_retries(image_path, retries=3, confidence=0.8, region=None,grayscale=None):
    attempt = 0
    while attempt < retries:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=region,grayscale=grayscale)
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            logging.warning(f"Image {image_path} not found, retrying... ({attempt + 1}/{retries})")
        attempt += 1
        time.sleep(0.7)  # Give it a short delay before retrying
    logging.error(f"Image {image_path} could not be found after {retries} retries.")
    return None  # Return None if the image is not found after retries

# Gold detection
def is_color_above_threshold(current_color, target_color, tolerance=5):
    return all(c >= t - tolerance for c, t in zip(current_color, target_color))

def get_current_gold(mss_instance,gold_region,threshold=0.983,gold10=(1222, 1108), gold10_color=[255, 232, 82]):
    """Detects the number of gold coins in the gold bar region."""
    
    
    gold_screenshot = np.array(mss_instance.grab(gold_region))

     # Check if the gold10 pixel matches the gold10 color
    gold10_pixel = pyautogui.pixel(*gold10)  # Get the pixel color at gold10's position
    if is_color_above_threshold(gold10_pixel, gold10_color,tolerance=5):
        return 10  # Return 10 if the gold10 color is detected 
    gray = cv2.cvtColor(gold_screenshot, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Match the gold in the region
    result = cv2.matchTemplate(gray, gold, cv2.TM_CCOEFF_NORMED)
    
    # Get locations where the result is above the threshold
    loc = np.where(result >= threshold)
    
    # Count the number of matches
    detected_coins = len(list(zip(*loc[::-1])))  # Converts loc to list of coordinates
    
    return detected_coins
def scroll_map(x,y,distance):
    pyautogui.moveTo(x,y, duration=random.uniform(0.05, 0.15), tween=pyautogui.easeInOutQuad)
    time.sleep(0.2)
    pyautogui.mouseDown(x,y)  # Hold left click
    pyautogui.moveTo(x,y + distance, duration=0.2)  # Move cursor down ok
    pyautogui.mouseUp()  # Release click

    

#Map recognition
def identify_map():
    map_images = [map1_image, map2_image, map3_image, map4_image, map5_image]

    results = executor.map(
        locate_image_with_retries, 
        map_images, 
        [1]*len(map_images),            # retries
        [0.85]*len(map_images),          # confidence
        [map_region]*len(map_images),   # region
        [True]*len(map_images)          # grayscale
    )
    
    # Iterate over the results to identify the map
    for map_location, map_image in zip(results, map_images):
        if map_location:
            map_name = os.path.basename(map_image).split('.')[0]  # Extract map name from image file
            logging.info(f"Map identified: {map_name} with confidence 0.85")
            return map_name
    
    return None  # No map identified
def perform_map_action(map_name):
    if map_name == "map_1":
        click_direct(arrow_x_map1,arrow_y_map1)
        time.sleep(0.1)
        scroll_map(map_scroll_x_1,map_scroll_y_1,190)
        enemy_detection_zones=[(560,1043,150,700),(480,690,700,910),(770, 1360, 820, 890),(1080,1400,161,651)]
        deploy_card = [(485, 660, 800, 900), (770, 940, 820,890),(1175, 1360, 570, 660)]
        deploy_dumbcombo = [(760, 940, 820, 890), (1175, 1360, 570, 740)]
        deploy_chest=[(485, 700, 620, 1000)]
        deploy_miner=[(770, 940, 820, 890)]
    
    elif map_name == "map_2":
        click_direct(arrow_x_map2,arrow_y_map2)
        time.sleep(0.1)
        scroll_map(map_scroll_x_2,map_scroll_y_2,250)
        enemy_detection_zones=[(518,757,541,914),(808,1152,158,897),(578,748,141,403),(1178,1432,399,893)]
        deploy_card = [(510, 750, 820, 890), (830, 1019, 850, 890),(540,740,290,510),(1180,1440,790,900)] #deployment tl,tr,up towerl,tower r
        deploy_dumbcombo = [(830, 1019, 850, 890), (555, 721, 330, 470)]
        deploy_chest=[(480, 630, 930, 1080)]
        deploy_miner=[(830, 1019, 850, 890)]

    elif map_name == "map_3":
        click_direct(arrow_x_map3,arrow_y_map3)
        time.sleep(0.1)
        scroll_map(map_scroll_x_3,map_scroll_y_3,290)
        enemy_detection_zones=[(580,938,216,887),(995,1265,485,899),(1157,1362,142,488),(808,1108,147,502)]
        deploy_card = [(736, 920, 760, 877), (1050, 1200, 760, 877),(1157, 1336, 277, 434)]
        deploy_dumbcombo = [(1050, 1200, 760, 877), (1157, 1336, 277, 434)]
        deploy_chest=[(736, 920, 760, 877), (1050, 1200, 760, 877)]
        deploy_miner=[(736, 920, 760, 877), (1050, 1200, 760, 877)]

    
    elif map_name == "map_4":
        click_direct(arrow_x_map4,arrow_y_map4)
        time.sleep(0.1)
        scroll_map(map_scroll_x_4,map_scroll_y_4,300)
        enemy_detection_zones=[(546,778,150,867),(871,1055,310,896),(1158,1359,145,554)]
        deploy_card = [(513, 725, 733, 850), (850, 1016, 733, 850),(1140, 1313, 424, 500)]
        deploy_dumbcombo = [(513, 725, 733, 850), (1140, 1313, 424, 500)]
        deploy_chest=[(850, 1016, 738, 890)]
        deploy_miner=[(513, 725, 733, 850),(1160, 1300, 424, 500)]

    elif map_name == "map_5":
        scroll_map(map_scroll_x_4,map_scroll_y_4,200)
        enemy_detection_zones=[(647,919,188,900),(990,1218,670,905),(1021,1180,161,600)]
        deploy_card = [(718, 953, 790, 890), (970, 1205, 790, 890),(1002, 1169, 600, 700)]
        deploy_dumbcombo = [(970, 1205, 790, 890), (1002, 1169, 455, 605)]
        deploy_chest=[(718, 953, 790, 890), (970, 1205, 790, 890)]
        deploy_miner=[(718, 953, 790, 890)]
    
    else:
        logging.error(f"Unknown map name: {map_name}")
        return None, None, None, None, None

    # FINAL VALIDATION
    if not enemy_detection_zones or not deploy_card or not deploy_dumbcombo:
        logging.error(f"Incomplete deployment data for map: {map_name}")
        return None, None, None, None, None

    return deploy_card, deploy_dumbcombo,deploy_chest,deploy_miner,enemy_detection_zones  # Return the ranges instead of fixed values
#Enemy's detection
def is_duplicate(new_pt, existing_pts, min_distance=10):
    for pt in existing_pts:
        dist = np.linalg.norm(np.array(new_pt) - np.array(pt))
        if dist < min_distance:
            return True
    return False

def is_red_area(region):
    """Optimized red area detection using BGR instead of HSV"""
    lower_red1 = np.array([0, 0, 180], dtype=np.uint8)  # Red in BGR
    upper_red1 = np.array([100, 100, 255], dtype=np.uint8)

    # Create a mask for red detection
    red_mask = cv2.inRange(region, lower_red1, upper_red1)

    # Calculate percentage of red pixels
    red_percentage = np.count_nonzero(red_mask) / (region.size / 3)
    return red_percentage > 0.009 
 
def find_largest_enemy_cluster(detected_enemies, distance_threshold=100, min_cluster_size=4):
    """Find the largest cluster of enemies and return its center."""
    if not detected_enemies:
        return None  # No enemies detected

    clusters = []
    visited = set()

    for i, (x1, y1) in enumerate(detected_enemies):
        if i in visited:
            continue  # Skip already clustered enemies
        
        cluster = [(x1, y1)]
        for j, (x2, y2) in enumerate(detected_enemies):
            if i != j:
                dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if dist <= distance_threshold:
                    cluster.append((x2, y2))
                    visited.add(j)

        clusters.append(cluster)

    # Find the largest cluster that meets the min_cluster_size condition
    largest_cluster = max([cluster for cluster in clusters if len(cluster) >= min_cluster_size], key=len, default=[])

    if not largest_cluster:
        return None  # No valid cluster found

    # Compute the center of the largest cluster
    x_cluster = sum(x for x, y in largest_cluster) // len(largest_cluster)
    y_cluster = sum(y for x, y in largest_cluster) // len(largest_cluster)

    logging.info(f"Targeting spell at largest cluster ({x_cluster}, {y_cluster}) with {len(largest_cluster)} enemies")
    return (x_cluster, y_cluster + 200)

def detect_enemy_units_in_realtime(mss_instance, monitor, threshold=0.805):
    try:
        screenshot = np.array(mss_instance.grab(monitor))

        if screenshot is None:
            print("Failed to capture screen.")
            return []

        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        # Downscale frame for faster processing
        frame_resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        detected_enemies = []
        seen_pts = []

        for name, template in templates.items():
            if template is None:
                continue

            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template

            # Resize template to match the downscaled frame
            template_resized = cv2.resize(template_gray, (0, 0), fx=0.5, fy=0.5)

            # Perform template matching
            result = cv2.matchTemplate(frame_gray, template_resized, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)

            w, h = template_resized.shape[1], template_resized.shape[0]

            for pt in zip(*locations[::-1]):
                if is_duplicate(pt, seen_pts):
                    continue
                seen_pts.append(pt)
                # Scale back coordinates to original size
                x, y = int(pt[0] * 2), int(pt[1] * 2)
                region = frame[y:y + h * 2, x:x + w * 2]

                if is_red_area(region):
                    detected_enemies.append((x, y))

        return detected_enemies
    except Exception as e:
        print(f"Error capturing or processing screen: {e}")
        return []
        

def process_enemy_positions(detected_enemies, enemy_detection_zones, deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, map_now):
    """Process detected enemies and decide where to deploy counter units based on the map."""
    
    # Initialize enemy count per zone
    enemy_count = [0] * len(enemy_detection_zones)

    # Function to count enemies in a given zone
    def count_enemy_in_zone(unit):
        x, y = unit
        for idx, (x1, x2, y1, y2) in enumerate(enemy_detection_zones):
            if x1 <= x <= x2 and y1 <= y <= y2:
                enemy_count[idx] += 1

    # Use thread pool to count enemies in different zones
    list(executor.map(count_enemy_in_zone, detected_enemies))

    # If no enemies are detected, choose random deployments
    if sum(enemy_count) == 0:
        card_deploy = deploy_card[0] if map_now in ["map_1", "map_2"] else random.choice([deploy_card[0], deploy_card[1]])
        combo_deploy = deploy_dumbcombo[1]
        chest_deploy = random.choice(deploy_chest)
        miner_deploy = random.choice(deploy_miner)
        if switch_to_card_deploy_var.get():
            combo_deploy = card_deploy
        if switch_special_card_priority_var.get():
        # If toggle is ON, deploy the AOW card even if no enemies are detected
            optional_aow_drop = deploy_card[1]  # Set the AOW drop location as required
            return card_deploy, combo_deploy, chest_deploy, miner_deploy, optional_aow_drop
        else:
            # If toggle is OFF, return None for AOW drop
            return card_deploy, combo_deploy, chest_deploy, miner_deploy, None

    # Determine min and max enemy zones
    max_enemy_zone = enemy_count.index(max(enemy_count))

    # Map-specific deployment logic (NO threading needed)
    def process_map_deployments(map_now, max_enemy_zone):
        """Determine the card and combo deployment based on the map and enemy zone."""
        map_config = {
            "map_1": [(0, 1), (0, 1), (1, 0), (2, 0)],
            "map_2": [(0, 0), (1, 1), (2, 1), (3, 1)],
            "map_3": [(0, 1), (1, 0), (2, 0), (0, 1)],
            "map_4": [(0, 1), (1, 0), (2, 1)],
            "map_5": [(0, 1), (1, 0), (2, 1)],
        }
        return deploy_card[map_config[map_now][max_enemy_zone][0]], deploy_dumbcombo[map_config[map_now][max_enemy_zone][1]]

    # Process deployment choices
    card_deploy, combo_deploy = process_map_deployments(map_now, max_enemy_zone)

    # Choose random chest and miner deployment
    chest_deploy = random.choice(deploy_chest) if deploy_chest else None
    miner_deploy = random.choice(deploy_miner) if deploy_miner else None

    if switch_special_card_priority_var.get():
        optional_aow_drop = deploy_card[1]  # Assign AOW drop (second deployment card)
        return card_deploy, combo_deploy, chest_deploy, miner_deploy, optional_aow_drop  # Return the AOW drop

    if switch_to_card_deploy_var.get():
        combo_deploy = card_deploy

    return card_deploy, combo_deploy, chest_deploy, miner_deploy,None

def find_and_set_quest_type():
    global temp_xp_reward

    # Step 1: Confirm the quest is visible using template matching
    quest_found = locate_image_with_retries(quest_image, retries=2,region=quest_region,confidence=0.7,grayscale=True)
    if quest_found is None:
        logging.info("Quest template not found. Skipping.")
        return False

    logging.info("Quest template found. Checking pixel color to determine quest type...")

    # Step 2: Use your original, fixed pixel position for color detection
    check_x, check_y = 735, 971
    try:
        r, g, b = pyautogui.pixel(check_x, check_y)
        logging.info(f"Pixel at ({check_x}, {check_y}) -> RGB: ({r}, {g}, {b})")

        if g < 120:
            if g > 30:
                temp_xp_reward = int(blue_xp_var.get())
                logging.info("Blue quest detected. XP reward set.")
            else:
                temp_xp_reward = int(purple_xp_var.get())
                logging.info("Purple quest detected. XP reward set.")
            return True
        else:
            if archlight_energy_farm_var.get():
                temp_xp_reward = int(blue_xp_var.get()) // 3
                logging.info("Green quest detected and accepted (Archlight farm mode ON).")
                return True
            else:
                logging.info("Green quest detected but skipped (Archlight farm mode OFF).")
                return False

    except Exception as e:
        logging.info(f"Error reading pixel: {e}")
        return False
    
def get_deployment_zone_using_barrack():
    # Locate the barrack's center
    barrack_center = locate_image_with_retries(barrack, retries=1, confidence=0.7,region=barrack_region,grayscale=True)
    
    if not barrack_center:
        logging.warning("Barrack not found. Trying alternative image...")
        barrack_center = locate_image_with_retries(barrack_1, retries=1, confidence=0.7, region=barrack_region, grayscale=True)
    
    if not barrack_center:
        logging.warning("Barrack not found. Trying alternative image...")
        barrack_center = locate_image_with_retries(barrack_2, retries=1, confidence=0.7, region=barrack_region, grayscale=True)

    if barrack_center:
        logging.info(f"Barrack found at coordinates:{barrack_center}")
        deploy_quest = (barrack_center[0] - 200, barrack_center[0] + 200, barrack_center[1] - 100, barrack_center[1] + 50)
        return deploy_quest
    else:
        logging.warning("Barrack not found. Using fallback deployment area.")
        deploy_quest=(820,1090,620,840)
        return deploy_quest  # Fallback deployment area if barrack isn't found
    
def wait_for_game_to_load():
    """Wait until the game is fully loaded and the start button appears.
    If play quest is still on screen, click it and abort this round so it retries.
    """
    start_quest_location = None
    timeout = time.time() + 30  # max wait of 30 seconds
    fallback_pixel_time = time.time() + 15  # Only use pixel fallback after 15 seconds

    while not start_quest_location and time.time() < timeout:
        # Case 1: Start quest button appears
        start_quest_location = locate_image_with_retries(start_quest, retries=2, confidence=0.5, region=start_quest_region, grayscale=True)
        if start_quest_location:
            logging.info("Game loaded, Start button found.")
            return start_quest_location

        # Case 2: Play quest is still there → means it never started
        play_quest_location = locate_image_with_retries(play_quest, retries=1, confidence=0.8, region=play_quest_region, grayscale=True)
        if play_quest_location:
            logging.warning("Play Quest still visible! Likely quest did not start. Clicking fallback point and retrying.")
            click_direct(603, 398)  # <- your fallback click spot
            time.sleep(np.random.uniform(0.3, 0.6))
            return None  # return early to retry the main flow

        # Case 3: After 15s, use pixel color fallback
        if time.time() >= fallback_pixel_time:
            pixel_coords = (972, 897)  # Example pixel position
            current_color = pyautogui.pixel(*pixel_coords)
            target_color = (252, 215, 31)  # Example RGB threshold

            if is_color_above_threshold(current_color, target_color, tolerance=10):
                logging.info(f"Pixel color above threshold at {pixel_coords}. Using as fallback for Start.")
                return pixel_coords  # Use this as a fallback "start_quest_location"

        logging.info("Waiting for Start button...")
        time.sleep(1)

    logging.warning("Timeout reached without detecting Start or Play Quest screen.")
    return None


def find_multiple_cards(card_images):
    """Find multiple cards using a thread pool for parallel processing."""
    futures = [executor.submit(find_card, card) for card in card_images]
    results = []
    
    for future in futures:
        try:
            results.append(future.result())  # Collect results safely
        except Exception as e:
            logging.error(f"Error finding card: {e}")
            results.append(None)  # Avoid crashing, return None for failed tasks

    return results

def find_card(card_image, offset=5):
    """Find the card on screen and return its location with a slight random offset."""
    try:
        location = pyautogui.locateCenterOnScreen(card_image, confidence=0.85, region=hand_region, grayscale=True)
        if location:
            x, y = location
            x += random.randint(-offset, offset)
            y += random.randint(-offset, offset)
            return x, y
        return None
    except Exception as e:
        logging.error(f"Error finding card {card_image}: {e}")
        return None
def play_card(card, x, y):
    try:
        click_direct(*card)
        time.sleep(np.random.uniform(0.2, 0.5))  # Increased sleep time
        click_direct(x, y)
    except Exception as e:
        logging.error(f"Error playing card {card} at ({x}, {y}): {e}")

temp_xp_reward = 0
bot_restart_lock = threading.Lock()
def main(): 
    initialize_xp_goal()
    with mss.mss() as mss_instance:
        while bot_running.is_set():
            # First, check for the Rumble button (if we're already in the Rumble window)
            rumble_button_location = locate_image_with_retries(rumble_button, retries=2, confidence=0.6,region=rumble_region,grayscale=True)
            rumblebutton_x = random.randint(1011, 1168)
            rumblebutton_y = random.randint(1020, 1060)
            stop_button_location = locate_image_with_retries(stop_button, retries=1, confidence=0.8,region=stop_region,grayscale=True)
            claim_quest_location = locate_image_with_retries(claim_quest,retries=1, confidence=0.8,region=claim_region,grayscale=True)
            claim_card_location=locate_image_with_retries(claim_card,retries=1, confidence=0.8,region=claim_region,grayscale=True)
            play_quest_location=locate_image_with_retries(play_quest,retries=1,confidence=0.8,region=play_quest_region,grayscale=True)
            lvl_up_location = locate_image_with_retries(lvl_up, retries=1, confidence=0.8, region=lvl_up_region, grayscale=True)
            
            # Initialize the flags before the loop
            map_checked = False  #Track if map is checked
            match_started = False  # Track if the match has started

            if keyboard.is_pressed("q"):  # If 'q' is pressed, stop the bot
                print("Stopping bot...")
                bot_running.clear()  # Stop the bot
                break #exit loop 
            if lvl_up_location:
                click_direct(603,398)
                time.sleep(np.random.uniform(0.3, 0.6))
                continue  
            if switch_quest_mode_var.get() and play_quest_location:
                click_direct(603,398)
                time.sleep(np.random.uniform(0.2, 0.5))
                continue
            if stop_button_location:
                click_direct(*stop_button_location)
                time.sleep(np.random.uniform(0.2, 0.5))  # Delay for smoothness
                continue

            if rumble_button_location:
                # If Rumble button is found, click it
                click_direct(rumblebutton_x, rumblebutton_y)
                logging.info("Rumbling started.")
                time.sleep(5)  # Wait for game to fully load
                continue  # Continue the loop after clicking rumble button
            if switch_quest_mode_var.get() and (claim_quest_location or is_color_above_threshold(pyautogui.pixel(919, 971), (190, 141, 16), tolerance=10)):
                if claim_card_location:
                    claim_click_quest=claim_quest_location
                else:
                    claim_click_quest=(919,971)
                click_direct(*claim_click_quest)
                time.sleep(np.random.uniform(4,5))
                claim_card_location=locate_image_with_retries(claim_card,retries=3, confidence=0.8,region=claim_region,grayscale=True)
                if claim_card_location:
                    time.sleep(np.random.uniform(1,2))
                    click_direct(*claim_card_location)
                    time.sleep(np.random.uniform(6,7))
                    lvl_up_location = locate_image_with_retries(lvl_up, retries=3, confidence=0.8, region=lvl_up_region, grayscale=True)
                    if lvl_up_location:
                        click_direct(603,398)
                        time.sleep(np.random.uniform(0.3, 0.6))
                    continue
                else:
                    moveMouse(603,398)
                    time.sleep(30)
                    continue
            if switch_quest_mode_var.get() and claim_card_location:
                click_direct(*claim_card_location)
                time.sleep(2)
                continue

            # If Rumble button was not found, check for the PvP (Start) button
            if switch_quest_mode_var.get():
                if find_and_set_quest_type():
                    time.sleep(np.random.uniform(1, 2))
                    click_direct(808,968)
                    time.sleep(1)
                    mission=random.choice(play_buttons)
                    x_min,x_max,y_min,y_max=mission
                    x_play,y_play=random.randint(x_min, x_max), random.randint(y_min, y_max)
                    click_direct(x_play,y_play)
                    moveMouse(949,711)
                    start_quest_location=wait_for_game_to_load()
                    if not start_quest_location:
                        logging.info("Quest start interrupted or failed, retrying whole setup.")
                        return # Go back to the top of the main loop
                    click_direct(*start_quest_location)
                    time.sleep(np.random.uniform(0.1, 0.3))
                    moveMouse(560,1040)
                    
                while bot_running.is_set():
                    current_gold = get_current_gold(mss_instance, gold_region)
                    logging.info(f"Current Gold: {current_gold}")

                    if current_gold == 0:
                        stop_button_location = locate_image_with_retries(stop_button, retries=1, confidence=0.8, region=stop_region, grayscale=True)
                        start_button_location = locate_image_with_retries(start_button, retries=1, confidence=0.8, region=start_region, grayscale=True)
                        world_map_button_location = locate_image_with_retries(world_map_button, retries=1, confidence=0.8, region=world_map_region, grayscale=True)
                        claim_card_location=locate_image_with_retries(claim_card,retries=1, confidence=0.8,region=claim_region,grayscale=True)
                        play_quest_location=locate_image_with_retries(play_quest,retries=1,confidence=0.8,region=play_quest_region,grayscale=True)

                        if stop_button_location:
                            logging.info("Stop button found, stopping cycle.")
                            update_quest_counter()
                            detect_victory_quest(victory)
                            click_direct(*stop_button_location)
                            time.sleep(np.random.uniform(0.2, 0.5))
                            break  
                        elif start_button_location:
                            logging.info("Pvp button found, exiting quest mode.")
                            break  
                        elif world_map_button_location:
                            logging.info("World map button found, exiting quest mode.")
                            click_direct(*world_map_button_location)
                            time.sleep(np.random.uniform(0.2,0.5))
                            break
                        elif claim_card_location or is_color_above_threshold(pyautogui.pixel(919, 971), (190, 141, 16), tolerance=10):
                            if claim_card_location:
                                claim_click_card=claim_card_location
                            else:
                                claim_click_card=(919,971)
                                
                            click_direct(*claim_click_card)
                            time.sleep(np.random.uniform(0.2,0.5))
                            time.sleep(np.random.uniform(6,7))
                            lvl_up_location = locate_image_with_retries(lvl_up, retries=3, confidence=0.8, region=lvl_up_region, grayscale=True)
                            if lvl_up_location:
                                logging.info("Mini leveled up")
                                click_direct(603,398)
                                time.sleep(np.random.uniform(0.3, 0.6))
                            break
                        elif play_quest_location:
                            logging.info("Play quest found, exiting quest mode.")
                            break  
  

                    if current_gold > 0 and not match_started:
                        match_started = True
                        logging.info("Quest Match started! Deploying units...")
                        deploy_quest = get_deployment_zone_using_barrack()


                    if  current_gold>0 and match_started:
                        detected_enemies = detect_enemy_units_in_realtime(mss_instance, game_window, threshold=0.8)
                        high_enemy_count = len(detected_enemies) >= 4  

                        # Check for card availability
                        combo_in_hand = find_multiple_cards(selected_combo_1)
                        control_in_hand = find_multiple_cards(selected_combo_2)
                        miner_in_hand = find_card(miner_card)
                        chest_in_hand = find_card(chest_card)
                        not_upgradeable_in_hand = find_card(selected_not_upgradeable)
                        spell_or_unbound_in_hand = find_card(selected_spell_or_unbound)

                        card_played = False  

                        # 🔹 **Combo 1 Deployment**
                        if all(combo_in_hand):
                            if current_gold < combo_1_cost:
                                logging.info(f"Combo ready but waiting for {combo_1_cost} gold. Current: {current_gold}")
                            else:
                                logging.info("Playing Combo 1!")
                                x_min, x_max, y_min, y_max = deploy_quest
                                x_combo, y_combo = random.randint(x_min, x_max), random.randint(y_min, y_max)

                                for index, card in enumerate(combo_in_hand):
                                    if card:
                                        if index == 1:
                                            x_combo += random.randint(-10, 10)
                                            y_combo += random.randint(-10, 10)
                                        play_card(card, x_combo, y_combo)
                                        time.sleep(np.random.uniform(0.1, 0.2))
                                card_played = True  

                        # 🔹 **Spell Deployment (unchanged)**
                        if switch_to_spell_or_unbound_deploy_var.get() and high_enemy_count and spell_or_unbound_in_hand and not card_played:
                            if current_gold < spell_or_unbound_cost:
                                logging.info("Waiting for gold to deploy spell/unbound")
                            else:
                                spell_target = find_largest_enemy_cluster(detected_enemies)
                                if spell_target:
                                    x_spell, y_spell = spell_target
                                    logging.info(f"Deploying Spell at cluster ({x_spell}, {y_spell})")
                                    play_card(spell_or_unbound_in_hand, x_spell, y_spell)
                                    card_played = True  

                        # 🔹 **Combo 2 Deployment**
                        elif not all(combo_in_hand):

                            if all(control_in_hand) and not card_played:
                                if current_gold < combo_2_cost:
                                    logging.info(f"Combo 2 ready but waiting for {combo_2_cost} gold. Current: {current_gold}")
                                else:
                                    logging.info("Playing Control Units cards!")
                                    x_min, x_max, y_min, y_max = deploy_quest
                                    x_card, y_card = random.randint(x_min, x_max), random.randint(y_min, y_max)

                                    for index, card in enumerate(control_in_hand):
                                        if card:
                                            if index == 1:
                                                x_card += random.randint(-10, 10)
                                                y_card += random.randint(-10, 10)
                                            play_card(card, x_card, y_card)
                                            time.sleep(np.random.uniform(0.1, 0.2))
                                    card_played = True  

                            # 🔹 **Chest Deployment**
                            elif chest_in_hand and not card_played and current_gold >= 1:
                                logging.info("Playing Chest card!")
                                x_min, x_max, y_min, y_max = deploy_quest
                                play_card(chest_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                card_played = True  

                            # 🔹 **Not Upgradeable Deployment (if enabled)**
                            elif switch_special_card_priority_var.get() and not_upgradeable_in_hand and not card_played:
                                if current_gold < not_upgradeable_cost:
                                    logging.info("Waiting for gold to deploy defense")
                                else:
                                    logging.info("Deploying Not Upgradeable card!")
                                    x_min, x_max, y_min, y_max = deploy_quest
                                    play_card(not_upgradeable_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                    card_played = True  

                            # 🔹 **Fallback: Miner Deployment**
                            elif miner_in_hand and not card_played and current_gold >= 1:
                                logging.info("Playing Miner card!")
                                x_min, x_max, y_min, y_max = deploy_quest
                                play_card(miner_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                card_played = True  

                            # 🔹 **Final Fallback: Deploy Not Upgradeable if nothing else played**
                            elif not card_played and not switch_special_card_priority_var.get() and current_gold >= not_upgradeable_cost and not_upgradeable_in_hand:
                                logging.info("Playing Not Upgradeable card as last option!")
                                x_min, x_max, y_min, y_max = deploy_quest
                                play_card(not_upgradeable_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                card_played = True  

                    time.sleep(np.random.uniform(0.2, 0.4))  # Smooth performance adjustment
                gc.collect()
            start_button_location = locate_image_with_retries(start_button, retries=5, confidence=0.90,region=start_region,grayscale=True)
            if start_button_location:
                # If Start button is found, click to enter PvP
                time.sleep(np.random.uniform(1, 2))  # Random delay for realism
                click_direct(*start_button_location)
                time.sleep(1)  # Wait for the game to start
                logging.info("Pressed PvP button")
                rumble_button_location = locate_image_with_retries(rumble_button, retries=2, confidence=0.6,region=rumble_region,grayscale=True)
                if not rumble_button_location:
                    logging.warning("Clicked blurred pvp button")
                    continue
                if rumble_button_location:
                    click_direct(rumblebutton_x, rumblebutton_y)
                    logging.info("Rumbling started")
                    time.sleep(5)  # Wait for game to fully load
            

            if not start_button_location and not rumble_button_location:
                logging.warning("Neither Start nor Rumble button found. Waiting before retrying...")
                time.sleep(3)  # Wait longer before retrying
                continue  # Skip restart unless this happens multiple times

            while bot_running.is_set():  
                # Keep running unless manually stopped
                current_gold = get_current_gold(mss_instance,gold_region)
                logging.info(f"Current Gold: {current_gold}")
                if keyboard.is_pressed("q"):  # If 'q' is pressed, stop the bot
                    print("Stopping bot...")
                    bot_running.clear()  # Stop the bot
                    break #exit loop  

                if current_gold == 0:
                    stop_button_location = locate_image_with_retries(stop_button, retries=1, confidence=0.8,region=stop_region,grayscale=True)
                    start_button_location = locate_image_with_retries(start_button, retries=1, confidence=0.8,region=start_region,grayscale=True)
                    back_button_location= locate_image_with_retries(back_button,retries=1,confidence=0.8,region=back_button_region,grayscale=True)
                    if stop_button_location:
                        logging.info("Stop button found, stopping cycle.")
                        detect_victory(victory)
                        click_direct(*stop_button_location)
                        time.sleep(np.random.uniform(0.2, 0.5))  # Delay for smoothness
                        break  # Exit inner loop and restart the game cycle
                    if start_button_location:
                        logging.info("Start button found after accidental click")
                        break  # Exit inner loop and restart the game cycle
                    if back_button_location:
                        logging.info("Back button found, stopping cycle.")
                        click_direct(*back_button_location)
                        time.sleep(np.random.uniform(0.2, 0.5))  # Delay for smoothness
                        break  # Exit inner loop and restart the game cycle
                
                if current_gold > 0 and not map_checked:
                    map_now = identify_map()  # Directly call identify_map
                    if map_now:
                        deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, enemy_detection_zones = perform_map_action(map_now)
                        current_map = map_now  # Store the map for later use
                        map_checked = True  # Prevent re-checking map
                        logging.info(f"Deployment zones for {map_now}: deploy_card={deploy_card}, deploy_dumbcombo={deploy_dumbcombo}")
                        
                    
                    else: 
                        logging.error(f"Failed to get deployment zones for {map_now}.")
                        break

                if current_gold > 0 and not match_started:
                    match_started = True  # Set the flag to True
                    logging.info("Match started! Now searching for cards and playing.")

                

                if match_started:
                    card_played = False  # Reset flag at the start of each cycle
                    detected_enemies = detect_enemy_units_in_realtime(mss_instance,game_window)
                    high_enemy_count = len(detected_enemies) >= 4 
                    card_deploy, combo_deploy, chest_deploy, miner_deploy,optional_aow_drop = process_enemy_positions(detected_enemies, enemy_detection_zones, deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, current_map)
                    if optional_aow_drop:
                        aow_drop = optional_aow_drop  # Unpack the AOW drop if it's present
                        logging.info(f"Special card priority is ON, AOW Drop is at {aow_drop}")
                    else:
                        logging.info("Special card priority is OFF, no AOW Drop.")

                    # **Combo Handling Logic (Highest Priority)**
                    combo_in_hand = find_multiple_cards(selected_combo_1)
                    if all(combo_in_hand):
                        if current_gold < combo_1_cost:
                            logging.info(f"Combo is ready but waiting for {combo_1_cost} gold. Current: {current_gold}")
                        else:
                            logging.info("Playing combo!")
                            x_min, x_max, y_min, y_max = combo_deploy
                            x_combo, y_combo = random.randint(x_min, x_max), random.randint(y_min, y_max)

                            for index, card in enumerate(combo_in_hand):
                                if card:
                                    if index == 1:
                                        x_combo += random.randint(-10, 10)
                                        y_combo += random.randint(-10, 10)

                                    play_card(card, x_combo, y_combo)
                                    time.sleep(np.random.uniform(0.1, 0.2))
                                else:
                                    logging.error("Failed to detect card for combo.")
                            card_played = True
                    #2nd highest priority
                    elif not all(combo_in_hand):

                            control_in_hand = find_multiple_cards(selected_combo_2) 
                            miner_in_hand = find_card(miner_card)
                            chest_in_hand = find_card(chest_card)  
                            not_upgradeable_in_hand = find_card(selected_not_upgradeable)
                            spell_or_unbound_in_hand=find_card(selected_spell_or_unbound)

                            if switch_to_spell_or_unbound_deploy_var.get() and high_enemy_count and spell_or_unbound_in_hand and not card_played:
                                if current_gold<spell_or_unbound_cost:
                                    logging.info("Waiting for gold to deploy spell or unbound")
                                else:
                                    detected_enemies = detect_enemy_units_in_realtime(mss_instance,game_window, threshold=0.8)
                                    spell_target = find_largest_enemy_cluster(detected_enemies)
                                    if spell_target:
                                        x_cluster, y_cluster = spell_target
                                        logging.info(f"Deploying Spell or Unbound at cluster ({x_cluster}, {y_cluster})")
                                        play_card(spell_or_unbound_in_hand, x_cluster, y_cluster)
                                        card_played = True


                            if all(control_in_hand) and not card_played:
                                if current_gold < combo_2_cost:
                                    logging.info(f"Combo is ready but waiting for {combo_2_cost} gold. Current: {current_gold}")
                                else:
                                    detected_enemies = detect_enemy_units_in_realtime(mss_instance,game_window)
                                    card_deploy, combo_deploy, chest_deploy, miner_deploy,optional_aow_drop = process_enemy_positions(detected_enemies, enemy_detection_zones, deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, current_map)  
                                    logging.info("Playing Control Units cards!")
                                    x_min, x_max, y_min, y_max = card_deploy
                                    x_card, y_card = random.randint(x_min, x_max), random.randint(y_min, y_max)
                                    card_played = True

                                    for index, card in enumerate(control_in_hand):
                                        if card:
                                            if index == 1:  
                                                x_card += random.randint(-10, 10)
                                                y_card += random.randint(-10, 10)

                                            play_card(card, x_card, y_card)
                                            time.sleep(np.random.uniform(0.1, 0.2))

                            elif chest_in_hand and not card_played and current_gold >= 1:
                                logging.info("Playing Chest card!")
                                x_min, x_max, y_min, y_max = chest_deploy
                                play_card(chest_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                card_played = True
                                
                            elif switch_special_card_priority_var.get() and not_upgradeable_in_hand and not card_played:
                                if current_gold<not_upgradeable_cost:
                                    logging.info("Waiting for gold to deploy defense")
                                else:
                                    logging.info("Prioritizing Not Upgradeable card due to high enemy count!")
                                    x_min, x_max, y_min, y_max = aow_drop
                                    x_card, y_card = random.randint(x_min, x_max), random.randint(y_min, y_max)
                                    logging.info(f"Deploying Not Upgradeable card at ({x_card}, {y_card})")
                                    play_card(not_upgradeable_in_hand, x_card, y_card)
                                    card_played = True
                            
                            elif high_enemy_count and not_upgradeable_in_hand and not switch_special_card_priority_var.get() and not card_played:
                                if current_gold<not_upgradeable_cost:
                                    logging.info("Waiting for gold to deploy defense")
                                else:
                                    logging.info("Prioritizing Not Upgradeable card due to high enemy count!")
                                    detected_enemies = detect_enemy_units_in_realtime(mss_instance,game_window)
                                    card_deploy, combo_deploy, chest_deploy, miner_deploy,optional_aow_drop = process_enemy_positions(detected_enemies, enemy_detection_zones, deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, current_map)
                                    x_min, x_max, y_min, y_max = card_deploy
                                    x_card, y_card = random.randint(x_min, x_max), random.randint(y_min, y_max)
                                    logging.info(f"Deploying Not Upgradeable card at ({x_card}, {y_card})")
                                    play_card(not_upgradeable_in_hand, x_card, y_card)
                                    card_played = True

                            elif miner_in_hand and not card_played and current_gold >= 1:
                                logging.info("Playing Miner card!")
                                x_min, x_max, y_min, y_max = miner_deploy
                                play_card(miner_in_hand, random.randint(x_min, x_max), random.randint(y_min, y_max))
                                card_played = True

                            # Final fallback: Only plays Not Upgradeable if no other cards were played
                            if not card_played and not switch_special_card_priority_var.get() and current_gold >= not_upgradeable_cost and not_upgradeable_in_hand:
                                logging.info("Playing Not Upgradeable card as last option!")
                                detected_enemies = detect_enemy_units_in_realtime(mss_instance,game_window)
                                card_deploy, combo_deploy, chest_deploy, miner_deploy,optional_aow_drop = process_enemy_positions(detected_enemies, enemy_detection_zones, deploy_card, deploy_dumbcombo, deploy_chest, deploy_miner, current_map)
                                x_min, x_max, y_min, y_max = card_deploy
                                x_card = random.randint(x_min, x_max)
                                y_card = random.randint(y_min, y_max)
                                logging.info(f"Deploying hero card at coordinates: ({x_card}, {y_card})")
                                play_card(not_upgradeable_in_hand, x_card, y_card)
                                card_played = True
                

                time.sleep(np.random.uniform(0.2, 0.4))  # Adjust sleep for smooth performance
            gc.collect()
            
def stop_bot():
    global executor
    with bot_restart_lock:  # Lock the restart process
        if not bot_running.is_set():
            logging.warning("Bot is not running.")
            return
        bot_running.clear()
        logging.info("Bot stopped.")
        if executor:
            executor.shutdown(wait=True)
            executor = None  # Reset executor for next start
        time.sleep(10)

def start_bot():
    global executor
    with bot_restart_lock:  # Lock the restart process
        if bot_running.is_set():
            logging.warning("Bot is already running.")
            return
        if executor is None or getattr(executor, "_shutdown", False):
            executor = ThreadPoolExecutor(max_workers=8)
        bot_running.set()
        logging.info("Bot started.")
        threading.Thread(target=main, daemon=True).start()

def save_default_xp_and_quests():
    defaults = {
        "max_quests": max_quests_var.get(),
        "rare_xp": blue_xp_var.get(),
        "epic_xp": purple_xp_var.get(),
        "exp_for_victory": exp_for_victory_var.get(),
        "max_xp_goal": max_xp_var.get()
    }
    with open(default_xp_file, "w") as f:
        json.dump(defaults, f)
    print("Default XP and quests saved to default_xp.json.")

def load_default_xp_and_quests():
    if os.path.exists(default_xp_file):
        with open(default_xp_file, "r") as f:
            defaults = json.load(f)
        max_quests_var.set(defaults.get("max_quests", "20"))
        blue_xp_var.set(defaults.get("rare_xp", "1080"))
        purple_xp_var.set(defaults.get("epic_xp", "1250"))
        exp_for_victory_var.set(defaults.get("exp_for_victory", "1080"))
        max_xp_var.set(defaults.get("max_xp_goal", "50000"))
        print("Loaded default XP and quests from default_xp.json.")

def save_current_setup():
    """Save the current setup with a custom name and store it in a JSON file."""
    setup_name = setup_name_var.get()
    if not setup_name:
        print("Please provide a name for the setup.")
        return

    new_setup = {
        "name": setup_name,
        "combo1_card1": combo1_card1_var.get(),
        "combo1_card2": combo1_card2_var.get(),
        "combo1_cost": combo1_cost_var.get(),
        "combo2_card1": combo2_card1_var.get(),
        "combo2_card2": combo2_card2_var.get(),
        "combo2_cost": combo2_cost_var.get(),
        "not_upgradeable_card": not_upgradeable_var.get(),
        "not_upgradeable_cost": not_upgradeable_cost_var.get(),
        "spell_or_unbound": spell_or_unbound_var.get(),
        "spell_or_unbound_cost": spell_or_unbound_cost_var.get(),
    }

    # Load existing setups from the file
    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            try:
                setups = json.load(f)  # Load the JSON data as a list
            except json.JSONDecodeError:
                setups = []  # If file is empty or corrupted, initialize an empty list
    else:
        setups = []

    # Ensure setups is a list before adding
    if not isinstance(setups, list):
        setups = []

    # Append the new setup to the list
    setups.append(new_setup)

    # Save the updated setups list back to the JSON file
    with open(setup_file, "w") as f:
        json.dump(setups, f, indent=4)

    print(f"Setup '{setup_name}' saved:", new_setup)

    # Reload the saved setups to update the dropdown
    load_saved_setups()

def load_saved_setups():
    """Loads all saved setups from the JSON file and updates the dropdown."""
    global setups  # Ensure we update the global list

    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            setups = json.load(f)

        # Get the list of setup names for the dropdown
        setup_names = [setup["name"] for setup in setups] if setups else ["No setups available"]

        # Update the StringVar and Combobox for the setup dropdown
        setup_list_var.set(setup_names[0] if setups else "No setups available")
        setup_dropdown["values"] = setup_names  # Update the dropdown values

        print("Loaded setups:", setups)
    else:
        print("No saved setups found.")
        setup_list_var.set("No setups available")
        setup_dropdown["values"] = ["No setups available"]  # Update with a single "No setups available" option

def delete_selected_setup():
    """Deletes the currently selected setup from the JSON file."""
    selected_name = setup_list_var.get()
    
    if not selected_name or selected_name == "No setups available":
        print("No valid setup selected for deletion.")
        return

    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            try:
                setups = json.load(f)
            except json.JSONDecodeError:
                print("Error loading setups. File might be corrupted.")
                return

        # Filter out the selected setup
        setups = [setup for setup in setups if setup["name"] != selected_name]

        # Save the updated list back to the JSON file
        with open(setup_file, "w") as f:
            json.dump(setups, f, indent=4)

        print(f"Setup '{selected_name}' deleted.")
        load_saved_setups()  # Refresh the dropdown

def load_selected_setup():
    """Loads the selected setup into the UI."""
    selected_name = setup_list_var.get()
    if selected_name and selected_name != "No setups available":
        # Find the setup based on the selected name
        selected_setup = next((setup for setup in setups if setup["name"] == selected_name), None)

        if selected_setup:
            # Set the UI fields to the selected setup values
            combo1_card1_var.set(selected_setup["combo1_card1"])
            combo1_card2_var.set(selected_setup["combo1_card2"])
            combo1_cost_var.set(selected_setup["combo1_cost"])
            combo2_card1_var.set(selected_setup["combo2_card1"])
            combo2_card2_var.set(selected_setup["combo2_card2"])
            combo2_cost_var.set(selected_setup["combo2_cost"])
            not_upgradeable_var.set(selected_setup["not_upgradeable_card"])
            not_upgradeable_cost_var.set(selected_setup["not_upgradeable_cost"])
            spell_or_unbound_var.set(selected_setup["spell_or_unbound"])
            spell_or_unbound_cost_var.set(selected_setup["spell_or_unbound_cost"])

            print(f"Loaded setup: {selected_setup}")

def create_ui():
    window = tk.Tk()
    window.title("Bot Control Panel")

    window.attributes("-topmost", True)

    # Create Notebook (Tabs)
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    # === Setup Name ===
    setup_frame = ttk.Frame(notebook)
    notebook.add(setup_frame, text="Setup")

    ttk.Label(setup_frame, text="Setup Name").grid(row=0, column=0, padx=4, pady=4)
    global setup_name_var
    setup_name_var = tk.StringVar()
    ttk.Entry(setup_frame, textvariable=setup_name_var).grid(row=0, column=1, padx=3, pady=3)

    # === Combo 1 Tab ===
    combo1_frame = ttk.Frame(notebook)
    notebook.add(combo1_frame, text="Combo 1")

    global combo1_card1_var, combo1_card2_var, combo1_cost_var
    ttk.Label(combo1_frame, text="Card 1").grid(row=0, column=0, padx=5, pady=5)
    combo1_card1_var = tk.StringVar(value="Swole Troll")
    ttk.Combobox(combo1_frame, textvariable=combo1_card1_var, values=list(available_cards.keys())).grid(row=0, column=1)

    ttk.Label(combo1_frame, text="Card 2").grid(row=1, column=0, padx=5, pady=5)
    combo1_card2_var = tk.StringVar(value="Dryad")
    ttk.Combobox(combo1_frame, textvariable=combo1_card2_var, values=list(available_cards.keys())).grid(row=1, column=1)

    ttk.Label(combo1_frame, text="Cost (1-10)").grid(row=2, column=0, padx=5, pady=5)
    combo1_cost_var = tk.StringVar(value=str(combo_1_cost))
    ttk.Entry(combo1_frame, textvariable=combo1_cost_var).grid(row=2, column=1)

    ttk.Button(combo1_frame, text="Update Combo 1", command=update_combo_1).grid(row=3, column=0, columnspan=2, pady=5)

    global switch_to_card_deploy_var
    switch_to_card_deploy_var = tk.BooleanVar()
    ttk.Checkbutton(combo1_frame, text="Switch to defend also with combo 1", variable=switch_to_card_deploy_var).grid(row=4, column=0, columnspan=2, pady=5)

    # === Combo 2 Tab ===
    combo2_frame = ttk.Frame(notebook)
    notebook.add(combo2_frame, text="Combo 2")

    global combo2_card1_var, combo2_card2_var, combo2_cost_var
    ttk.Label(combo2_frame, text="Card 1").grid(row=0, column=0, padx=5, pady=5)
    combo2_card1_var = tk.StringVar(value="Ghoul")
    ttk.Combobox(combo2_frame, textvariable=combo2_card1_var, values=list(available_cards.keys())).grid(row=0, column=1)

    ttk.Label(combo2_frame, text="Card 2").grid(row=1, column=0, padx=5, pady=5)
    combo2_card2_var = tk.StringVar(value="Witch Doctor")
    ttk.Combobox(combo2_frame, textvariable=combo2_card2_var, values=list(available_cards.keys())).grid(row=1, column=1)

    ttk.Label(combo2_frame, text="Cost (1-10)").grid(row=2, column=0, padx=5, pady=5)
    combo2_cost_var = tk.StringVar(value=str(combo_2_cost))
    ttk.Entry(combo2_frame, textvariable=combo2_cost_var).grid(row=2, column=1)

    ttk.Button(combo2_frame, text="Update Combo 2", command=update_combo_2).grid(row=3, column=0, columnspan=2, pady=5)

    # === Not Upgradeable Tab ===
    not_upgradeable_frame = ttk.Frame(notebook)
    notebook.add(not_upgradeable_frame, text="Not Upgradeable")

    global not_upgradeable_var, not_upgradeable_cost_var
    ttk.Label(not_upgradeable_frame, text="Select Not Upgradeable").grid(row=0, column=0, padx=5, pady=5)
    not_upgradeable_var = tk.StringVar(value="Sylvanas")
    ttk.Combobox(not_upgradeable_frame, textvariable=not_upgradeable_var, values=list(available_cards.keys())).grid(row=0, column=1)

    ttk.Label(not_upgradeable_frame, text="Cost (1-10)").grid(row=1, column=0, padx=5, pady=5)
    not_upgradeable_cost_var = tk.StringVar(value=str(not_upgradeable_cost))
    ttk.Entry(not_upgradeable_frame, textvariable=not_upgradeable_cost_var).grid(row=1, column=1)

    ttk.Button(not_upgradeable_frame, text="Update Not Upgradeable", command=update_not_upgradeable).grid(row=2, column=0, columnspan=2, pady=5)

    # Special Card Priority 
    global switch_special_card_priority_var
    switch_special_card_priority_var = tk.BooleanVar()
    ttk.Checkbutton(not_upgradeable_frame, text="Ancient of War", variable=switch_special_card_priority_var).grid(row=3, column=0, columnspan=2, pady=5)

    # === Spell or Unbound Tab ===
    spell_frame = ttk.Frame(notebook)
    notebook.add(spell_frame, text="Spell / Unbound")

    global switch_to_spell_or_unbound_deploy_var
    switch_to_spell_or_unbound_deploy_var = tk.BooleanVar()
    ttk.Checkbutton(spell_frame, text="Switch to use spell or unbound", variable=switch_to_spell_or_unbound_deploy_var).grid(row=0, column=0, columnspan=2, pady=5)

    global spell_or_unbound_var, spell_or_unbound_cost_var
    ttk.Label(spell_frame, text="Select Spell or Unbound").grid(row=1, column=0, padx=5, pady=5)
    spell_or_unbound_var = tk.StringVar(value="Blizzard")
    ttk.Combobox(spell_frame, textvariable=spell_or_unbound_var, values=list(spell_or_unbound.keys())).grid(row=1, column=1)

    ttk.Label(spell_frame, text="Cost (1-10)").grid(row=2, column=0, padx=5, pady=5)
    spell_or_unbound_cost_var = tk.StringVar(value=str(spell_or_unbound_cost))
    ttk.Entry(spell_frame, textvariable=spell_or_unbound_cost_var).grid(row=2, column=1)

    ttk.Button(spell_frame, text="Update Spell or Unbound", command=update_spell_or_unbound).grid(row=3, column=0, columnspan=2, pady=5)

    # === Total Exp ===
    global quest_count_var, max_quests_var, quest_label
    global blue_xp_var, purple_xp_var
    ttk.Label(setup_frame, text="Quests Completed:").grid(row=6, column=0, padx=5, pady=5)
    quest_count_var = tk.IntVar(value=0)  # Tracks completed quests
    quest_label = ttk.Label(setup_frame, text="0")
    quest_label.grid(row=6, column=1, padx=5, pady=5)

    # === Row 7 Compact Layout (Max Quests, Rare XP, Epic XP) ===
    row7_frame = ttk.Frame(setup_frame)
    row7_frame.grid(row=7, column=0, columnspan=6, sticky='w', padx=5, pady=2)

    # Max Quests
    ttk.Label(row7_frame, text="Max Quests:").pack(side="left", padx=(0, 2))
    max_quests_var = tk.StringVar(value="20")
    ttk.Entry(row7_frame, textvariable=max_quests_var, width=6).pack(side="left", padx=(0, 10))

    # Rare XP
    ttk.Label(row7_frame, text="Rare XP:").pack(side="left", padx=(0, 2))
    blue_xp_var = tk.StringVar(value="1080")
    ttk.Entry(row7_frame, textvariable=blue_xp_var, width=6).pack(side="left", padx=(0, 10))

    # Epic XP
    ttk.Label(row7_frame, text="Epic XP:").pack(side="left", padx=(0, 2))
    purple_xp_var = tk.StringVar(value="1250")
    ttk.Entry(row7_frame, textvariable=purple_xp_var, width=6).pack(side="left")

    global exp_for_victory_var
    ttk.Label(setup_frame, text="Enter Exp for victory").grid(row=9, column=0, padx=5, pady=5)
    exp_for_victory_var = tk.StringVar(value="1080")  # Default value for the multiplier
    ttk.Entry(setup_frame, textvariable=exp_for_victory_var).grid(row=9, column=1, padx=5, pady=5)
    
    global max_xp_var
    ttk.Label(setup_frame, text="Enter Max XP Goal").grid(row=10, column=0, padx=5, pady=5)
    max_xp_var = tk.StringVar(value="50000")  # Default total XP goal
    ttk.Entry(setup_frame, textvariable=max_xp_var).grid(row=10, column=1, padx=5, pady=5)

    global result_label
    result_label = ttk.Label(setup_frame, text="Remaining XP: 0")  # Update label text
    result_label.grid(row=12, column=0, columnspan=2, pady=5)
    # === Quest mode and archlight energy farm mode ===
    global archlight_energy_farm_var
    archlight_energy_farm_var = tk.BooleanVar()
    ttk.Checkbutton(setup_frame, text="Also green quest(Trigger also quest mode)", variable=archlight_energy_farm_var).grid(row=8, column=1, pady=5)

    global switch_quest_mode_var
    switch_quest_mode_var = tk.BooleanVar()
    ttk.Checkbutton(setup_frame, text="Quest mode(Rare and epic)", variable=switch_quest_mode_var).grid(row=8, column=0, pady=5)

    ttk.Button(setup_frame, text="Set Default XP & Quests", command=save_default_xp_and_quests).grid(row=1, column=1, padx=5, pady=5)

    # === Save & Load Setup ===
    ttk.Button(setup_frame, text="Save Setup", command=save_current_setup).grid(row=1, column=0, pady=5)

    global setup_list_var
    setup_list_var = tk.StringVar(value="No setups available")
    global setup_dropdown
    setup_dropdown = ttk.Combobox(setup_frame, textvariable=setup_list_var, values=["No setups available"])
    setup_dropdown.grid(row=2, column=0, columnspan=2, pady=5)

    ttk.Button(setup_frame, text="Load Selected Setup", command=load_selected_setup).grid(row=3, column=0, pady=5)
    ttk.Button(setup_frame, text="Delete Selected Setup", command=delete_selected_setup).grid(row=3, column=1, pady=5)

    # === Start/Stop Bot ===
    ttk.Button(setup_frame, text="Start Bot", command=start_bot).grid(row=5, column=0, pady=5)
    ttk.Button(setup_frame, text="Stop Bot", command=stop_bot).grid(row=5, column=1, pady=5)

    ttk.Button(window, text="Quit", command=window.quit).pack(pady=10)

    load_saved_setups()
    load_default_xp_and_quests()
    window.mainloop()

if __name__ == "__main__":
    create_ui()