import time, random, os, json

SAVE_FILE = "fashir_save.json"

def clear():
    os.system('clear' if os.name!= 'nt' else 'cls')

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# صور ASCII
ART = {
    "hero": r"""
    /|\
   / o \
   / | \
   / \ \
   """,
    "enemy1": r"""
    /==\
   ( >.<)
   / | \
   / \ \
   """,
    "enemy2": r"""
    [><]
   /====\
   | o |
   / \/ \
   """,
    "boss": r"""
    /####\
   ( X )
   / === \
   /||\ \
   """,

    # شوارع الفاشر - المرحلة 1
    "fashir_street": r"""
    | ___ ___
    | ___ | |
    |___| |___|
    | / \ / \
    |___| | / \ / \
    | / \/ \
    |_______|/ \
    ___ ___
    """,

    # مسجد السلطان علي دينار - المرحلة 2
    "mosque": r"""
        /\
       / \
      / \
     / /\ \
    / \ \
   /__/____\__\
    | |||| |
    | |||| |
   _|__||||__|_
  |_____________|
   | |
   |__|____|__|
   """,

    # بحيرة الفاشر - المرحلة 3
    "lake": r"""
    ~~~~~~~~~~~~ ~~~~~~~~~~~~
   ~~~~~ ~~~ ~~~~~~~
  ~~~ ~~
 ~~~ ~~
~~ ~~~~ ~~~ ~~~~ ~~~~ ~~
 ~ ~~~ ~~~ ~~~ ~~~ ~
  ~~ ~~~ ~~~ ~~~ ~
   ~~~~~~~~~~~~ ~~~~~~~~~~~~
    | Bridge | Road |
    ~~~~~~~~~~~~ ~~~~~~~~~~~~
    """
}

# الأسلحة والدروع - تم تصحيح القوس الناقص هنا
WEAPONS = {
    1: {"name": "سيف قديم", "atk": 5, "price": 0},
    2: {"name": "كلاش", "atk": 15, "price": 100},
    3: {"name": "RPG", "atk": 30, "price": 300}
ARMORS = {
    1: {"name": "قميص عادي", "def": 0, "price": 0},
    2: {"name": "درع خفيف", "def": 10, "price": 150},
    3: {"name": "درع ثقيل", "def": 25, "price": 400}
}

# المراحل مع صور الفاشر
STAGES = [
    {"name": "المرحلة 1: شوارع الفاشر", "location": "شارع الفاشر",
     "art": ART["fashir_street"], "art_enemy": ART["enemy1"],
     "enemy": {"name": "متمرد", "hp": 60, "atk": 12, "xp": 30, "gold": 50}},
    {"name": "المرحلة 2: مسجد السلطان علي دينار", "location": "مسجد السلطان علي دينار",
     "art": ART["mosque"], "art_enemy": ART["enemy2"],
     "enemy": {"name": "قائد ميداني", "hp": 90, "atk": 18, "xp": 60, "gold": 100}},
    {"name": "المرحلة 3: بحيرة الفاشر", "location": "بحيرة الفاشر",
     "art": ART["lake"], "art_enemy": ART["boss"],
     "enemy": {"name": "زعيم العدو", "hp": 150, "atk": 25, "xp": 120, "gold": 200}}
]

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None

def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)

def shop(player):
    while True:
        clear()
        print("="*40)
        print(" المتجر")
        print("="*40)
        print(f"قروشك: {player['gold']} جنيه")
        print("\n[1] أسلحة")
        for k, v in WEAPONS.items():
            print(f" {k}. {v['name']} - هجوم +{v['atk']} - {v['price']} جنيه")
        print("\n[2] دروع")
        for k, v in ARMORS.items():
            print(f" {k}. {v['name']} - دفاع +{v['def']} - {v['price']} جنيه")
        print("\n[0] رجوع")

        ch = input("اختار: ")
        if ch == "0": break
        if ch == "1":
            try:
                w = int(input("رقم السلاح: "))
                if w in WEAPONS and player["gold"] >= WEAPONS[w]["price"]:
                    player["gold"] -= WEAPONS[w]["price"]
                    player["weapon"] = WEAPONS[w]
                    slow_print(f"اشتريت {WEAPONS[w]['name']}!")
                    time.sleep(1)
            except: pass
        if ch == "2":
            try:
                a = int(input("رقم الدرع: "))
                if a in ARMORS and player["gold"] >= ARMORS[a]["price"]:
                    player["gold"] -= ARMORS[a]["price"]
                    player["armor"] = ARMORS[a]
                    slow_print(f"اشتريت {ARMORS[a]['name']}!")
                    time.sleep(1)
            except: pass

