---
layout: post
title:  "Molecular Symmetry"
description: "Explore molecular geometry in 3D, investigate symmetry operations and export TeX or PDF reports."
type: card-dated
date:   2025-06-16
image: molecular-symmetry.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-11
tag: Application
author: Nara Avila
card: card-2
repo: application-vault/simetria-molecular
live_url: https://application-vault.github.io/simetria-molecular
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-mol">
<header class="guide-hero">
	<span class="eyebrow">Geometry, visualization and group theory</span>
	<h2>Molecular Symmetry</h2>
	<p class="lead">Explore a molecule as both a spatial structure and a mathematical object. Load XYZ coordinates, inspect the geometry in an interactive 3D view and request a symmetry report that connects group identification, atom permutations and the composition of operations.</p>
</header>
<nav class="guide-nav" aria-label="Guide sections">
	<a href="{{ page.url | relative_url }}#idea">The idea</a>
	<a href="{{ page.url | relative_url }}#system">Molecules</a>
	<a href="{{ page.url | relative_url }}#viewer">3D view</a>
	<a href="{{ page.url | relative_url }}#appearance">Display</a>
	<a href="{{ page.url | relative_url }}#analysis">Analysis</a>
	<a href="{{ page.url | relative_url }}#report">Report</a>
	<a href="{{ page.url | relative_url }}#custom">Custom XYZ</a>
</nav>
<p>The screenshots use the English interface and <strong>Fe(III) tetrathiolate</strong>, a 97-atom coordination complex, as the main example. Choose <strong>PT</strong>, <strong>EN</strong> or <strong>ZH</strong> in the header to change the interface language. The preference is saved in your browser; molecular identifiers, coordinates and backend-generated TeX/PDF content remain unchanged.</p>
<p>The molecular geometry comes from the project's <code>feiii_tetrathiolate.xyz</code> file and is loaded locally for these screenshots. The report screenshot contains an illustrative TeX example to demonstrate the interface, not a live backend analysis result.</p>

<section id="idea">
	<h3>From molecular shape to symmetry operations</h3>
	<p>Developed in the context of the graduate course <strong>PGF5261, Group Theory Applied to Solids and Molecules</strong>, the project brings visual exploration and algebraic analysis into the same workspace. Its purpose is to make the connection between a molecular geometry and its symmetry group easier to investigate, discuss and document.</p>
	<p>A symmetry operation leaves the structure indistinguishable from its original arrangement: equivalent atoms may exchange positions, but the molecular geometry is preserved. Rotations and reflections provide familiar examples. The report relates these operations to atom permutations and tables describing how operations combine.</p>
	<p>The Fe(III) tetrathiolate example makes that investigation tangible: locate the central iron atom, its four sulfur donors and the surrounding organic ligands. Compare the full ligand arrangement, not just the coordination center, before proposing a symmetry operation. A point-group assignment must be checked against the supplied coordinates rather than inferred from the compound's name.</p>
	<aside class="guide-callout"><strong>A geometry-based investigation, not a quantum-chemistry calculation.</strong> The current controls visualize XYZ structures and request symmetry analyses. The viewport mentions orbitals and molecular electrostatic potential (MEP), but does not offer those calculations. Editing coordinates updates the geometry; it does not optimize the molecule's energy or relax its structure.</aside>
</section>

<section id="system">
	<div class="step-heading"><span class="step-number">01</span><h3>Choose a molecular system</h3></div>
	<p>Open the application and use <strong>Choose a molecule</strong> to select a structure from the available catalog. The <strong>Input / Coordinates</strong> field fills with its XYZ data, and the molecular viewer updates automatically. The catalog is loaded from the backend, so its contents depend on the deployed service.</p>
	<p>The workspace separates three tasks: selecting or entering the molecule, inspecting its geometry and choosing an analysis. Start with a familiar structure and check the atom count and coordinates before interpreting its symmetry.</p>
	{% include software-figure.html folder="molecular-symmetry" file="molsym01.png" alt="English Molecular Symmetry workspace with Fe III tetrathiolate selected and its 97-atom XYZ structure" caption="Fe(III) tetrathiolate: inspect the original 97-atom geometry alongside its XYZ coordinates." %}
</section>

<section id="viewer">
	<div class="step-heading"><span class="step-number">02</span><h3>Explore the geometry in 3D</h3></div>
	<p>Choose <strong>Graphics</strong> to access the display controls. Rotate and zoom the model to inspect its arrangement from different angles. Try locating equivalent atoms, a possible rotation axis or a mirror plane before requesting the algebraic analysis.</p>
	<p>Turn off <strong>Automatic rotation</strong> to hold an orientation while inspecting it or taking a screenshot. <strong>Reset view</strong> refits the model and stops automatic rotation. These actions change the presentation, not the XYZ coordinates submitted for analysis.</p>
	{% include software-figure.html folder="molecular-symmetry" file="molsym02.png" alt="Fe III tetrathiolate displayed as a Ball and Stick model with an oblique view of its metal center and ligands" caption="An oblique Ball & Stick view reveals the metal center and surrounding ligands without changing the geometry." %}
</section>

