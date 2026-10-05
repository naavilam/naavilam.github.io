---
layout: post
title:  "Quantum Battleship"
description: "Challenge real quantum computers in Battleship."
type: card-dated
date:   2025-04-11
image: batalha-naval-quantica.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-05
tag: Game
author: Nara Avila
card: card-1
repo: quantum-computing-research/Batalha-Naval-Quantica
live_url: https://quantum-computing-research.github.io/Batalha-Naval-Quantica
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-qubat">
<header class="guide-hero"><span class="eyebrow">Mission briefing</span><h2>A battle with a quantum twist</h2><p class="lead">Quantum Battleship combines a familiar strategy game with an experiment in random number generation. Configure your opponent, enter your player name and attack by coordinates while the computer responds. A completed battle provides a starting point for exploring how the selected quantum service produces random choices and for examining the available statistical charts.</p></header>
<nav class="guide-nav" aria-label="Guide sections"><a href="{{ page.url | relative_url }}#backend">Backend</a><a href="{{ page.url | relative_url }}#player">Player</a><a href="{{ page.url | relative_url }}#turn">Play</a><a href="{{ page.url | relative_url }}#finish">Finish</a><a href="{{ page.url | relative_url }}#statistics">Statistics</a></nav>
<div class="guide-grid">
<div class="guide-card"><h4>Mission</h4><p>Play a complete battle against the computer.</p></div>
<div class="guide-card"><h4>Experiment</h4><p>Observe the random choices used by the opponent.</p></div>
<div class="guide-card"><h4>Debrief</h4><p>Explore the statistical analysis after playing.</p></div></div>
<section id="backend"><div class="step-heading"><span class="step-number">01</span><h3>Choose your opponent’s backend</h3></div><p>Browse the <strong>AWS backend</strong> carousel with the arrow controls and select the backend offered by the game. Then choose the board size and number of ships before starting. Available hardware and simulators depend on the deployed service; use the option actually shown by your session.</p>{% include software-figure.html folder="quantum-battleship" file="qubat01.png" alt="AWS backend carousel and game configuration" caption="Choose the opponent backend, board size and fleet size." %}</section>

<section id="player"><div class="step-heading"><span class="step-number">02</span><h3>Introduce yourself and launch the battle</h3></div><p>Click <strong>Start game</strong> (<em>Iniciar Jogo</em>). In the welcome dialog, enter your player name and read the experiment explanation. Click <strong>Play</strong> (<em>Jogar</em>) to continue. Follow the status bar; if the service is occupied, use the waiting queue when that control becomes available.</p>{% include software-figure.html folder="quantum-battleship" file="qubat02.png" alt="Player name and experiment consent dialog" caption="Enter your name and confirm participation to begin." %}</section>

<section id="turn"><div class="step-heading"><span class="step-number">03</span><h3>Make your move</h3></div><p>Watch the turn indicator and the two boards. When it is your turn, type a coordinate such as <code>A5</code> into the move field and click <strong>Attack</strong> (<em>Atacar</em>). Wait for the attack result and the computer response before making the next move. Continue until the battle reaches its final result.</p>{% include software-figure.html folder="quantum-battleship" file="qubat03.png" alt="Player board, opponent board and coordinate attack field" caption="A coordinate becomes a move; the status display tells you when to play again." %}</section>

<section id="finish"><div class="step-heading"><span class="step-number">04</span><h3>Read the final message</h3></div><p>At completion, an overlay headed <strong>End of game</strong> (<em>Fim de Jogo</em>) displays the result message. Read the outcome before clicking <strong>End game</strong> (<em>Encerrar Jogo</em>), which closes the session and reloads the page.</p>{% include software-figure.html folder="quantum-battleship" file="qubat04.png" alt="End-of-game overlay showing the battle outcome" caption="The final message closes the play sequence." %}</section>

<section id="statistics"><div class="step-heading"><span class="step-number">05</span><h3>Turn the battle into a statistical question</h3></div><p>Open <strong>Analysis / Charts</strong> (<em>Análise / Gráficos</em>) to reach the analytics page. Select <strong>Hardware</strong>, adjust <strong>Shots</strong>, and click <strong>Reload</strong> (<em>Recarregar</em>) to request the displayed analysis. Read the Hamming-weight distribution, per-qubit frequency of bit 1, autocorrelation for lags 1–20, per-qubit entropy and the summary. Compare configurations using the hardware and sample controls. This page is the statistical report interface; save a browser printout or screenshots if you need a shareable copy.</p>{% include software-figure.html folder="quantum-battleship" file="qubat05.png" alt="Analytics page with hardware, shots and charts" caption="Inspect the available statistics using the hardware and sample controls." %}</section>
<aside class="guide-callout">Hardware information cards describe possible providers. The backend actually used for a match is determined by the deployed game service. A statistical chart is evidence to inspect, rather than a guarantee that a sample is perfectly random.</aside>
<footer class="guide-footer">Source documentation: <a href="https://quantum-computing-research.github.io/Batalha-Naval-Quantica">Live game</a> · <a href="https://quantum-computing-research.github.io/Batalha-Naval-Quantica/analytics.html">Analytics interface</a> · <a href="https://github.com/quantum-computing-research/Batalha-Naval-Quantica">Repository</a>. Interface labels may appear in Portuguese; this guide provides their English meaning.</footer>
</div>
