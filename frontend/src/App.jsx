import React, { useState, useEffect } from "react";
import axios from "axios";

import ClassSelectionScreen from "./components/ClassSelection";
import GameplayScreen from "./components/GameplayScreen";
import { sounds } from "./utils/audio";

export default function App() {
	const [step, setStep] = useState("SELECT_CLASS");
	const [classesData, setClassesData] = useState({});
	const [loadingClasses, setLoadingClasses] = useState(true);

	const [player, setPlayer] = useState(null);
	const [logs, setLogs] = useState([]);
	const [input, setInput] = useState("");
	const [suggestedActions, setSuggestedActions] = useState([]);
	const [isGameOver, setIsGameOver] = useState(false);
	const [loading, setLoading] = useState(false);
	const [crtEnabled, setCrtEnabled] = useState(true);
	const [audioEnabled, setAudioEnabled] = useState(true);

	// --- DICE ROLL MODAL STATE ---
	const [rolling, setRolling] = useState(false);
	const [animatedRollValue, setAnimatedRollValue] = useState(1);
	const [rollData, setRollData] = useState(null);
	const [rollFinished, setRollFinished] = useState(false);
	const [pendingResponse, setPendingResponse] = useState(null);

	useEffect(() => {
		axios
			.get("http://127.0.0.1:8000/api/classes")
			.then((res) => {
				setClassesData(res.data);
				setLoadingClasses(false);
			})
			.catch((err) => {
				console.error("Could not fetch classes from backend:", err);
				setLoadingClasses(false);
			});
	}, []);

	const applyTurnResponse = (responseData) => {
		if (responseData.roll) {
			const { stat_used, d20_roll, modifier, total, dc, effective_dc, rep_modifier, success } = responseData.roll;
			const icon = success ? "✅" : "💀";
			const outcomeText = success ? "SUCCESS" : "CRITICAL FAILURE";
			const dcText = rep_modifier
				? `Effective DC ${effective_dc} (Base ${dc}, Rep Mod ${rep_modifier > 0 ? `+${rep_modifier}` : rep_modifier})`
				: `DC ${dc}`;
			const rollLog = `[CHECK: ${stat_used}] 🎲 d20(${d20_roll}) + Mod(${modifier}) = ${total} vs ${dcText} ➔ ${outcomeText} ${icon}`;

			setLogs((prev) => [...prev, { sender: "SYSTEM", text: rollLog }, { sender: "STORY", text: responseData.narrative }]);
		} else {
			setLogs((prev) => [...prev, { sender: "STORY", text: responseData.narrative }]);
		}

		setPlayer((prev) => {
			if (!prev) return prev;
			return {
				...prev,
				hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (responseData.hp_change || 0))),
				eddies: Math.max(0, prev.eddies + (responseData.eddies_change || 0)),
				current_node_id: responseData.current_node_id || prev.current_node_id,
				story_pins: Array.isArray(responseData.story_pins) ? responseData.story_pins : prev.story_pins,
				location: responseData.new_location || prev.location,
				reputation: responseData.updated_reputation || prev.reputation,
			};
		});

		if (responseData.is_game_over) {
			setIsGameOver(true);
			setSuggestedActions([]);
		} else if (responseData.suggested_actions) {
			setSuggestedActions(responseData.suggested_actions);
		}
	};

	const handleSelectClass = async (roleName, info) => {
		if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();

		const startingRep = info.reputation
			? { ...info.reputation }
			: { corporates: 0, underground: 0, law_enforcement: 0 };

		const startingPins = Array.isArray(info.story_pins)
			? info.story_pins.map((p) => ({ ...p }))
			: [];

		const selectedPlayer = {
			name: "V-2077",
			role: roleName,
			hp: info.hp,
			max_hp: info.max_hp,
			eddies: info.eddies,
			current_node_id: info.current_node_id || "venizelou",
			story_pins: startingPins,
			location: info.location,
			stats: info.stats || { HACKING: 1, COMBAT: 1, TECH: 1 },
			reputation: startingRep,
		};

		setPlayer(selectedPlayer);
		setLoading(true);
		setIsGameOver(false);
		setStep("GAME");

		try {
			const res = await axios.post("http://127.0.0.1:8000/api/start", selectedPlayer);
			const { system_log, story, current_node_id, story_pins } = res.data;

			setLogs([
				{ sender: "SYSTEM", text: system_log },
				{ sender: "STORY", text: story.narrative },
			]);
			setSuggestedActions(story.suggested_actions || []);

			setPlayer((prev) => ({
				...prev,
				reputation: res.data?.reputation ?? prev.reputation,
				current_node_id: current_node_id || story.current_node_id || prev.current_node_id,
				story_pins: Array.isArray(story_pins) ? story_pins : prev.story_pins,
				location: story.new_location || prev.location,
			}));
		} catch (err) {
			setLogs([{ sender: "SYSTEM", text: "ERROR: UNABLE TO FETCH INITIAL STARTING DATA FROM BACKEND." }]);
		} finally {
			setLoading(false);
		}
	};

	const triggerDiceRollAnimation = (rollInfo, responseData) => {
		setRollData(rollInfo);
		setPendingResponse(responseData);
		setRolling(true);
		setRollFinished(false);

		let counter = 0;
		const interval = setInterval(() => {
			setAnimatedRollValue(Math.floor(Math.random() * 20) + 1);
			counter++;
			if (counter > 15) {
				clearInterval(interval);
				setAnimatedRollValue(rollInfo.d20_roll);
				setRollFinished(true);
				if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();
			}
		}, 70);
	};

	const handleCloseDiceModal = () => {
		if (!pendingResponse || !rollData) return;
		applyTurnResponse(pendingResponse);
		setRolling(false);
		setRollData(null);
		setPendingResponse(null);
		setRollFinished(false);
	};

	const handleAction = async (actionText) => {
		const userAction = actionText || input;
		if (!userAction.trim() || loading || isGameOver) return;

		if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();

		const updatedLogs = [...logs, { sender: "PLAYER", text: userAction }];
		setLogs(updatedLogs);
		setInput("");
		setLoading(true);

		try {
			const historyStrings = updatedLogs.map((l) => `${l.sender}: ${l.text}`);
			const res = await axios.post("http://127.0.0.1:8000/api/action", {
				action: userAction,
				player_state: player,
				history: historyStrings,
			});

			const data = res.data;

			if (data.roll) {
				triggerDiceRollAnimation(data.roll, data);
			} else {
				applyTurnResponse(data);
			}
		} catch (err) {
			setLogs((prev) => [...prev, { sender: "SYSTEM", text: "ERROR: NEURAL LINK DISRUPTED. BACKEND UNREACHABLE." }]);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen bg-[#080811] text-white relative overflow-x-hidden">
			<main className="relative z-10">
				{step === "SELECT_CLASS" ? (
					<ClassSelectionScreen
						classesData={classesData}
						loadingClasses={loadingClasses}
						onSelectClass={handleSelectClass}
					/>
				) : (
					<GameplayScreen
						player={player}
						logs={logs}
						loading={loading}
						crtEnabled={crtEnabled}
						setCrtEnabled={setCrtEnabled}
						isGameOver={isGameOver}
						suggestedActions={suggestedActions}
						input={input}
						setInput={setInput}
						handleAction={handleAction}
						onSwitchClass={() => setStep("SELECT_CLASS")}
						rolling={rolling}
						rollData={rollData}
						rollFinished={rollFinished}
						animatedRollValue={animatedRollValue}
						handleCloseDiceModal={handleCloseDiceModal}
					/>
				)}
			</main>
		</div>
	);
}