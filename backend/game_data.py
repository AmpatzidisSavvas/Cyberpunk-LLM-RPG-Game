CLASSES_DATA = {
    "Netrunner": {
        "description": "A master of the digital sprawl, weaving through ICE and manipulating corporate mainframes.",
        "hp": 90,
        "max_hp": 90,
        "eddies": 400,
        "inventory": ["Cyberdeck v2", "ICE-Breaker", "Health Hypo"],
        "location": "Thessaloniki - Ladadika Sub-Level 4 Terminal",
        "stats": {"HACKING": 5, "COMBAT": 1, "TECH": 2},
        "start_scenario": "net_start",
        "scenarios": {
            # --- STAGE 1: THE GRID ENTRY (LADADIKA SUB-LEVEL 4) ---
            "net_start": {
                "illustration": "class-3.png",
                "narrative": "Neon code streams across your retinas as you jack into the grimy local grid hidden underneath the historic Ladadika quarter. Crimson traces of Arasaka Black ICE flare up, threatening to fry your deck. Deep within the encrypted cluster lies a file titled 'PROJECT_OLYMPUS', routed straight from the OTE Spire relay.",
                "suggested_actions": ["Bypass the firewall", "Trace the attacker", "Dump cache and disconnect"],
                "new_location": "Thessaloniki - Deep Net Subgrid",
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
                "narrative": "CRITICAL SUCCESS! Your ICE-Breaker tears through the Arasaka firewall. You breach the core vault housed inside the ancient Rotunda Data Sanctuary and discover 'PROJECT_OLYMPUS' contains military neural-parasite schematics.",
                "eddies_change": 250,
                "new_items": ["Project Olympus Schematics"],
                "suggested_actions": ["Infiltrate Executive Subnet at Aristotelous Plaza", "Route data to White Tower Array", "Copy data and sell to Shadow Fixer"],
                "new_location": "Thessaloniki - Rotunda Data Vault",
                "action_map": {
                    "Infiltrate Executive Subnet at Aristotelous Plaza": {
                        "stat": "HACKING", "dc": 16,
                        "success": "end_net_god",
                        "fail": "net_exec_trap"
                    },
                    "Route data to White Tower Array": {
                        "stat": "HACKING", "dc": 13,
                        "success": "net_citadel_broadcast",
                        "fail": "net_citadel_fail"
                    },
                    "Copy data and sell to Shadow Fixer": "end_net_rich"
                }
            },
            "net_firewall_fail": {
                "narrative": "CHECK FAILED! Feedback code violently shunts back into your deck, searing your neural interface (-30 HP). Alarms blare across the Kamara Cyber-Arch area, forcing you to seek physical shelter.",
                "hp_change": -30,
                "suggested_actions": ["Overclock cyberdeck to force entry", "Retreat to Kamara Underdeck Safehouse"],
                "new_location": "Thessaloniki - Kamara Damaged Node",
                "action_map": {
                    "Overclock cyberdeck to force entry": {
                        "stat": "HACKING", "dc": 15,
                        "success": "net_firewall_win",
                        "fail": "end_flatline"
                    },
                    "Retreat to Kamara Underdeck Safehouse": "net_disconnect"
                }
            },

            # --- STAGE 2: BRANCH B (ATTACKER TRACE) ---
            "net_trace_win": {
                "narrative": "CRITICAL SUCCESS! You counter-hack the Black ICE author, revealing a rogue NetWatch agent operating out of the abandoned transmitter sub-levels of the OTE Tower.",
                "new_items": ["NetWatch Rogue Credentials"],
                "suggested_actions": ["Blackmail the Rogue Agent", "Expose NetWatch to the Public Grid", "Hijack OTE Transmitter Beam"],
                "new_location": "Thessaloniki - OTE Tower Relay Station",
                "action_map": {
                    "Blackmail the Rogue Agent": "end_net_fixer",
                    "Expose NetWatch to the Public Grid": "end_net_hero",
                    "Hijack OTE Transmitter Beam": {
                        "stat": "HACKING", "dc": 15,
                        "success": "end_net_god",
                        "fail": "net_exec_trap"
                    }
                }
            },
            "net_trace_fail": {
                "narrative": "CHECK FAILED! The attacker was waiting for your trace! A NetWatch ping locks onto your physical cyberdeck location near the Thermaikos waterfront.",
                "hp_change": -20,
                "suggested_actions": ["Jack out immediately"],
                "action_map": {
                    "Jack out immediately": "end_net_captured"
                }
            },

            # --- EXPANDED BRANCH: CITADEL BROADCAST ---
            "net_citadel_broadcast": {
                "narrative": "SUCCESS! You hijack the high-frequency transmitter on top of the heavily armored White Citadel. Cybernetic holograms project 'PROJECT_OLYMPUS' files across the sky over the Thermaikos Gulf.",
                "eddies_change": 1500,
                "new_items": ["White Citadel Root Access"],
                "suggested_actions": ["Demand Ransom from Arasaka Execs", "Broadcast to Underground Resistance"],
                "new_location": "Thessaloniki - White Citadel Tower",
                "action_map": {
                    "Demand Ransom from Arasaka Execs": "end_net_rich",
                    "Broadcast to Underground Resistance": "end_net_hero"
                }
            },
            "net_citadel_fail": {
                "narrative": "CHECK FAILED! The White Citadel's auto-defenses detect your intrusion vector and unleash lethal lethal neural feedback.",
                "hp_change": -50,
                "suggested_actions": ["Emergency Disconnect"],
                "action_map": {
                    "Emergency Disconnect": "end_flatline"
                }
            },

            # --- COMMON & ENDING SCENARIOS ---
            "net_exec_trap": {
                "narrative": "FAIL! Arasaka's executive counter-daemons at Aristotelous Plaza purge your cyberdeck storage and lock your neural buffer. You barely disconnect before brain death.",
                "hp_change": -40,
                "lost_items": ["Project Olympus Schematics"],
                "is_game_over": True
            },
            "net_disconnect": {
                "narrative": "Emergency jack-out executed in a damp alleyway behind Ladadika. You purge memory buffers and return to physical reality empty-handed, but alive.",
                "is_game_over": True
            },
            "end_flatline": {
                "narrative": "CRITICAL SYSTEM FAILURE: High-voltage Black ICE fries your central nervous system. Your optic implants fade to black permanently along the neon shore.",
                "hp_change": -100,
                "is_game_over": True
            },
            "end_net_god": {
                "narrative": "MISSION COMPLETE: You commandeer Arasaka's executive subnet at Aristotelous Plaza! You now control Thessalonki's entire automated power grid and sky-defense from the shadows as the ultimate Net God.",
                "eddies_change": 10000,
                "is_game_over": True
            },
            "end_net_rich": {
                "narrative": "MISSION COMPLETE: A Shadow Fixer operating out of the Ano Poli sky-villas buys the schematics for a fortune. You wire 5,000 Eddies to your account and retire off-grid.",
                "eddies_change": 5000,
                "is_game_over": True
            },
            "end_net_hero": {
                "narrative": "MISSION COMPLETE: You broadcast NetWatch corruption across every holoscreen in Aristotelous Square. You become a folk hero in Thessaloniki's digital underground.",
                "is_game_over": True
            },
            "end_net_fixer": {
                "narrative": "MISSION COMPLETE: The NetWatch rogue becomes your permanent informant. You now rule Thessaloniki's underground data broker network from OTE Tower.",
                "eddies_change": 3000,
                "is_game_over": True
            },
            "end_net_captured": {
                "narrative": "MISSION COMPLETE (FAILED): A NetWatch strike team raids your location by the harbor. You spend the rest of your life in a high-security cyber-prison in the Aegean.",
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
        "location": "Thessaloniki - Kamara Cyber-Arch Junction",
        "stats": {"HACKING": 1, "COMBAT": 5, "TECH": 2},
        "start_scenario": "solo_start",
        "scenarios": {
            # --- STAGE 1: ALLEY AMBUSH (KAMARA CYBER-ARCH) ---
            "solo_start": {
                "illustration": "class-2.png",
                "narrative": "A pair of cyber-enhanced scavs jump you beneath the towering, holo-advert-encrusted Kamara Arch, weapons hot. Out of the corner of your eye, you spot a high-tier Militech supply crate sitting near an abandoned tram track.",
                "suggested_actions": ["Unload with Smart-Pistol", "Close in with Combat Knife", "Tactical slide to Militech Crate"],
                "new_location": "Thessaloniki - Kamara Underdeck Alley",
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
                "narrative": "TARGET ELIMINATED! Your smart-bullets home in and drop both scavs instantly onto the wet pavement. On one body, you find an encrypted bounty datapad listing a $2,000 hit on a local warlord hiding in Ano Poli.",
                "eddies_change": 300,
                "new_items": ["Bounty Datapad"],
                "suggested_actions": ["Assault Scav Stronghold in Ano Poli", "Turn Datapad in to NCPD at Aristotelous Plaza", "Infiltrate Helexpo Black Market"],
                "new_location": "Thessaloniki - Kamara Perimeter",
                "action_map": {
                    "Assault Scav Stronghold in Ano Poli": {
                        "stat": "COMBAT", "dc": 15,
                        "success": "end_solo_warlord",
                        "fail": "end_solo_overwhelmed"
                    },
                    "Turn Datapad in to NCPD at Aristotelous Plaza": "end_solo_bounty",
                    "Infiltrate Helexpo Black Market": {
                        "stat": "COMBAT", "dc": 13,
                        "success": "solo_helexpo_raid",
                        "fail": "end_solo_overwhelmed"
                    }
                }
            },
            "solo_gun_fail": {
                "narrative": "CHECK FAILED! A localized EMP jammer glitches your smart-pistol targeting. You take heavy crossfire (-40 HP) before diving behind a concrete pillar.",
                "hp_change": -40,
                "suggested_actions": ["Draw Combat Knife for final stand", "Retreat into the Sub-Level Catacombs"],
                "action_map": {
                    "Draw Combat Knife for final stand": {
                        "stat": "COMBAT", "dc": 13,
                        "success": "solo_knife_win",
                        "fail": "end_solo_overwhelmed"
                    },
                    "Retreat into the Sub-Level Catacombs": "end_solo_coward"
                }
            },

            # --- STAGE 2: BRANCH B (TACTICAL CRATE) ---
            "solo_crate_win": {
                "narrative": "TACTICAL SUCCESS! You slide past gunfire, breach the Militech crate with your boot, and pull out a prototype Heavy Plasma Cannon!",
                "new_items": ["Prototype Plasma Cannon"],
                "suggested_actions": ["Annihilate the ambush squad", "Sell cannon to street gang at Ladadika", "Storm the White Citadel Armory"],
                "action_map": {
                    "Annihilate the ambush squad": "end_solo_merc_legend",
                    "Sell cannon to street gang at Ladadika": "end_solo_arms_dealer",
                    "Storm the White Citadel Armory": {
                        "stat": "COMBAT", "dc": 16,
                        "success": "end_solo_citadel_conqueror",
                        "fail": "end_solo_overwhelmed"
                    }
                }
            },
            "solo_crate_fail": {
                "narrative": "CHECK FAILED! The crate lock jams, leaving you pinned in the open. A shotgun blast shreds your Armor Plating (-50 HP).",
                "hp_change": -50,
                "lost_items": ["Armor Plating"],
                "suggested_actions": ["Retreat into the Sub-Level Catacombs"],
                "action_map": {
                    "Retreat into the Sub-Level Catacombs": "end_solo_coward"
                }
            },

            # --- STAGE 2: BRANCH C (COMBAT KNIFE) ---
            "solo_knife_win": {
                "narrative": "CRITICAL HIT! You close the distance, driving your knife straight into the scav leader's cybernetic neck joint before disarming his squadmate.",
                "eddies_change": 500,
                "new_items": ["Custom Cyberware Core"],
                "suggested_actions": ["Claim Upper Ano Poli Territory"],
                "action_map": {
                    "Claim Upper Ano Poli Territory": "end_solo_warlord"
                }
            },
            "solo_knife_fail": {
                "narrative": "CHECK FAILED! You miss your leap on the slick wet asphalt and take a point-blank shotgun blast to the chest.",
                "hp_change": -70,
                "is_game_over": True
            },

            # --- EXPANDED BRANCH: HELEXPO RAID ---
            "solo_helexpo_raid": {
                "narrative": "SUCCESS! You breach the illegal arms exhibition at the Helexpo Grounds, taking down corporate arms dealers and seizing an experimental gunship prototype.",
                "eddies_change": 2500,
                "new_items": ["Militech Gunship Keys"],
                "suggested_actions": ["Rule the City Skies", "Sell Gunship to Syndicate"],
                "new_location": "Thessaloniki - Helexpo Cyber Grounds",
                "action_map": {
                    "Rule the City Skies": "end_solo_merc_legend",
                    "Sell Gunship to Syndicate": "end_solo_arms_dealer"
                }
            },

            # --- ENDINGS ---
            "end_solo_warlord": {
                "narrative": "MISSION COMPLETE: You storm the Scav stronghold overlooking the city in ancient Ano Poli, eliminate the boss, and take control of Thessaloniki's mercenary underworld.",
                "eddies_change": 4000,
                "is_game_over": True
            },
            "end_solo_bounty": {
                "narrative": "MISSION COMPLETE: NCPD headquarters at Aristotelous Plaza transfers 2,000 Eddies to your account. You restock top-tier ammo for your next contract.",
                "eddies_change": 2000,
                "is_game_over": True
            },
            "end_solo_merc_legend": {
                "narrative": "MISSION COMPLETE: You obliterate the scav squad with the plasma cannon. Your display of sheer force makes you a feared mercenary legend across all sectors.",
                "is_game_over": True
            },
            "end_solo_citadel_conqueror": {
                "narrative": "MISSION COMPLETE: You breach and seize the corporate guard hub at the White Citadel! Corporate security surrenders control of the coastline to you.",
                "eddies_change": 8000,
                "is_game_over": True
            },
            "end_solo_arms_dealer": {
                "narrative": "MISSION COMPLETE: You fence the Militech technology for 6,000 Eddies on the Ladadika black market and retire from street combat.",
                "eddies_change": 6000,
                "is_game_over": True
            },
            "end_solo_overwhelmed": {
                "narrative": "MISSION COMPLETE (FAILED): Outnumbered and bleeding out, you are executed in the dark alleyways beneath Kamara.",
                "is_game_over": True
            },
            "end_solo_coward": {
                "narrative": "MISSION COMPLETE: You crawl into the subterranean catacombs, surviving the fight but losing all your street reputation.",
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
        "location": "Thessaloniki - Under-City Workshop (Rotunda Vaults)",
        "stats": {"HACKING": 2, "COMBAT": 1, "TECH": 5},
        "start_scenario": "tech_start",
        "scenarios": {
            # --- STAGE 1: WORKSHOP DISCOVERY (ROTUNDA VAULTS) ---
            "tech_start": {
                "illustration": "class-1.png",
                "narrative": "While stripping servo-motors from a discarded military drone in your workshop hidden near the Rotunda's subterranean catacombs, your scanner picks up an active AI Core. Suddenly, a local protection syndicate knocks hard on your reinforced steel doors!",
                "suggested_actions": ["Hotwire core into combat drone", "Rig door with scrap explosive", "Extract core and escape to Ladadika"],
                "new_location": "Thessaloniki - Under-City Workshop",
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
                    "Extract core and escape to Ladadika": {
                        "stat": "TECH", "dc": 14,
                        "success": "tech_extract_win",
                        "fail": "tech_extract_fail"
                    }
                }
            },

            # --- STAGE 2: BRANCH A (COMBAT DRONE) ---
            "tech_drone_win": {
                "narrative": "SUCCESS! The military drone boots up, hovering with twin autocannons active. It bursts through your workshop door and drives the syndicate forces out into Kamara plaza!",
                "new_items": ["Combat Drone Companion"],
                "suggested_actions": ["Upgrade Drone into Mech Armor", "Deploy Drone to guard Aristotelous vendors", "Harness OTE Tower Power Grid"],
                "new_location": "Thessaloniki - Rotunda Outer Ring",
                "action_map": {
                    "Upgrade Drone into Mech Armor": {
                        "stat": "TECH", "dc": 15,
                        "success": "end_tech_titan",
                        "fail": "end_tech_overload"
                    },
                    "Deploy Drone to guard Aristotelous vendors": "end_tech_patron",
                    "Harness OTE Tower Power Grid": {
                        "stat": "TECH", "dc": 14,
                        "success": "tech_ote_overcharge",
                        "fail": "end_tech_overload"
                    }
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
                "narrative": "BOOM! The scrap explosive detonates as the gangers breach the door, disabling them instantly. In the wreckage, you recover a high-grade Militech hydraulic power frame.",
                "eddies_change": 400,
                "new_items": ["Hydraulic Power Frame"],
                "suggested_actions": ["Sell frame at Ladadika Black Market", "Build custom Exo-Suit in Ano Poli"],
                "action_map": {
                    "Sell frame at Ladadika Black Market": "end_tech_wealth",
                    "Build custom Exo-Suit in Ano Poli": "end_tech_titan"
                }
            },
            "tech_trap_fail": {
                "narrative": "CHECK FAILED! The tripwire snaps prematurely! The syndicate breaches your workshop and loots your equipment.",
                "hp_change": -30,
                "lost_items": ["Toolkit"],
                "is_game_over": True
            },

            # --- STAGE 2: BRANCH C (EXTRACT CORE) ---
            "tech_extract_win": {
                "narrative": "CRITICAL EXTRACT! You carefully use your torch as a delicate scalpel, recovering an intact, pristine AI core before slipping out through the drainage pipes to Ladadika.",
                "new_items": ["Pristine AI Core"],
                "suggested_actions": ["Sell AI Core to Aristotelous bidder", "Build automated Helexpo factory"],
                "action_map": {
                    "Sell AI Core to Aristotelous bidder": "end_tech_wealth",
                    "Build automated Helexpo factory": "end_tech_factory"
                }
            },
            "tech_extract_fail": {
                "narrative": "CHECK FAILED! You puncture the AI core matrix, causing a localized shockwave that demolishes your workbench.",
                "hp_change": -35,
                "is_game_over": True
            },

            # --- EXPANDED BRANCH: OTE OVERCHARGE ---
            "tech_ote_overcharge": {
                "narrative": "SUCCESS! You tap into the high-voltage relay of the OTE Tower, supercharging your drone mesh network across the whole metropolis.",
                "eddies_change": 2000,
                "new_items": ["Overcharged Power Grid Interface"],
                "suggested_actions": ["Monopolize City Energy Grid", "Establish Cyber-Tech Haven in Ano Poli"],
                "new_location": "Thessaloniki - OTE Tower Summit",
                "action_map": {
                    "Monopolize City Energy Grid": "end_tech_factory",
                    "Establish Cyber-Tech Haven in Ano Poli": "end_tech_patron"
                }
            },

            # --- ENDINGS ---
            "end_tech_titan": {
                "narrative": "MISSION COMPLETE: You construct a piloted Cyber-Mech! You become the unstoppable titan guarding the historic streets of Thessaloniki.",
                "eddies_change": 2000,
                "is_game_over": True
            },
            "end_tech_patron": {
                "narrative": "MISSION COMPLETE: Your autonomous drones protect Aristotelous Square and local street vendors. Grateful merchant guilds pool their funds to pay you a huge weekly retainer.",
                "eddies_change": 3000,
                "is_game_over": True
            },
            "end_tech_wealth": {
                "narrative": "MISSION COMPLETE: High-tech black market bidders at Ladadika enter a price war for your loot. You net 7,000 Eddies and open a chain of ripperdoc tech clinics.",
                "eddies_change": 7000,
                "is_game_over": True
            },
            "end_tech_factory": {
                "narrative": "MISSION COMPLETE: You construct an automated micro-factory in the abandoned Helexpo pavilions that mass-produces cyberware, making you the premier tech mogul of the city.",
                "eddies_change": 10000,
                "is_game_over": True
            },
            "end_tech_overload": {
                "narrative": "MISSION COMPLETE (FAILED): Overclocking the cyberware triggers a catastrophic meltdown, blowing your workshop straight into the Aegean Sea.",
                "hp_change": -100,
                "is_game_over": True
            }
        }
    }
}