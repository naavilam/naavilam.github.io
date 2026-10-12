---
layout: post
title:  "Quantum Battleship"
description: "Play Battleship and explore quantum-inspired randomness through match records and statistical analysis."
type: card-dated
date:   2025-04-11
image: batalha-naval-quantica.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-11
tag: Game
author: Nara Avila
card: card-1
repo: quantum-computing-research/Batalha-Naval-Quantica
live_url: https://quantum-computing-research.github.io/Batalha-Naval-Quantica
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-qubat">
<header class="guide-hero">
	<span class="eyebrow">Game and research experiment</span>
	<h2>Quantum Battleship</h2>
	<p class="lead">A familiar game becomes a way to investigate randomness. You choose coordinates to find the opponent's fleet; the computer uses measurement-derived choices to attack yours. Finish a battle, inspect its record and compare the distributions behind those choices.</p>
</header>
<nav class="guide-nav" aria-label="Guide sections">
	<a href="{{ page.url | relative_url }}#idea">The idea</a>
	<a href="{{ page.url | relative_url }}#backend">Setup</a>
	<a href="{{ page.url | relative_url }}#player">Start</a>
	<a href="{{ page.url | relative_url }}#turn">Play</a>
	<a href="{{ page.url | relative_url }}#finish">Match record</a>
	<a href="{{ page.url | relative_url }}#statistics">Analysis</a>
	<a href="{{ page.url | relative_url }}#architecture">Architecture</a>
</nav>
<p>The screenshots below show the English interface. Portuguese and Chinese are also available through the language selector. The gameplay, completed record and charts use a local demonstration with synthetic data, not a live hardware execution.</p>

<section id="idea">
	<h3>Why put quantum randomness inside a game?</h3>
	<p>The project connects quantum computing, a playable interface and empirical data analysis. Instead of looking at isolated bit strings, players see random choices become coordinates, hits and misses. Each completed match supplies observations that can be examined individually or combined with other matches associated with the same hardware.</p>
	<p>Measurement outcomes are mapped to positions on a board. The circuit panel makes that connection visible, while an optional classical search component helps the computer follow up on hits. This separates the source of an attack from the strategy used to find a ship.</p>
	<aside class="guide-callout"><strong>What the current version measures.</strong> The v0 experience uses synthetic data and reusable caches associated with the selected hardware. Selecting a hardware card does not mean that a new job runs on that physical device. Simulated data can demonstrate the workflow, but cannot establish the quality of a real quantum processor or certify quantum randomness.</aside>
</section>

<section id="backend">
	<div class="step-heading"><span class="step-number">01</span><h3>Configure the battle</h3></div>
	<p>Select a computer from the hardware carousel, then choose a <strong>4 × 4, 8 × 8 or 16 × 16</strong> board and the number of ships. The fleet options depend on board size. Use <strong>PT</strong>, <strong>EN</strong> or <strong>ZH</strong> in the header to change the interface language.</p>
	<p>The AWS Braket price field is an <strong>estimate for the selected hardware</strong>, not a bill for playing with cached or synthetic data.</p>
	<aside class="guide-callout">
		<strong>Want a harder opponent? Enable classical assistance.</strong>
		<p>Before starting, use the CPU-chip difficulty button to enable hard mode (Plus). In normal mode, the opponent uses quantum-source coordinates without the classical follow-up search. In hard mode, a hit activates a classical computer that targets neighboring cells to finish locating and sinking that ship.</p>
		<p>As more hits reveal a horizontal or vertical alignment, the search follows that direction. Once the targeted ship is sunk, the classical helper switches off and quantum-source attacks resume until another hit activates it. This makes the match harder by turning a chance discovery into a focused search, rather than leaving every next attack to the quantum-source sequence.</p>
	</aside>
	{% include software-figure.html folder="quantum-battleship" file="qubat01.png" alt="Quantum Battleship hardware carousel, board size, fleet and estimated price controls" caption="Select the hardware association and configure the board, fleet and difficulty before starting." %}
</section>

<section id="player">
	<div class="step-heading"><span class="step-number">02</span><h3>Enter your name and confirm participation</h3></div>
	<p>Choose <strong>Start match</strong> (<em>Iniciar partida</em>). Enter your player name in the participation dialog and read the explanation of the experiment. Choose <strong>Play</strong> (<em>Jogar</em>) to continue. The demonstration described here uses synthetic data, as explained above.</p>
	<p>The page moves to the game area while the request is being processed. Follow the status indicator: the game starts only when the backend confirms the session. If the service reports an error or an unavailable configuration, review that message before trying again.</p>
	{% include software-figure.html folder="quantum-battleship" file="qubat02.png" alt="Participation dialog with a demonstration player name and experiment explanation" caption="Enter a player name and confirm participation before the match begins." %}