def level_up(player):
    while player["xp"] >= player["xp_needed"]:
        player["xp"] -= player["xp_needed"]
        player["lvl"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["atk"] += 5
        player["xp_needed"] = int(player["xp_needed"] * 1.5)
        slow_print(f"\n🎉 مبروك! وصلت مستوى {player['lvl']}!")
        time.sleep(1)

def fight(player, stage):
    enemy = stage["enemy"].copy()
    clear()
    print(f"\nالموقع: {stage['location']}")
    print(stage["art"])
    print(stage["art_enemy"])
    slow_print(f"\n⚔️ ظهر {enemy['name']}! HP: {enemy['hp']}")
    time.sleep(1)

    while player["hp"] > 0 and enemy["hp"] > 0:
        total_atk = player["atk"] + player["weapon"]["atk"]
        total_def = player["armor"]["def"]

        print(f"\n{player['name']} | Lv {player['lvl']} | HP {player['hp']}/{player['max_hp']} | XP {player['xp']}/{player['xp_needed']}")
        print(f"{enemy['name']} | HP {enemy['hp']}")
        print("\n1. هجوم")
        print("2. دفاع +10 HP")
        print("3. هروب")
        choice = input("اختار: ")

        if choice == "1":
            dmg = max(1, random.randint(total_atk-5, total_atk+5) - enemy.get("def", 0))
            enemy["hp"] -= dmg
            slow_print(f"ضربت {enemy['name']} بـ {dmg} ضرر!")
            time.sleep(0.5)
        elif choice == "2":
            heal = 10
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            slow_print(f"تحصنت واستعدت {heal} HP!")
            time.sleep(0.5)
        elif choice == "3":
            slow_print("هربت من المعركة!")
            return False

        if enemy["hp"] <= 0:
            slow_print(f"\n✅ هزمت {enemy['name']}!")
            player["xp"] += enemy["xp"]
            player["gold"] += enemy["gold"]
            player["hp"] = min(player["max_hp"], player["hp"] + 20)
            slow_print(f"+{enemy['xp']} XP | +{enemy['gold']} جنيه")
            level_up(player)
            time.sleep(1.5)
            return True

        e_dmg = max(1, random.randint(enemy["atk"]-5, enemy["atk"]+5) - total_def)
        player["hp"] -= e_dmg
        slow_print(f"{enemy['name']} ضربك بـ {e_dmg} ضرر!")
        time.sleep(0.5)

        if player["hp"] <= 0:
            slow_print("\n💀 لقد مت... المهمة فشلت!")
            time.sleep(2)
            return False

    return True

def main():
    clear()
    print("="*45)
    print(" 🔥 لعبة الفاشر: معركة الكرامة 🔥")
    print("="*45)
    print(" المطور: محمد إبراهيم")
    print("="*45)
    print("\n1. لعبة جديدة")
    print("2. تحميل اللعبة")
    choice = input("اختار: ")

    if choice == "2":
        saved = load_game()
        if saved:
            player = saved
            slow_print("تم تحميل اللعبة!")
        else:
            slow_print("ما لقيت ملف حفظ!")
            time.sleep(1)
            return main()
    else:
        name = input("\nادخل اسم البطل: ")
        player = {
            "name": name, "hp": 100, "max_hp": 100, "atk": 20,
            "lvl": 1, "xp": 0, "xp_needed": 100, "gold": 50,
            "weapon": WEAPONS[1], "armor": ARMORS[1],
            "stage": 0
        }

    clear()
    slow_print(f"\n{ART['hero']}")
    slow_print(f"القصة: {player['name']}، الفاشر تناديك. حرر المدينة!")
    time.sleep(1)

    for i in range(player["stage"], len(STAGES)):
        stage = STAGES[i]
        clear()
        print(f"\n{'='*40}")
        slow_print(stage["name"])
        print(f"{'='*40}")
        print("1. قاتل")
        print("2. المتجر")
        print("3. حفظ وخروج")
        ch = input("اختار: ")

        if ch == "2":
            shop(player)
            continue
        if ch == "3":
            save_game(player)
            slow_print("تم الحفظ!")
            return

        if fight(player, stage):
            player["stage"] += 1
        else:
            return

        if player["stage"] >= len(STAGES):
            clear()
            print("\n" + "="*45)
            slow_print("🏆 مبروك! حررت الفاشر وانتصرت!")
            slow_print(f"النهاية - {player['name']} بطل المدينة")
            print("="*45)
            print("\nالمطور: محمد إبراهيم © 2026")
            return

    print("\nشكراً للعب!")
    print("المطور: محمد إبراهيم © 2026")

if __name__ == "__main__":
    main()
