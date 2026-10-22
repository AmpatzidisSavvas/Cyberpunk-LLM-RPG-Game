CLASSES_DATA = {
    "Netrunner": {
        "description": "A master of the digital sprawl, weaving through ICE and manipulating corporate mainframes.",
        "hp": 90,
        "max_hp": 90,
        "eddies": 400,
        "inventory": ["Cyberdeck v2", "ICE-Breaker", "Health Hypo"],
        "location": "Neo-Thessaloniki - Sub-Level 4 Terminal",
        "stats": {"HACKING": 5, "COMBAT": 1, "TECH": 2},
        "start_scenario": "net_start",
        "scenarios": {
            # --- STAGE 1: THE GRID ENTRY ---
            "net_start": {
                "illustration": "image_0.png",
                "narrative": "Neon code streams across your retinas as you jack into the grimy local grid near Ladadika. Crimson traces of Arasaka Black ICE flare up, threatening to fry your deck. Deep within the encrypted cluster lies a file titled 'PROJECT_OLYMPUS'.",
                "suggested_actions": ["Bypass the firewall", "Trace the attacker", "Dump cache and disconnect"],
                "new_location": "Neo-Thessaloniki - Deep Net Subgrid",
                "action_map": {
                    "Bypass the firewall": {
                        "stat": "HACKING", "dc": 12,
                        "success": "net_firewall_win",
                        "fail": "net_firewall_fail"
                    },
                    "Trace the attacker": {
                        "stat": "HACKING", "dc": 14,
                        "success": "net_trace_win",
                        "fail": "net_trace_fail"
                    },
                    "Dump cache and disconnect": "net_disconnect"
                }
            },
            
            # --- STAGE 2: BRANCH A (FIREWALL BYPASS) ---
            "net_firewall_win": {
                "narrative": "CRITICAL SUCCESS! Your ICE-Breaker tears through the Arasaka firewall. You breach the core data vault and discover 'PROJECT_OLYMPUS' contains military neural-parasite schematics.",
                "eddies_change": 250,
                "new_items": ["Project Olympus Schematics"],
                "suggested_actions": ["Infiltrate Executive Subnet", "Copy data and sell to Shadow Fixer"],
                "new_location": "Neo-Thessaloniki - Arasaka Core Vault",
                "action_map": {
                    "Infiltrate Executive Subnet": {
                        "stat": "HACKING", "dc": 16,
                        "success": "end_net_god",
                        "fail": "net_exec_trap"
                    },
                    "Copy data and sell to Shadow Fixer": "end_net_rich"
                }
            },
            "net_firewall_fail": {
                "narrative": "CHECK FAILED! Feedback code violently shunts back into your deck, searing your neural interface (-30 HP). Alarms blare across Sector 09, forcing you to seek physical shelter.",
                "hp_change": -30,
                "suggested_actions": ["Overclock cyberdeck to force entry", "Retreat to Sector 09 Safehouse"],
                "new_location": "Neo-Thessaloniki - Damaged Node",
                "action_map": {
                    "Overclock cyberdeck to force entry": {
                        "stat": "HACKING", "dc": 15,
                        "success": "net_firewall_win",
                        "fail": "end_flatline"
                    },
                    "Retreat to Sector 09 Safehouse": "net_disconnect"
                }
            },

            # --- STAGE 2: BRANCH B (ATTACKER TRACE) ---
            "net_trace_win": {
                "narrative": "CRITICAL SUCCESS! You counter-hack the Black ICE author, revealing an rogue NetWatch agent operating out of an abandoned server farm in Kalamaria.",
                "new_items": ["NetWatch Rogue Credentials"],
                "suggested_actions": ["Blackmail the Rogue Agent", "Expose NetWatch to the Public Grid"],
                "new_location": "Neo-Thessaloniki - NetWatch Rogue Hideout",
                "action_map": {
                    "Blackmail the Rogue Agent": "end_net_fixer",
                    "Expose NetWatch to the Public Grid": "end_net_hero"
                }
            },
            "net_trace_fail": {
                "narrative": "CHECK FAILED! The attacker was waiting for your trace! A NetWatch ping locks onto your physical cyberdeck location.",
                "hp_change": -20,
                "suggested_actions": ["Jack out immediately"],
                "action_map": {
                    "Jack out immediately": "end_net_captured"
                }
            },

            # --- COMMON & ENDING SCENARIOS ---
            "net_exec_trap": {
                "narrative": "FAIL! Arasaka's executive counter-daemons purge your cyberdeck storage and lock your neural buffer. You barely disconnect before brain death.",
                "hp_change": -40,
                "lost_items": ["Project Olympus Schematics"],
                "is_game_over": True
            },
            "net_disconnect": {
                "narrative": "Emergency jack-out executed. You purge memory buffers and return to physical reality empty-handed, but alive.",
                "is_game_over": True
            },
            "end_flatline": {
                "narrative": "CRITICAL SYSTEM FAILURE: High-voltage Black ICE fries your central nervous system. Your optic implants fade to black permanently.",
                "hp_change": -100,
                "is_game_over": True
            },
            "end_net_god": {
                "narrative": "MISSION COMPLETE: You commandeer Arasaka's executive subnet! You now control Neo-Thessaloniki's power grid from the shadows as the ultimate Net God.",
                "eddies_change": 10000,
                "is_game_over": True
            },
            "end_net_rich": {
                "narrative": "MISSION COMPLETE: The Shadow Fixer buys the schematics for a fortune. You wire 5,000 Eddies to your account and retire to an off-grid penthouse.",
                "eddies_change": 5000,
                "is_game_over": True
            },
            "end_net_hero": {
                "narrative": "MISSION COMPLETE: You broadcast NetWatch corruption across every holoscreen in the city. You become a folk hero in the digital underground.",
                "is_game_over": True
            },
            "end_net_fixer": {
                "narrative": "MISSION COMPLETE: The NetWatch rogue becomes your permanent informant. You now rule Neo-Thessaloniki's underground data broker network.",
                "eddies_change": 3000,
                "is_game_over": True
            },
            "end_net_captured": {
                "narrative": "MISSION COMPLETE (FAILED): A NetWatch strike team raids your location. You spend the rest of your life in a high-security cyber-prison.",
                "is_game_over": True
            }
        }
    },

    "Gunner": {
        "description": "A lethal combat specialist equipped with heavy firepower and elite tactical muscle.",
        "hp": 130,
        "max_hp": 130,
        "eddies": 250,
        "inventory": ["Smart-Pistol", "Combat Knife", "Armor Plating"],
        "location": "Neo-Thessaloniki - Sector 09 Combat Zone",
        "stats": {"HACKING": 1, "COMBAT": 5, "TECH": 2},
        "start_scenario": "solo_start",
        "scenarios": {
            # --- STAGE 1: ALLEY AMBUSH ---
            "solo_start": {
                "illustration": "image_1.png",
                "narrative": "A pair of cyber-enhanced scavs jump you from behind an overturned container in Sector 09, weapons hot. Out of the corner of your eye, you spot a high-tier Militech supply crate nearby.",
                "suggested_actions": ["Unload with Smart-Pistol", "Close in with Combat Knife", "Tactical slide to Militech Crate"],
                "new_location": "Neo-Thessaloniki - Alleyway Skirmish",
                "action_map": {
                    "Unload with Smart-Pistol": {
                        "stat": "COMBAT", "dc": 10,
                        "success": "solo_gun_win",
                        "fail": "solo_gun_fail"
                    },
                    "Close in with Combat Knife": {
                        "stat": "COMBAT", "dc": 14,
                        "success": "solo_knife_win",
                        "fail": "solo_knife_fail"
                    },
                    "Tactical slide to Militech Crate": {
                        "stat": "COMBAT", "dc": 12,
                        "success": "solo_crate_win",
                        "fail": "solo_crate_fail"
                    }
                }
            },

            # --- STAGE 2: BRANCH A (SMART PISTOL) ---
            "solo_gun_win": {
                "narrative": "TARGET ELIMINATED! Your smart-bullets home in and drop both scavs instantly. On one of their bodies, you find a encrypted bounty datapad listing a $2,000 hit on a local warlord.",
                "eddies_change": 300,
                "new_items": ["Bounty Datapad"],
                "suggested_actions": ["Hunt down the Scav Warlord", "Turn Datapad in to NCPD"],
                "new_location": "Neo-Thessaloniki - Sector 09 Hideout",
                "action_map": {
                    "Hunt down the Scav Warlord": {
                        "stat": "COMBAT", "dc": 15,
                        "success": "end_solo_warlord",
                        "fail": "end_solo_overwhelmed"
                    },
                    "Turn Datapad in to NCPD": "end_solo_bounty"
                }
            },
            "solo_gun_fail": {
                "narrative": "CHECK FAILED! A localized EMP jammer glitches your smart-pistol targeting. You take heavy crossfire (-40 HP) before diving into cover.",
                "hp_change": -40,
                "suggested_actions": ["Draw Combat Knife for final stand", "Retreat into the sewers"],
                "action_map": {
                    "Draw Combat Knife for final stand": {
                        "stat": "COMBAT", "dc": 13,
                        "success": "solo_knife_win",
                        "fail": "end_solo_overwhelmed"
                    },
                    "Retreat into the sewers": "end_solo_coward"
                }
            },

            # --- STAGE 2: BRANCH B (TACTICAL CRATE) ---
            "solo_crate_win": {
                "narrative": "TACTICAL SUCCESS! You slide past gunfire, breach the crate with your boot, and pull out a prototype Heavy Plasma Cannon!",
                "new_items": ["Prototype Plasma Cannon"],
                "suggested_actions": ["Annihilate the ambush squad", "Sell cannon to street gang"],
                "action_map": {
                    "Annihilate the ambush squad": "end_solo_merc_legend",
                    "Sell cannon to street gang": "end_solo_arms_dealer"
                }
            },
            "solo_crate_fail": {
                "narrative": "CHECK FAILED! The crate lock jams, leaving you pinned in the open. A shotgun blast shreds your Armor Plating (-50 HP).",
                "hp_change": -50,
                "lost_items": ["Armor Plating"],
                "suggested_actions": ["Retreat into the sewers"],
                "action_map": {
                    "Retreat into the sewers": "end_solo_coward"
                }
            },

            # --- STAGE 2: BRANCH C (COMBAT KNIFE) ---
            "solo_knife_win": {
                "narrative": "CRITICAL HIT! You close the distance, driving your knife straight into the leader's cybernetic neck joint before disarming his squadmate.",
                "eddies_change": 500,
                "new_items": ["Custom Cyberware Core"],
                "suggested_actions": ["Claim Scav Territory"],
                "action_map": {
                    "Claim Scav Territory": "end_solo_warlord"
                }
            },
            "solo_knife_fail": {
                "narrative": "CHECK FAILED! You miss your leap and take a point-blank shotgun blast to the chest.",
                "hp_change": -70,
                "is_game_over": True
            },

            # --- ENDINGS ---
            "end_solo_warlord": {
                "narrative": "MISSION COMPLETE: You storm the Scav stronghold, kill the warlord, and take control of Sector 09's mercenary underworld.",
                "eddies_change": 4000,
                "is_game_over": True
            },
            "end_solo_bounty": {
                "narrative": "MISSION COMPLETE: NCPD transfers $2,000 to your bank account. You buy top-tier ammo and prepare for the next contract.",
                "eddies_change": 2000,
                "is_game_over": True
            },
            "end_solo_merc_legend": {
                "narrative": "MISSION COMPLETE: You obliterate the scav squad with the plasma cannon. Your display of sheer force makes you an feared mercenary legend.",
                "is_game_over": True
            },
            "end_solo_arms_dealer": {
                "narrative": "MISSION COMPLETE: You fence the Militech Plasma Cannon for $6,000 Eddies on the black market and retire from street fighting.",
                "eddies_change": 6000,
                "is_game_over": True
            },
            "end_solo_overwhelmed": {
                "narrative": "MISSION COMPLETE (FAILED): Outnumbered and bleeding out, you are executed in the dark alleyway of Sector 09.",
                "is_game_over": True
            },
            "end_solo_coward": {
                "narrative": "MISSION COMPLETE: You crawl into the sewers, surviving the fight, but losing all your street reputation.",
                "is_game_over": True
            }
        }
    },

    "Techie": {
        "description": "A genius inventor and mechanic who builds custom tech, bypasses locks, and modifies gear.",
        "hp": 100,
        "max_hp": 100,
        "eddies": 300,
        "inventory": ["Toolkit", "Scrap Metal", "Welding Torch"],
        "location": "Neo-Thessaloniki - Under-City Workshop",
        "stats": {"HACKING": 2, "COMBAT": 1, "TECH": 5},
        "start_scenario": "tech_start",
        "scenarios": {
            # --- STAGE 1: WORKSHOP DISCOVERY ---
            "tech_start": {
                "illustration": "image_2.png",
                "narrative": "While stripping servo-motors from a discarded military drone in your workshop, your scanner picks up an active, rogue AI Core inside its casing. Suddenly, a local protection racket gang bangs on your workshop door!",
                "suggested_actions": ["Hotwire core into combat drone", "Rig door with scrap explosive", "Extract core and hide"],
                "new_location": "Neo-Thessaloniki - Under-City Workshop",
                "action_map": {
                    "Hotwire core into combat drone": {
                        "stat": "TECH", "dc": 11,
                        "success": "tech_drone_win",
                        "fail": "tech_drone_fail"
                    },
                    "Rig door with scrap explosive": {
                        "stat": "TECH", "dc": 13,
                        "success": "tech_trap_win",
                        "fail": "tech_trap_fail"
                    },
                    "Extract core and hide": {
                        "stat": "TECH", "dc": 14,
                        "success": "tech_extract_win",
                        "fail": "tech_extract_fail"
                    }
                }
            },

            # --- STAGE 2: BRANCH A (COMBAT DRONE) ---
            "tech_drone_win": {
                "narrative": "SUCCESS! The military drone boots up, hovering with twin autocannons active. It bursts through your door and drives the protection racket away!",
                "new_items": ["Combat Drone Companion"],
                "suggested_actions": ["Upgrade Drone into Mech Armor", "Deploy Drone to guard the street vendors"],
                "new_location": "Neo-Thessaloniki - Under-City Streets",
                "action_map": {
                    "Upgrade Drone into Mech Armor": {
                        "stat": "TECH", "dc": 15,
                        "success": "end_tech_titan",
                        "fail": "end_tech_overload"
                    },
                    "Deploy Drone to guard the street vendors": "end_tech_patron"
                }
            },
            "tech_drone_fail": {
                "narrative": "CHECK FAILED! The power capacitor overloads, scorching your hands (-25 HP) and destroying the drone circuit board.",
                "hp_change": -25,
                "suggested_actions": ["Rig door with scrap explosive"],
                "action_map": {
                    "Rig door with scrap explosive": {
                        "stat": "TECH", "dc": 13,
                        "success": "tech_trap_win",
                        "fail": "tech_trap_fail"
                    }
                }
            },

            # --- STAGE 2: BRANCH B (EXPLOSIVE TRAP) ---
            "tech_trap_win": {
                "narrative": "BOOM! The scrap explosive detonates as the gangers breach the door, disabling them instantly. In the wreckage, you find a high-grade Militech hydraulic power suit.",
                "eddies_change": 400,
                "new_items": ["Hydraulic Power Frame"],
                "suggested_actions": ["Sell frame on black market", "Build custom Exo-Suit"],
                "action_map": {
                    "Sell frame on black market": "end_tech_wealth",
                    "Build custom Exo-Suit": "end_tech_titan"
                }
            },
            "tech_trap_fail": {
                "narrative": "CHECK FAILED! The wire snaps prematurely! The gangers breach your workshop and loot your equipment.",
                "hp_change": -30,
                "lost_items": ["Toolkit"],
                "is_game_over": True
            },

            # --- STAGE 2: BRANCH C (EXTRACT CORE) ---
            "tech_extract_win": {
                "narrative": "CRITICAL EXTRACT! You carefully use your torch as a delicate scalpel, recovering an intact pristine AI core before slipping out the back door.",
                "new_items": ["Pristine AI Core"],
                "suggested_actions": ["Sell AI Core to bidder", "Build automated factory"],
                "action_map": {
                    "Sell AI Core to bidder": "end_tech_wealth",
                    "Build automated factory": "end_tech_factory"
                }
            },
            "tech_extract_fail": {
                "narrative": "CHECK FAILED! You puncture the AI core matrix, causing a localized shockwave that demolishes your workshop workbench.",
                "hp_change": -35,
                "is_game_over": True
            },

            # --- ENDINGS ---
            "end_tech_titan": {
                "narrative": "MISSION COMPLETE: You construct a piloted Cyber-Mech! You become the unstoppable guardian of Neo-Thessaloniki's Under-City.",
                "eddies_change": 2000,
                "is_game_over": True
            },
            "end_tech_patron": {
                "narrative": "MISSION COMPLETE: Your autonomous drones protect local markets. Grateful street vendors pool their funds to pay you a weekly salary.",
                "eddies_change": 3000,
                "is_game_over": True
            },
            "end_tech_wealth": {
                "narrative": "MISSION COMPLETE: High-tech black market bidders enter a price war for your loot. You net $7,000 Eddies and open a chain of tech clinics.",
                "eddies_change": 7000,
                "is_game_over": True
            },
            "end_tech_factory": {
                "narrative": "MISSION COMPLETE: You build an automated micro-factory that mass-produces cyberware, making you the top tech mogul in the city.",
                "eddies_change": 10000,
                "is_game_over": True
            },
            "end_tech_overload": {
                "narrative": "MISSION COMPLETE (FAILED): Overclocking the Mech armor triggers a catastrophic meltdown, destroying your workshop.",
                "hp_change": -100,
                "is_game_over": True
            }
        }
    }
}