</section>

<section id="turn">
	<div class="step-heading"><span class="step-number">03</span><h3>Attack by coordinates</h3></div>
	<p>The player board shows your fleet and the computer's attacks. The opponent board records your attempts, while the fleet panels track ship status. The turn highlight identifies which side is acting.</p>
	<p>With hard mode enabled, watch the <strong>classical chip panel</strong> as well as the quantum circuit: it identifies when the opponent is using the follow-up search. Both kinds of attack count toward the battle result, but classical search attacks are excluded from the quantum-randomness charts so that strategy is not mistaken for random sampling.</p>
	<p>When it is your turn, enter a coordinate such as <code>A3</code> and choose <strong>Attack</strong>. The letter identifies the row and the number the column. Wait for the result and the opponent's response; the game determines when you may attack again. Continue until one fleet is sunk, or use <strong>End match</strong> to leave the session.</p>
	{% include software-figure.html folder="quantum-battleship" file="qubat03.png" alt="Demonstration game with circuit, player turn highlight, coordinate input and two boards" caption="Synthetic demonstration: the circuit, turn indicator and boards connect each move to its source and result." %}
</section>

<section id="finish">
	<div class="step-heading"><span class="step-number">04</span><h3>Keep the match record</h3></div>
	<p>A completed battle opens a <strong>Match record</strong> with the outcome, player name, hardware association, data source, duration and score. It also presents both sides' move statistics, final boards, the circuit and the available measurement analysis.</p>
	<p>Choose <strong>Download PNG certificate</strong> for a visual record or <strong>Download JSON data</strong> for the structured result. The certificate documents the match; it is not a certificate of quantum randomness. Use <strong>New match</strong> to return to play. The header's <strong>Leaderboard</strong> opens the player ranking.</p>
	{% include software-figure.html folder="quantum-battleship" file="qubat04.png" alt="Demonstration match record with outcome, score, statistics, final boards and download controls" caption="Illustrative completed record with synthetic data; PNG and JSON downloads preserve the match information." %}
</section>

<section id="statistics">
	<div class="step-heading"><span class="step-number">05</span><h3>Compare the observed distributions</h3></div>
	<p>Open <strong>Analytics</strong> in the game header. Select a <strong>Computer</strong> and a <strong>Board</strong> size, or combine all board sizes. The page aggregates archived quantum-source attacks and excludes classical search attacks. Expand the source matches to inspect which records contribute to the sample.</p>
	<p>For a single board size, inspect Hamming weight, the frequency of bit 1, entropy per qubit and observed cell frequencies. The combined view uses normalized positions and size-aware baselines so that different board sizes can be compared. The summary reports sample counts and empirical entropy, including empirical min-entropy.</p>
	{% include software-figure.html folder="quantum-battleship" file="qubat05.png" alt="Demonstration analytics with board filters, empirical metrics, four charts and a source match" caption="Illustrative analysis of 319 synthetic samples; these charts are not measurements from a physical processor." %}
	<aside class="guide-callout"><strong>Observation is not certification.</strong> Entropy and frequency charts describe the available sample. XEB, sample timing (tQC) and certified min-entropy require protocol-specific evidence that these game records do not provide. The interface marks those quantities unavailable rather than claiming a result. Small samples, repeated values and synthetic caches must be considered when interpreting any chart.</aside>
</section>

<section id="architecture">
	<h3>From a move to a reusable observation</h3>
	<p>The browser sends game actions to an HTTP API backed by AWS Lambda. DynamoDB stores active sessions; S3 stores reusable measurement caches, completed match records and player summaries. The analytics endpoint reads archived observations, while the frontend renders the game, ranking and statistical views.</p>
	<p>This structure keeps the educational interaction and the data trail connected: a move belongs to a match, a match identifies its configuration and source, and the resulting observations can be revisited in the analysis.</p>
</section>

<footer class="guide-footer">Explore the project: <a href="https://quantum-computing-research.github.io/Batalha-Naval-Quantica">Play Quantum Battleship</a> · <a href="https://quantum-computing-research.github.io/Batalha-Naval-Quantica/analytics.html">Open analytics</a> · <a href="https://github.com/quantum-computing-research/Batalha-Naval-Quantica">Source code</a>. Scientific context: <a href="https://www.nature.com/articles/s41586-025-08737-1">Nature randomness paper</a>.</footer>
</div>
