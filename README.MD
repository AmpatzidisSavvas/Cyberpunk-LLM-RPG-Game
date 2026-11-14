# Cyberpunk LLM RPG Game

<p>
  <strong>Cyberpunk LLM RPG Game</strong> is an interactive role-playing game inspired by the cyberpunk genre, built with <strong>React</strong> and <strong>Python</strong>. The project combines a futuristic cyberpunk setting with Large Language Models (LLMs) to create an immersive, dynamic storytelling experience where players can explore a dystopian version of Thessaloniki, interact with a dangerous world, and shape their own adventures through their choices.
</p>

<p>
  The game blends traditional RPG mechanics with AI-powered narrative generation, allowing players to choose different character classes, make decisions, and experience branching storylines influenced by their statistics, dice rolls, and faction reputation.
</p>

<h2>🛠️ Technologies</h2>

<ul>
  <li><strong>React</strong> - Frontend user interface and interactive gameplay.</li>
  <li><strong>Python</strong> - Backend logic and game systems.</li>
  <li><strong>FastAPI</strong> - REST API for communication between the frontend and backend.</li>
  <li><strong>Ollama</strong> - Local execution of Large Language Models.</li>
  <li><strong>Qwen 2.5 3B</strong> - AI model responsible for dynamically generating narratives and suggested actions.</li>
  <li><strong>Pydantic</strong> - Data validation and structured game responses.</li>
  <li><strong>Uvicorn</strong> - ASGI server used to run the backend.</li>
</ul>

<h2>🎮 Features</h2>

<ul>
  <li><strong>Cyberpunk-inspired world:</strong> A futuristic dystopian version of Thessaloniki, Greece.</li>
  <li><strong>Character Classes:</strong> Choose between Netrunner, Gunner, and Techie, each with unique attributes, equipment, and starting scenarios.</li>
  <li><strong>Interactive Gameplay:</strong> Make decisions that influence the progression of the story.</li>
  <li><strong>AI-powered storytelling:</strong> Qwen 2.5 3B generates dynamic narratives and new suggested actions.</li>
  <li><strong>Dice-based RPG Mechanics:</strong> Actions are resolved through D20 dice rolls combined with character statistics.</li>
  <li><strong>Faction Reputation System:</strong> Player decisions influence relationships with corporations, the underground, and law enforcement.</li>
  <li><strong>Player Statistics and Inventory:</strong> Manage health (HP), Eddies, equipment, and character attributes.</li>
  <li><strong>Branching Storylines:</strong> Different decisions lead to different outcomes and story developments.</li>
  <li><strong>Anti-Repetition System:</strong> Tracks previously used actions to encourage fresh gameplay choices.</li>
</ul>

<h2>🚀 Project Goal</h2>

<p>
  The goal of this project is to explore the integration of Large Language Models into RPG game development, creating a more immersive and adaptable gaming experience where player choices influence the story.
</p>

<p>
  By combining predefined story scenarios with AI-generated events, the game aims to balance structured RPG progression with the flexibility of dynamic storytelling.
</p>

<h2>⚙️ How to Run the Application</h2>

<h3>Prerequisites</h3>

<p>Before running the application, make sure you have installed:</p>

<ul>
  <li>Python</li>
  <li>Node.js and npm</li>
  <li><a href="https://ollama.com/">Ollama</a></li>
</ul>

<h3>1. Clone the Repository</h3>

<pre>
git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
</pre>

<h3>2. Install Backend Dependencies</h3>

<pre>
pip install fastapi uvicorn ollama pydantic
</pre>

<h3>3. Download the AI Model</h3>

<p>Make sure Ollama is running, then download the required model:</p>

<pre>
ollama pull qwen2.5:3b
</pre>

<h3>4. Start the Backend</h3>

<pre>
python main.py
</pre>

<p>Alternatively, run the backend using Uvicorn:</p>

<pre>
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
</pre>

<p>The backend will be available at:</p>

<pre>
http://127.0.0.1:8000
</pre>

<h3>5. Start the Frontend</h3>

<p>Open a new terminal, navigate to the frontend directory, and install the dependencies:</p>

<pre>
npm install
</pre>

<p>Start the React development server:</p>

<pre>
npm run dev
</pre>

<p>The frontend should be available at:</p>

<pre>
http://localhost:5173
</pre>


<h2>📌 Project Status</h2>

<p>
  🚧 This project is currently under development. More features and improvements may be added over time.
</p>