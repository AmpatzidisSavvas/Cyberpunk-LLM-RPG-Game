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
            "net_start": {
                "narrative": "Neon code streams across your retinas as you jack into the local grid near Ladadika. Traces of Arasaka Black ICE flare up, threatening to fry your deck.",
                "suggested_actions": ["Bypass the firewall", "Dump cache and disconnect", "Trace the attacker"],
                "new_location": "Neo-Thessaloniki - Deep Net Subgrid",
                "action_map": {
                    "Bypass the firewall": {
                        "stat": "HACKING", "dc": 12,
                        "success": "net_bypass_success",
                        "fail": "net_bypass_fail"
                    },
                    "Dump cache and disconnect": "net_disconnect",
                    "Trace the attacker": {
                        "stat": "HACKING", "dc": 15,
                        "success": "net_trace_success",
                        "fail": "net_trace_fail"
                    }
                }
            },
            "net_bypass_success": {
                "narrative": "CRITICAL SUCCESS! Your ICE-Breaker tears through the Arasaka firewall. You gain root access to the main node and siphon corporate secret funds.",
                "eddies_change": 500,
                "new_items": ["Arasaka Prototype Schematics"],
                "suggested_actions": ["Upload schematics to open network", "Sell data to shadow fixer"],
                "action_map": {
                    "Upload schematics to open network": "end_net_hero",
                    "Sell data to shadow fixer": "end_net_rich"
                }
            },
            "net_bypass_fail": {
                "narrative": "CHECK FAILED! The firewall counters with feedback code, frying your deck interface and shocking your nervous system (-30 HP).",
                "hp_change": -30,
                "suggested_actions": ["Dump cache and disconnect"],
                "action_map": {
                    "Dump cache and disconnect": "net_disconnect"
                }
            },
            "net_disconnect": {
                "narrative": "You dump memory buffers and jack out safely, but leave empty-handed.",
                "is_game_over": True
            },
            "net_trace_success": {
                "narrative": "CRITICAL SUCCESS! You locate the netrunner trap and turn their daemon against them, gaining an executive access code.",
                "new_items": ["Exec Access Code"],
                "suggested_actions": ["Sell data to shadow fixer"],
                "action_map": {
                    "Sell data to shadow fixer": "end_net_rich"
                }
            },
            "net_trace_fail": {
                "narrative": "CHECK FAILED! Tracing backfires—NetWatch detects your signal instantly.",
                "hp_change": -40,
                "is_game_over": True
            },
            "end_net_hero": {
                "narrative": "MISSION COMPLETE: You exposed Arasaka across Neo-Thessaloniki and became a legend in the digital sprawl.",
                "is_game_over": True
            },
            "end_net_rich": {
                "narrative": "MISSION COMPLETE: You sold high-grade corp secrets and retired to an off-grid penthouse.",
                "eddies_change": 5000,
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
            "solo_start": {
                "narrative": "A pair of cyber-enhanced scavs jump you from behind an overturned container, weapons hot.",
                "suggested_actions": ["Unload with Smart-Pistol", "Close in with Combat Knife"],
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
                    }
                }
            },
            "solo_gun_win": {
                "narrative": "TARGET ELIMINATED! Your smart-bullets lock on and drop both scavs instantly.",
                "eddies_change": 300,
                "new_items": ["Bounty Beacon"],
                "suggested_actions": ["Claim bounty with police"],
                "action_map": {"Claim bounty with police": "end_solo_bounty"}
            },
            "solo_gun_fail": {
                "narrative": "CHECK FAILED! Smart-targeting glitches—you take heavy crossfire before pulling back (-40 HP).",
                "hp_change": -40,
                "is_game_over": True
            },
            "solo_knife_win": {
                "narrative": "CRITICAL HIT! You disarm the scavs in close quarters and claim their gear.",
                "new_items": ["Scav Weapon Array"],
                "eddies_change": 400,
                "is_game_over": True
            },
            "solo_knife_fail": {
                "narrative": "CHECK FAILED! You miss the leap and take a point-blank blast.",
                "hp_change": -60,
                "is_game_over": True
            },
            "end_solo_bounty": {
                "narrative": "MISSION COMPLETE: Police deposit a fat bounty into your account. Another contract closed.",
                "eddies_change": 2000,
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
            "tech_start": {
                "narrative": "You're stripping out functional servo-motors from a discarded military drone when you locate an active AI core.",
                "suggested_actions": ["Hotwire core into drone", "Extract core carefully"],
                "action_map": {
                    "Hotwire core into drone": {
                        "stat": "TECH", "dc": 11,
                        "success": "tech_win",
                        "fail": "tech_fail"
                    },
                    "Extract core carefully": {
                        "stat": "TECH", "dc": 14,
                        "success": "tech_extract_win",
                        "fail": "tech_fail"
                    }
                }
            },
            "tech_win": {
                "narrative": "SUCCESS! The drone boots up and obeys your subroutines, becoming your personal automated defense unit.",
                "new_items": ["Combat Drone Companion"],
                "is_game_over": True
            },
            "tech_extract_win": {
                "narrative": "CRITICAL EXTRACT! You recover the intact pristine core and sell it on the black market.",
                "eddies_change": 3000,
                "is_game_over": True
            },
            "tech_fail": {
                "narrative": "CHECK FAILED! The power capacitor overloads, scorching your hands and ruining the scavenge.",
                "hp_change": -25,
                "is_game_over": True
            }
        }
    }
}