<section id="appearance">
	<div class="step-heading"><span class="step-number">03</span><h3>Adjust the molecular display</h3></div>
	<ul>
		<li><strong>Style:</strong> choose Ball &amp; Stick, Sticks, Spheres or Lines. Ball &amp; Stick makes atom positions and bonds easy to compare.</li>
		<li><strong>Color palette:</strong> use element colors, Pastel, Vibrant or Monochrome. Consistent colors help when comparing figures.</li>
		<li><strong>Display:</strong> show or hide hydrogens, enable atom labels, toggle automatic rotation and change the viewer background.</li>
	</ul>
	<p>The header's theme button changes the application theme. <strong>Dark background</strong> is a separate control for the molecular viewport. Hiding hydrogen atoms changes only what is displayed; it does not remove them from the input used by the backend.</p>
	{% include software-figure.html folder="molecular-symmetry" file="molsym03.png" alt="English display controls and Fe III tetrathiolate in default element colors with hydrogens hidden" caption="Hide hydrogens and use element colors to make the iron, sulfur donors and ligand framework easier to inspect." %}
</section>

<section id="analysis">
	<div class="step-heading"><span class="step-number">04</span><h3>Choose the scope of the symmetry report</h3></div>
	<p>Switch from <strong>Graphics</strong> to <strong>Symmetry</strong>. Select the analyses you want and choose <strong>Analyze symmetry</strong>. The application sends the current XYZ contents and the selected analysis flags to the backend; the processing indicator remains visible until the request completes.</p>
	<div class="table-scroll">
		<table class="guide-table">
			<thead><tr><th scope="col">Analysis</th><th scope="col">What to inspect</th></tr></thead>
			<tbody>
				<tr><td>Group identification</td><td>The symmetry group identified for the supplied structure.</td></tr>
				<tr><td>Permutations</td><td>How each operation maps atoms onto equivalent positions.</td></tr>
				<tr><td>Multiplication table</td><td>How pairs of symmetry operations compose.</td></tr>
				<tr><td>Conjugacy classes</td><td>How operations are grouped under conjugation.</td></tr>
			</tbody>
		</table>
	</div>
	{% include software-figure.html folder="molecular-symmetry" file="molsym04.png" alt="English Symmetry mode showing selectable group, permutation, multiplication and conjugacy analyses" caption="Select the report contents before submitting the molecular coordinates." %}
	<aside class="guide-callout"><strong>Available versus upcoming.</strong> Characters, Eigenvalues, Subgroups, Cyclic and Abelian remain disabled and marked Coming soon. A checkbox in that list is not evidence that its analysis is implemented. The report also depends on the coordinates and the capabilities of the deployed backend; distorted or incomplete structures should not be assumed to retain the ideal molecule's symmetry.</aside>
</section>

<section id="report">
	<div class="step-heading"><span class="step-number">05</span><h3>Reuse the TeX result or generate a PDF</h3></div>
	<p>The backend returns the report as TeX source in <strong>Result (.tex)</strong>. Choose <strong>Copy</strong> to place that source on the clipboard or <strong>Generate PDF</strong> to request its compilation. The PDF opens in another tab, where the browser provides save and print actions. Allow pop-ups if the report tab is blocked.</p>
	<p>The interface language does not rewrite the report. Its scientific notation, text and formatting come from the backend. If analysis or compilation fails, read the displayed error and check your input; preserve any available TeX so it can be inspected or compiled separately.</p>
	{% include software-figure.html folder="molecular-symmetry" file="molsym05.png" alt="English report panel displaying illustrative Fe III tetrathiolate TeX source with Copy and Generate PDF buttons" caption="Illustrative TeX example, not a live analysis result: Copy reuses the source and Generate PDF requests compilation." %}
</section>

<section id="custom">
	<div class="step-heading"><span class="step-number">06</span><h3>Paste your own XYZ structure</h3></div>
	<p>Select <strong>Other (specify)</strong> to unlock the coordinate field. Open your <code>.xyz</code> file in a text editor and paste its <strong>complete contents</strong>, not its filename or path. The first line is the number of atoms, the second is a comment, and the remaining lines contain an element symbol followed by three Cartesian coordinates.</p>
	<p>Keep the comment line even when it is blank, use decimal points in the numeric fields and check that the declared atom count matches the coordinate rows. The viewer updates as you edit. Inspect the structure before submitting it through the same Symmetry workflow.</p>
	{% include software-figure.html folder="molecular-symmetry" file="molsym06.png" alt="Other specify selected with the complete Fe III tetrathiolate XYZ file in the editable coordinate field" caption="The same 97-atom complex can be entered as custom XYZ, using the same viewer and report workflow." %}
	<details>
		<summary>A minimal XYZ example: water</summary>
		<p>This symmetric example uses coordinates in angstroms. The two hydrogens lie at equal distances from oxygen.</p>
		<pre><code>3
Water - coordinates in angstroms
O  0.0000  0.0000  0.0000
H  0.7586  0.0000  0.5043
H -0.7586  0.0000  0.5043</code></pre>
	</details>
</section>

<section id="architecture">
	<h3>One structure, two complementary views</h3>
	<p>The browser uses <strong>3Dmol.js</strong> to render the XYZ structure locally. The HTTP API supplies the molecule catalog and coordinates, receives the selected symmetry analyses and compiles TeX into PDF. Keeping visualization separate from analysis lets you inspect the structure without rerunning the mathematical report every time you change the camera or colors.</p>
</section>

<footer class="guide-footer">Explore the project: <a href="https://application-vault.github.io/simetria-molecular">Open Molecular Symmetry</a> · <a href="https://github.com/application-vault/simetria-molecular">Source code</a> · <a href="https://github.com/application-vault/simetria-molecular/tree/frontend">Frontend and controls</a>.</footer>
</div>
