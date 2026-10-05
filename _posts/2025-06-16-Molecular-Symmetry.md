---
layout: post
title:  "Molecular Symmetry"
description: "Parse .xyz files and generate molecular symmetry reports."
type: card-dated
date:   2025-06-16
image: molecular-symmetry.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-05
tag: Application
author: Nara Avila
card: card-2
repo: application-vault/simetria-molecular
live_url: https://application-vault.github.io/simetria-molecular
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-mol">
<header class="guide-hero"><span class="eyebrow">The molecular laboratory</span><h2>From geometry to symmetry</h2><p class="lead">Molecular Symmetry turns XYZ coordinates into an interactive molecular view and a symmetry report. Developed in the context of the graduate course PGF5261, Group Theory Applied to Solids and Molecules, it connects visual exploration with group identification, atom permutations and operation tables. Start with a built-in system or paste your own structure, then choose the analyses and export the results.</p></header>
<nav class="guide-nav" aria-label="Guide sections"><a href="#system">System</a><a href="#viewer">3D view</a><a href="#appearance">Appearance</a><a href="#analysis">Analysis</a><a href="#report">Report</a><a href="#custom">Custom XYZ</a></nav>
<ol class="guide-flow"><li>Select a system</li><li>Explore its geometry</li><li>Choose analyses</li><li>Export the report</li></ol>

<section id="system"><div class="step-heading"><span class="step-number">01</span><h3>Start with a molecular system</h3></div><p>Open the application and choose a molecule from the system selector. Its XYZ coordinates populate the coordinate field and the 3D view updates automatically. Begin with a familiar molecule so you can connect its geometry to its symmetry.</p>{% include software-figure.html folder="molecular-symmetry" file="molsym01.png" alt="Molecule selector and XYZ coordinate panel" caption="Choose a built-in system and inspect the coordinates loaded for it." %}</section>

<section id="viewer"><div class="step-heading"><span class="step-number">02</span><h3>Make the geometry readable</h3></div><p>Use the <strong>Graphical</strong> mode (<em>Gráfico</em>) to explore the molecule in the 3D viewer. Rotate and zoom to inspect bonds and equivalent atoms. Use <strong>Reset view</strong> to restore a useful starting orientation.</p>{% include software-figure.html folder="molecular-symmetry" file="molsym02.png" alt="Interactive 3D molecular view" caption="Inspect the molecule from several angles before choosing the analysis." %}</section>

<section id="appearance"><div class="step-heading"><span class="step-number">03</span><h3>Build the view you need</h3></div><div class="guide-grid">
<div class="guide-card"><h4>Representation</h4><p>Choose Ball & Stick, sticks, spheres, or lines. Ball & Stick makes atom positions and bonds easy to compare.</p></div>
<div class="guide-card"><h4>Color palette</h4><p>Choose element colors, pastel, vibrant, or monochrome. Use the same palette across figures for a consistent report.</p></div>
<div class="guide-card"><h4>Display controls</h4><p>Show or hide hydrogens and atom labels; toggle automatic rotation and the dark background. Stop rotation for screenshots.</p></div></div>{% include software-figure.html folder="molecular-symmetry" file="molsym03.png" alt="Representation, palette and display controls" caption="A single geometry, presented with the visual settings that suit your explanation." %}</section>

<section id="analysis"><div class="step-heading"><span class="step-number">04</span><h3>Choose what the report explains</h3></div><p>Switch to <strong>Symmetry</strong> (<em>Simetria</em>). Select the analyses you need, then click <strong>Analyze symmetry</strong> (<em>Analisar Simetria</em>) and wait for the result.</p>{% include software-figure.html folder="molecular-symmetry" file="molsym04.png" alt="Symmetry analysis selection panel" caption="Select the scope before submitting the analysis." %}</section>
<div class="table-scroll"><table class="guide-table"><thead><tr><th scope="col">Analysis</th><th scope="col">Purpose</th></tr></thead><tbody><tr><td>Group identification</td><td>Identify the molecular symmetry group.</td></tr><tr><td>Permutations</td><td>Inspect how symmetry operations rearrange atoms.</td></tr><tr><td>Multiplication table</td><td>See how operations compose.</td></tr><tr><td>Conjugacy classes</td><td>Group operations into conjugacy classes.</td></tr></tbody></table>
</div><aside class="guide-callout">The interface also lists character tables, eigenvalues, subgroups, cyclic and abelian analyses as disabled, upcoming options.</aside>

<section id="report"><div class="step-heading"><span class="step-number">05</span><h3>From result to a shareable document</h3></div><p>The text output is TeX. After the analysis returns, use <strong>Copy TeX</strong> to reuse it in your writing or <strong>Generate PDF</strong> to compile the current result. The PDF opens in a browser tab, where you can save or print it. If compilation fails, retain the TeX and check the error shown by the application.</p>{% include software-figure.html folder="molecular-symmetry" file="molsym05.png" alt="TeX result and PDF export actions" caption="Copy the source or generate a PDF from the returned report." %}</section>

<section id="custom"><div class="step-heading"><span class="step-number">06</span><h3>Bring your own molecule</h3></div><p>Choose <strong>Other (specify)</strong> (<em>Outra (especifique)</em>) to unlock the coordinate field. Open your <code>.xyz</code> file in a text editor and paste its <strong>full contents</strong> into the field, rather than its filename or path. The viewer updates as the coordinates change. Inspect the structure, select the analyses, and run the same report workflow.</p>{% include software-figure.html folder="molecular-symmetry" file="molsym06.png" alt="Custom XYZ pasted into the editable coordinate field" caption="Your own molecular structure enters through the same analysis pipeline." %}</section>
<details><summary>A minimal XYZ example: water</summary><p>The first line is the atom count, the second is a comment, and the remaining lines contain the element symbol and three Cartesian coordinates. Keep the comment line even if it is blank.</p><pre><code>3
Water — coordinates in angstroms
O  0.0000  0.0000  0.0000
H  0.7586  0.0000  0.5043
H -0.7586  0.0000  0.5043</code></pre>
</details>
<footer class="guide-footer">Source documentation: <a href="https://github.com/application-vault/simetria-molecular/tree/frontend">Frontend and controls</a> · <a href="https://application-vault.github.io/simetria-molecular">Open application</a>. Interface labels may appear in Portuguese; this guide provides their English meaning.</footer>
</div>
