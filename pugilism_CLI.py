from pugilism import *
import time

# example fighters Andy and Bob.
p1 = pugilists[0]
p2 = pugilists[1]

# Gameplay
print("Ready to fight?")
print("Each fighter will have a given Composure. Composure is lost by being hit, or by using certain moves.")

# Initiative roll
## IMPERFECT ROLLING LOGIC, YES.
if (random.randint(1, 20) + getModifier(p1.dexterity)) > random.randint(1, 20)+getModifier(p2.dexterity):
    pair = [p1, p2]
else:
    pair = [p2, p1]

def round(lead, follow):
    lead.ready()
    follow.ready()
    print(f"{lead}'s composure will be {lead.composure}, and {follow}'s composure will be {follow.composure}.")    
    time.sleep(1)
    print(f"{lead} will attack first this round.")
    time.sleep(1)
    while True:
        print(f"{lead}. These are your attack options:")

        for i, attack in enumerate(attacks_core):
            print(f"{i+1}) {attack['name']}: fatigue {attack['fatigue']}, power {attack['POW']}")

        lead_ATK1 = attacks_core[int(input("Choose your first attack: "))-1]
        lead_ATK2 = attacks_core[int(input("Choose your second attack: "))-1]
        time.sleep(1)

        print("These are your defense options:")

        for i, defense in enumerate(defenses_core):
            print(f"{i+1}) {defense['name']}: fatigue {defense['fatigue']}, {defense['description']}")


        lead_DEF = defenses_core[int(input(f"Choose your defense: "))-1]
        time.sleep(2)

        print(f"{follow}. These are your attack options:")
        for i, attack in enumerate(attacks_core):
            print(f"{i+1}) {attack['name']}: fatigue {attack['fatigue']}, power {attack['POW']}")

        follow_ATK1 = attacks_core[int(input("Choose your first attack: "))-1]
        follow_ATK2 = attacks_core[int(input("Choose your second one:"))-1]

        print("These are your defense options: ")
        for i, defense in enumerate(defenses_core):
            print(f"{i+1}) {defense['name']}: fatigue {defense['fatigue']}, {defense['description']}")

        follow_DEF = defenses_core[int(input("Choose your defense: "))-1]

        match follow_DEF.get("name"):
            case "Body Protect":
                lead.tire(lead_ATK1.get("fatigue"))
                print(f"{follow} protects his body...")      
                if lead_ATK1.get("target")=="B":
                    lead.tire(lead_ATK2.get("fatigue"))
                    print(f"and blocks {lead}'s {lead_ATK1.get("name")}.")
                    if lead_ATK2.get("target")=="B":
                        print(f"And their {lead_ATK2.get("name")} as well! What a wall.")
                    else:
                        print(f"But {lead}'s {lead_ATK1.get("name")} hits.")
                        follow.suffer(lead_ATK2.get("POW"))
                        if follow.composure>0:
                            print("Our fighters still stand!")
                        else:
                            print(f"{follow} is KO!")
                            break        
                elif lead_ATK2.get("target")=="B":
                    print(f"But the first attack hits them!")
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        print(f"{follow} is still standing, and he covers himself, blocking the second attack!")
                    else:
                        print(f"{follow} is KO!")
                        break
                else:
                    print(f"But {lead}'s first attack hits {follow} like a truck!")
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        follow.suffer(lead_ATK2.get("POW"))
                        print(f"{follow} is still standing! But here comes the second one... Pow!")                    
                    else:
                        print(f"{follow} is KO!")
                        break
                if follow.composure>0:
                    print(f"{follow} is holding out like a champ, but we will see you again after these messages.")
                else:
                    print(f"{follow} is KO!")
                    break

            case "Head Protect":
                lead.tire(lead_ATK1.get("fatigue"))
                print(f"{follow} covers covers their head...")
                if lead_ATK1.get("target")=="H":
                    lead.tire(lead_ATK2.get("fatigue"))
                    if lead_ATK2.get("target")=="H":
                        print(f"BLOCKED BOTH!")
                    else:
                        print(f"AND BLOCKS THE FIRST ATTACK! BUT THE SECOND ONE HITS WITH {lead_ATK2.get("POW")} POW.")
                        follow.suffer(lead_ATK2.get("POW"))
                        if follow.composure>0:
                            print("This is the end of this round!")
                        else:
                            print(f"{follow} is KO!")
                            break

                elif lead_ATK2.get("target")=="H":
                    print(f"THE FIRST ATTACK HITS!")
                    follow.suffer(lead_ATK1.get("POW"))

                    if follow.composure>0:
                        print(f"STILL STANDING, {follow} BLOCKS THE INCOMING FOLLOW UP!")
                        lead.tire(lead_ATK2.get("fatigue"))
                    else:            
                        print(f"{follow} is KO!")
                        break
                else:
                    print(f"{lead}'s FIRST ATTACK HITS LIKE A {lead_ATK1.get("POW")}-POW TRUCK!")
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        follow.suffer(lead_ATK2.get("POW"))
                        print("HE'S STILL STANDING! BUT HERE COMES ANOTHER ONE... POW!")
                    else:
                        print(f"{follow} is KO!")
                        break 
                if follow.composure>0:
                    print(f"{follow} is holding out like a champ, but we will see you again after these messages.")
                else:
                    print(f"{follow} is KO!")
                    break

            case "General Defense":
                lead.tire(lead_ATK1.get("fatigue"))

                # Two jabs, NO DAMAGE
                if (lead_ATK1.get("type")==lead_ATK2.get("type") and lead_ATK1.get("type")=="J"):
                    lead.tire(lead_ATK2.get("fatigue"))
                    print(f"Both jabs are blocked!")              

                # Two HEAVYS, FULL DAMAGE 
                elif (lead_ATK1.get("type")==lead_ATK2.get("type") and lead_ATK1.get("type")=="H"):
                    print(f"a heavy hit overpowers {follow} for {lead_ATK1.get("POW")} damage.")
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        print(f"and another one! this time, for {lead_ATK2.get("POW")}")
                        follow.suffer(lead_ATK2.get("POW"))
                        lead.tire(lead_ATK2.get("fatigue"))
                    else:
                        print(f"{follow} is KO!")
                        break    
                # One heavy
                elif lead_ATK1.get("type")=="H":
                        print("heavy hit")
                        follow.suffer(lead_ATK1.get("POW"))
                        if follow.composure>0:
                            lead.tire(lead_ATK2.get("fatigue"))
                            print("But he's still up and blocks the second one!")
                        else:
                            print(f"{follow} is KO!")
                            break
                elif lead_ATK2.get("type")=="H":
                        lead.tire(lead_ATK2.get("fatigue"))
                        follow.suffer(lead_ATK2.get("POW"))
                        print(f"{follow} blocks the first attack, but {lead} retaliates with a heavy blow! He connects.")
                        
                # Two strikes, OR a strike and a jab
                else:
                    if lead_ATK1.get("POW")>=lead_ATK2.get("POW") or follow.composure<lead_ATK1.get("POW"): # if the first one is harder or not survivable.
                        print(f"{follow} blocks the first attack, but the second one hits!")
                        follow.suffer(lead_ATK2.get("POW"))
                        lead.tire(lead_ATK2.get("fatigue"))
                        if follow.composure>0:
                            print(f"Despite that, {follow} is still up! We'll see what happens next round.")
                        else:
                            print(f"{follow} is KO!")
                            break
                    else:
                            follow.suffer(lead_ATK1.get("POW"))
                            print(f"{follow} gets hit!")

                            lead.tire(lead_ATK2.get("fatigue"))
                            if follow.composure>0:
                                lead.tire(lead_ATK2.get("fatigue"))
                                print("But he's still up, and he blocks the follow-up.")
                            else:
                                print(f"{follow} is KO!")
                                break
                    
            case "Duck & Weave":
                lead.tire(lead_ATK1.get("fatigue"))
                if lead_ATK1.get("target")!=lead_ATK2.get("target"):
                    lead.tire(lead_ATK2.get("fatigue"))
                    follow.tire(follow_DEF.get("fatigue"))
                    print(f"Oh! {follow} Ducks and Weaves through both attacks, evading both!")
                else:
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        follow.suffer(lead_ATK2.get("POW"))
                        lead.tire(lead_ATK2.get("fatigue"))
                        print(f"{follow} is hit twice!")
                        if follow.composure>0:
                            follow.tire(follow_DEF.get("fatigue"))
                            print(f"but {follow} is still up.")
                        else:
                            print(f"{follow} is KO!")
                            break
                    else:
                        print(f"{follow} is KO!")
                        break

            case "Counter":
                lead.tire(lead_ATK1.get("fatigue"))
                
                # 2 Heavy attacks:
                if (lead_ATK1.get("type")=="H" and lead_ATK2.get("type")=="H"):
                    if (lead_ATK1.get("POW")>follow.composure) | (lead_ATK1.get("POW") > lead_ATK2.get("POW")): # si el primero es letal, o peor.
                        lead.suffer(math.floor(lead_ATK1.get("POW")/2))
                        if lead.composure>0:
                            lead.tire(lead_ATK2.get("fatigue"))
                            follow.suffer(lead_ATK2.get("POW"))
                            if follow.composure>0:
                                print(f"{follow} is still standing!")
                            else:
                                print(f"{lead} is KO")
                                break
                        else:
                            print(f"{follow} has struck back and {lead} is DOWN!")
                    else:
                        lead.tire(lead_ATK2.get("fatigue"))
                        lead.suffer(math.floor(lead_ATK2.get("POW")/2))
                        
                # heavy solo el primero;
                elif lead_ATK1.get("type")=="H":
                    lead.tire(lead_ATK2.get("fatigue"))
                    lead.suffer(math.floor(lead_ATK1.get("POW")/2))
                    if lead.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        follow.suffer(lead_ATK2.get("POW"))
                        print(f"Still standing, {lead} goes for another one and connects!")
                        if follow.composure>0:
                            print("still standing!")
                        else:
                           print(f"{lead} is KO!")
                           break
                    else: 
                        print(f"{lead} is KO!")
                        break
                # heavy solo el Segundo;
                elif lead_ATK2.get("type")=="H":
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        lead.suffer(math.floor(lead_ATK2.get("POW")/2))
                        if lead.composure>0:
                            print("They are both still standing!")
                        else:
                            print(f"{lead} is KO!")
                            break
                    else:
                        print(f"{follow} is KO!")
                        break
                # Si ninguno es Heavy, o sea, si ninguno va a ser countereado:
                else:
                    follow.suffer(lead_ATK1.get("POW"))
                    if follow.composure>0:
                        lead.tire(lead_ATK2.get("fatigue"))
                        follow.suffer(lead_ATK2.get("POW"))
                        if follow.composure>0:
                            print(f"{follow} is still standing!")
                        else:
                            print(f"{follow} is KO!")
                            break
                    else:
                        print(f"{follow} is KO!")                        
                        break
        
        match lead_DEF.get("name"):
                    case "Body Protect":
                        follow.tire(follow_ATK1.get("fatigue"))
                        print(f"{lead} blocked...")
                        if follow_ATK1.get("target")=="B":
                            follow.tire(follow_ATK2.get("fatigue"))
                            if follow_ATK2.get("target")=="B":
                                print(f"Both attacks, like a wall! {lead} takes no damage.")
                            else:
                                print(f"and deflects one attack, but another hits their head")
                                lead.suffer(follow_ATK2.get("POW"))
                                if lead.composure>0:
                                    print("And they are both still standing!")
                                else:
                                    print(f"{lead} is KO!")
                                            
                        elif follow_ATK2.get("target")=="B":
                            print(f"But the first attack hits them!")
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                print(f"{lead} is still standing, and he covers himself, blocking the second attack!")
                            else:
                                print(f"{lead} is KO!")
                                
                        else:
                            print(f"But {follow}'s first attack hits {lead} like a truck!")
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                lead.suffer(follow_ATK2.get("POW"))
                                print(f"{lead} is still standing! But here comes the second one... Pow!")                    
                            else:
                                print(f"{lead} is KO!")
                        if lead.composure>0:
                            print(f"{lead} is holding out like a champ, but we will see you again after these messages.")
                        else:
                            print(f"{lead} is KO!")

                    case "Head Protect":
                        follow.tire(follow_ATK1.get("fatigue"))
                        print(f"{lead} covers covers their head...")
                        if follow_ATK1.get("target")=="H":
                            follow.tire(follow_ATK2.get("fatigue"))
                            if follow_ATK2.get("target")=="H":
                                print(f"BLOCKED BOTH!")
                            else:
                                print(f"AND BLOCKS THE FIRST ATTACK! BUT THE SECOND ONE HITS WITH {follow_ATK2.get("POW")} POW.")
                                lead.suffer(follow_ATK2.get("POW"))
                                if lead.composure>0:
                                    print("This is the end of this round!")
                                else:
                                    print(f"{lead} is KO!")

                        elif follow_ATK2.get("target")=="H":
                            print(f"THE FIRST ATTACK HITS!")
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                print(f"Still standing, {lead} blocks the incoming follow up!")
                                follow.tire(follow_ATK2.get("fatigue"))
                            else:            
                                print(f"{lead} is KO!")
                        else:
                            print(f"{follow}'s FIRST ATTACK HITS LIKE A {follow_ATK1.get("POW")}-POW TRUCK!")
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                lead.suffer(follow_ATK2.get("POW"))
                                print("HE'S STILL STANDING! BUT HERE COMES ANOTHER ONE... POW!")
                            else:
                                print(f"{lead} is KO!")
                        if lead.composure>0:
                            print(f"{lead} is holding out like a champ, but we will see you again after these messages.")
                        else:
                            print(f"{lead} is KO!")
                            
                    case "General Defense":
                        follow.tire(follow_ATK1.get("fatigue"))

                        # Two jabs, NO DAMAGE
                        if (follow_ATK1.get("type")==follow_ATK2.get("type") and follow_ATK1.get("type")=="J"):
                            follow.tire(follow_ATK2.get("fatigue"))
                            print(f"Both jabs are blocked!")              

                        # Two HEAVYS, FULL DAMAGE 
                        elif (follow_ATK1.get("type")==follow_ATK2.get("type") and follow_ATK1.get("type")=="H"):
                            print(f"a heavy hit overpowers {lead} for {follow_ATK1.get("POW")} damage.")
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                print(f"and another one! this time, for {follow_ATK2.get("POW")}")
                                lead.suffer(follow_ATK2.get("POW"))
                                follow.tire(follow_ATK2.get("fatigue"))
                            else:
                                print(f"{lead} is KO!")

                                    
                        # One heavy
                        elif follow_ATK1.get("type")=="H":
                                print("heavy hit")
                                lead.suffer(follow_ATK1.get("POW"))
                                if lead.composure>0:
                                    follow.tire(follow_ATK2.get("fatigue"))
                                    print("But he's still up and blocks the second one!")
                                else:
                                    print(f"{lead} is KO!")
                                    
                        elif follow_ATK2.get("type")=="H":
                                follow.tire(follow_ATK2.get("fatigue"))
                                lead.suffer(follow_ATK2.get("POW"))
                                print(f"{lead} blocks the first attack, but {follow} retaliates with a heavy blow! He connects.")
                                
                        # Two strikes, OR a strike and a jab
                        else:
                            if follow_ATK1.get("POW")>=follow_ATK2.get("POW") or lead.composure<follow_ATK1.get("POW"): # if the first one is harder or not survivable.
                                print(f"{lead} blocks the first attack, but the second one hits!")
                                lead.suffer(follow_ATK2.get("POW"))
                                follow.tire(follow_ATK2.get("fatigue"))
                                if lead.composure>0:
                                    print(f"Despite that, {lead} is still up! We'll see what happens next round.")
                                else:
                                    print(f"{lead} is KO!")
                            else:
                                    lead.suffer(follow_ATK1.get("POW"))
                                    print(f"{lead} gets hit!")

                                    follow.tire(follow_ATK2.get("fatigue"))
                                    if lead.composure>0:
                                        follow.tire(follow_ATK2.get("fatigue"))
                                        print("But he's still up, and he blocks the lead-up.")
                                    else:
                                        print(f"{lead} is KO!")
                                        
                    case "Duck & Weave":
                        follow.tire(follow_ATK1.get("fatigue"))
                        if follow_ATK1.get("target")!=follow_ATK2.get("target"):
                            follow.tire(follow_ATK2.get("fatigue"))
                            lead.tire(lead_DEF.get("fatigue"))
                            print(f"Oh! {lead} Ducks and Weaves through both attacks, evading both!")
                        else:
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                lead.suffer(follow_ATK2.get("POW"))
                                follow.tire(follow_ATK2.get("fatigue"))
                                print(f"{lead} is hit twice!")
                                if lead.composure>0:
                                    print(f"but {lead} is still up.")
                                    lead.tire(lead_DEF.get("fatigue"))
                                else:
                                    print(f"{lead} is KO!")
                            else:
                                print(f"{lead} is KO!")
                                
                    case "Counter":
                        follow.tire(follow_ATK1.get("fatigue"))
                        
                        # 2 Heavy attacks:
                        if (follow_ATK1.get("type")=="H" and follow_ATK2.get("type")=="H"):
                            if (follow_ATK1.get("POW")>lead.composure) | (follow_ATK1.get("POW") > follow_ATK2.get("POW")): # si el primero es letal, o peor.
                                follow.suffer(math.floor(follow_ATK1.get("POW")/2))
                                if follow.composure>0:
                                    follow.tire(follow_ATK2.get("fatigue"))
                                    lead.suffer(follow_ATK2.get("POW"))
                                    if lead.composure>0:
                                        print(f"{lead} is still standing!")
                                    else:
                                        print(f"{follow} is KO")
                                        
                                else:
                                    print(f"{lead} has struck back and {follow} is DOWN!")
                            else:
                                follow.tire(follow_ATK2.get("fatigue"))
                                follow.suffer(math.floor(follow_ATK2.get("POW")/2))
                                
                        # heavy solo el primero;
                        elif follow_ATK1.get("type")=="H":
                            follow.tire(follow_ATK2.get("fatigue"))
                            follow.suffer(math.floor(follow_ATK1.get("POW")/2))
                            if follow.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                lead.suffer(follow_ATK2.get("POW"))
                                print(f"Still standing, {follow} goes for another one and connects!")
                                if lead.composure>0:
                                    print("still standing!")
                                else:
                                    print(f"{follow} is KO!")
                            else: 
                                print(f"{follow} is KO!")
                                
                        # heavy solo el Segundo;
                        elif follow_ATK2.get("type")=="H":
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                follow.suffer(math.floor(follow_ATK2.get("POW")/2))
                                if follow.composure>0:
                                    print("They are both still standing!")
                                else:
                                    print(f"{follow} is KO!")
                            else:
                                print(f"{lead} is KO!")
                                
                        # Si ninguno es Heavy, o sea, si ninguno va a ser countereado:
                        else:
                            lead.suffer(follow_ATK1.get("POW"))
                            if lead.composure>0:
                                follow.tire(follow_ATK2.get("fatigue"))
                                lead.suffer(follow_ATK2.get("POW"))
                                if lead.composure>0:
                                    print(f"{lead} is still standing!")
                                else:
                                    print(f"{lead} is KO!")
                            else: 
                                print(f"{lead} is KO!")

        print(f"Currently {lead} has {lead.composure} composure,")
        print(f"and {follow} has {follow.composure} composure.")
    
    if lead.composure>follow.composure:
        return lead
    else:
        return follow

print("THIS IS WHERE ROUND 1 STARTS")

print(f"{round(pair[0], pair[1]).name} wins the first round!")    

print("THIS IS WHERE ROUND 2 STARTS")
print(f"{round(pair[1], pair[0])} wins the second round!")

if p1.winded:
    if p1.winded and p2.winded:
        print(f"{print(f"{round(pair[0], pair[1])}").name} wins the match!")
    else:
        print(f"{p2.name} wins the match!")
else:
    print(f"{p1.name} wins the match!")