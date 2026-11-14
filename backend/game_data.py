CLASSES_DATA = {
    "Netrunner": {
        "description": "A digital phantom navigating the maritime data-cables and corporate black-ICE of Thessaloniki's port.",
        "hp": 90,
        "max_hp": 90,
        "eddies": 400,
        "inventory": ["Cyberdeck v2", "ICE-Breaker", "Encrypted Ghost-Chip"],
        "location": "Thessaloniki - Pier 6 Maritime Data Hub",
        "stats": {"HACKING": 5, "COMBAT": 1, "TECH": 2},
        "reputation": {"corporates": -10, "underground": 15, "law_enforcement": 0},
        "origin_theme": "Maritime cyber-espionage, ghost-ships at Thermaikos Port, and rogue AI smuggling.",
        "start_scenario": "net_start",
        "scenarios": {
            "net_start": {
                "illustration": "class-3.png",
                "narrative": "Salt mist clings to your visor inside a rusted shipping container at Pier 6. You are jacked directly into the Aegean Undersea Fiber Trunk, intercepting a ghost-freighter's neural cargo before Arasaka's harbor daemons trace your deck.",
                "suggested_actions": [
                    "Siphon the neural cargo manifest",
                    "Spoof harbor customs beacon to misdirect Arasaka",
                    "Deploy black-ICE trap on the freighter's bridge"
                ],
                "new_location": "Thessaloniki - Aegean Sub-Cable Node",
                "action_map": {
                    "Siphon the neural cargo manifest": {
                        "stat": "HACKING", "dc": 12, "faction": "corporates",
                        "success": "net_stage2_win",
                        "fail": "net_stage2_fail"
                    },
                    "Spoof harbor customs beacon to misdirect Arasaka": {
                        "stat": "HACKING", "dc": 13, "faction": "law_enforcement",
                        "success": "net_stage2_win",
                        "fail": "net_stage2_fail"
                    },
                    "Deploy black-ICE trap on the freighter's bridge": "net_stage2_win"
                }
            },
            "net_stage2_win": {
                "narrative": "Your code slips cleanly past the harbor firewalls. You decrypt the manifest: a rogue AI shard named 'KASSANDRA' is being smuggled toward Ladadika—and Arasaka hit-teams are already mobilizing to intercept it.",
                "eddies_change": 200,
                "reputation_change": {"corporates": -15, "underground": 10},
                "new_items": ["Kassandra Routing Key"],
                "new_location": "Thessaloniki - Ladadika Perimeter",
                "suggested_actions": [
                    "Track the smuggler convoy into Ladadika",
                    "Auction the Routing Key on the underground shadow-net",
                    "Infiltrate the local NetWatch relay to scrub your trace"
                ]
            },
            "net_stage2_fail": {
                "narrative": "Arasaka's harbor Black ICE snaps back like a whip, scorching your neural buffer (-20 HP) before you rip the cable free. You flee Pier 6 into the rain-slicked alleys of Ladadika with Arasaka drones scanning the rooftops.",
                "hp_change": -20,
                "reputation_change": {"corporates": -20},
                "new_location": "Thessaloniki - Ladadika Backstreets",
                "suggested_actions": [
                    "Hide inside a neon-lit cyber-cafe to patch your deck",
                    "Ambush a lone Arasaka recon drone for parts",
                    "Contact a local street fixer for safe passage"
                ]
            }
        }
    },

    "Gunner": {
        "description": "A battle-hardened street mercenary forged in the vertical gang wars of Ano Poli.",
        "hp": 130,
        "max_hp": 130,
        "eddies": 250,
        "inventory": ["Smart-Pistol", "Mono-Edge Knife", "Kevlar Trench"],
        "location": "Thessaloniki - Ano Poli Heptapyrgion Ramparts",
        "stats": {"HACKING": 1, "COMBAT": 5, "TECH": 2},
        "reputation": {"corporates": 0, "underground": 20, "law_enforcement": -15},
        "origin_theme": "Gritty rooftop gang warfare, Militech hit-squads, and street survival in Ano Poli.",
        "start_scenario": "solo_start",
        "scenarios": {
            "solo_start": {
                "illustration": "class-2.png",
                "narrative": "Rain lashes the ancient stone ramparts of Heptapyrgion overlooking the neon sprawl below. You're guarding a wounded Vardar Syndicate lieutenant when Militech hover-skiffs cut their engines and drop breach-teams onto the rooftop.",
                "suggested_actions": [
                    "Suppress the breach-team with Smart-Pistol fire",
                    "Drop smoke and flank through the Byzantine watchtower",
                    "Use the lieutenant as leverage to parley with Militech"
                ],
                "new_location": "Thessaloniki - Heptapyrgion Siege Zone",
                "action_map": {
                    "Suppress the breach-team with Smart-Pistol fire": {
                        "stat": "COMBAT", "dc": 11, "faction": "corporates",
                        "success": "solo_stage2_win",
                        "fail": "solo_stage2_fail"
                    },
                    "Drop smoke and flank through the Byzantine watchtower": {
                        "stat": "COMBAT", "dc": 13, "faction": "underground",
                        "success": "solo_stage2_win",
                        "fail": "solo_stage2_fail"
                    },
                    "Use the lieutenant as leverage to parley with Militech": "solo_stage2_betray"
                }
            },
            "solo_stage2_win": {
                "narrative": "Your smart-rounds tear through the Militech vanguard, forcing their skiff to peel off into the storm. The grateful Vardar lieutenant hands you an encrypted briefcase bound for Aristotelous Plaza before passing out.",
                "eddies_change": 300,
                "reputation_change": {"underground": 15, "corporates": -15},
                "new_items": ["Vardar Encrypted Briefcase"],
                "new_location": "Thessaloniki - Ano Poli Descent",
                "suggested_actions": [
                    "Descend toward Aristotelous Plaza to deliver the briefcase",
                    "Crack open the briefcase to inspect the payload",
                    "Loot the fallen Militech troopers for heavy gear"
                ]
            },
            "solo_stage2_fail": {
                "narrative": "Suppressive fire pins you behind crumbling stone, and a stray plasma bolt grazes your shoulder (-25 HP). The Vardar lieutenant is captured, leaving you wounded and hunted across the upper city walls.",
                "hp_change": -25,
                "reputation_change": {"underground": -15},
                "new_location": "Thessaloniki - Ano Poli Slums",
                "suggested_actions": [
                    "Track the Militech extraction convoy down the hill",
                    "Find an underground ripperdoc in the slums",
                    "Set an ambush along the narrow cobblestone stairs"
                ]
            },
            "solo_stage2_betray": {
                "narrative": "You lower your weapon and hand over the syndicate lieutenant. Militech transfers a fat cred-chip to your account, though word of your betrayal spreads instantly across Thessaloniki's underworld.",
                "eddies_change": 600,
                "reputation_change": {"corporates": 25, "underground": -35},
                "new_location": "Thessaloniki - Corporate Checkpoint",
                "suggested_actions": [
                    "Take a Militech corporate contract in Aristotelous Plaza",
                    "Lay low in a neutral bar near the waterfront",
                    "Use your new eddies to upgrade your combat cyberware"
                ]
            }
        }
    },

    "Techie": {
        "description": "An underground cyber-archaeologist salvaging pre-collapse tech from the flooded metro ruins.",
        "hp": 100,
        "max_hp": 100,
        "eddies": 300,
        "inventory": ["Arc-Welder", "Salvage Scanner", "Magnetic Grapple"],
        "location": "Thessaloniki - Venizelou Deep Metro Ruins",
        "stats": {"HACKING": 2, "COMBAT": 1, "TECH": 5},
        "reputation": {"corporates": 0, "underground": 10, "law_enforcement": 5},
        "origin_theme": "Subterranean cyber-archaeology, flooded metro tunnels beneath Egnatia, and pre-collapse machinery.",
        "start_scenario": "tech_start",
        "scenarios": {
            "tech_start": {
                "illustration": "class-1.png",
                "narrative": "Fifty meters beneath Egnatia Street, your headlamp illuminates marble Roman columns fused with corroded 2040s transit rails. Your scanner locks onto a humming pre-collapse fusion cell—just as automated excavation spiders wake up in the dark.",
                "suggested_actions": [
                    "Overload the excavation spiders with your Arc-Welder",
                    "Rig a magnetic grapple to yank the fusion cell free",
                    "Re-route the tunnel's dormant floodgates to trap the machines"
                ],
                "new_location": "Thessaloniki - Subterranean Roman Vaults",
                "action_map": {
                    "Overload the excavation spiders with your Arc-Welder": {
                        "stat": "TECH", "dc": 12, "faction": "underground",
                        "success": "tech_stage2_win",
                        "fail": "tech_stage2_fail"
                    },
                    "Rig a magnetic grapple to yank the fusion cell free": {
                        "stat": "TECH", "dc": 13, "faction": "corporates",
                        "success": "tech_stage2_win",
                        "fail": "tech_stage2_fail"
                    },
                    "Re-route the tunnel's dormant floodgates to trap the machines": "tech_stage2_win"
                }
            },
            "tech_stage2_win": {
                "narrative": "Sparks shower the flooded tracks as the ancient machines short out. You pry loose the unstable pre-collapse Fusion Cell—a relic worth a fortune to either corporate labs or the underground resistance.",
                "eddies_change": 150,
                "reputation_change": {"underground": 10},
                "new_items": ["Pre-Collapse Fusion Cell"],
                "new_location": "Thessaloniki - Rotunda Sub-Basement",
                "suggested_actions": [
                    "Ascend into the Rotunda market to find a buyer",
                    "Modify your Arc-Welder using the Fusion Cell's energy",
                    "Explore deeper into the sealed Byzantine catacombs"
                ]
            },
            "tech_stage2_fail": {
                "narrative": "The fusion housing vents superheated steam, blistering your arms (-20 HP) as the tunnel ceiling begins to cave in. You scramble up a maintenance ladder into the neon glare of Egnatia Street empty-handed.",
                "hp_change": -20,
                "new_location": "Thessaloniki - Egnatia Neon Strip",
                "suggested_actions": [
                    "Salvage scrap parts from a wrecked transit drone",
                    "Visit a Rotunda workshop to treat your burns",
                    "Check local fixer boards for a quick repair job"
                ]
            }
        }
    }
}