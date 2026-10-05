---
layout: post
title:  "GitHub Release and Milestone CLI"
description: "Release and milestone workflow for GitHub repositories. Automate and manage releases, milestones, and development cycles using a simple and intuitive interface with the GitHub CLI."
date:   2025-12-12
type: card-img-top
image: github-version-control.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-05
tag: Automation
author: Nara Avila
card: card-3
repo: automation-scripting/github-version-control
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-gitvc">
<header class="guide-hero"><span class="eyebrow">The delivery workshop</span><h2>Give every delivery a history</h2><p class="lead">GitHub Version Control is a Zsh workflow for planning work in GitHub Projects and recording deliveries with Git tags and GitHub Releases. Its rel commands connect issues, development lines and published versions so you can see what is evolving and what has shipped. Git still records your code changes; this module organizes the planning and release cycle around them.</p></header>
<nav class="guide-nav" aria-label="Guide sections"><a href="#setup">Initialize</a><a href="#tasks">Tasks</a><a href="#pending">Pending work</a><a href="#milestone">Patch / milestone</a><a href="#minor">Minor</a><a href="#major">Major</a></nav>
<ol class="guide-flow"><li>Open a development line</li><li>Create and track tasks</li><li>Tag a completed fix</li><li>Publish a release</li></ol>

<section id="setup"><div class="step-heading"><span class="step-number">01</span><h3>Connect a repository to the workflow</h3></div><p>Use a Zsh shell with <code>git</code>, the GitHub CLI (<code>gh</code>) and <code>jq</code> installed. Authenticate with an account that can manage the repository and its Projects. Clone the module, load its functions, then enter the local checkout of the GitHub project you want to manage.</p>{% include software-figure.html folder="github-version-control" file="gitvc01.png" alt="Zsh setup and GitHub repository context" caption="Load the module, authenticate and enter the target repository." %}</section>
<pre><code>gh auth login
gh auth refresh -s project
git clone https://github.com/automation-scripting/github-version-control.git &quot;$HOME/github-version-control&quot;

source &quot;$HOME/github-version-control/rel/rel-lib.zsh&quot;
source &quot;$HOME/github-version-control/rel/rel-release.zsh&quot;
source &quot;$HOME/github-version-control/rel/rel-set-item-status.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-init.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-todo.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-set-item-status.zsh&quot;
source &quot;$HOME/github-version-control/rel/rel.zsh&quot;

cd /path/to/your/github-project
gh repo view
rel init &quot;Prepare the first development cycle&quot;</code></pre>

<section id="tasks"><div class="step-heading"><span class="step-number">02</span><h3>Write the work as actionable tasks</h3></div><p><code>rel init</code> creates feature issues and adds them to the active development line. Separate task titles with <code>--</code>. Use <code>rel fix</code> for fixes. The workflow reuses a linked open Project named <code>vX.Y.x</code>, or initializes a development line when needed.</p>{% include software-figure.html folder="github-version-control" file="gitvc02.png" alt="Feature issues added to the active GitHub Project" caption="One task per issue, grouped in a versioned development line." %}</section>
<pre><code>rel init &quot;Add search&quot; -- &quot;Document the API&quot;
rel fix &quot;Correct the export filename&quot;
rel progress 12
rel done 12</code></pre>

<section id="pending"><div class="step-heading"><span class="step-number">03</span><h3>See what remains to be done</h3></div><p>Run the standalone <code>todo</code> function to display the active development line and its task statuses. Open the linked GitHub Project to inspect the board. To put a particular issue back into Todo, use <code>rel todo 12</code>; this changes its status rather than listing tasks.</p>{% include software-figure.html folder="github-version-control" file="gitvc03.png" alt="Terminal task overview and GitHub Project board" caption="Keep pending work visible throughout the development cycle." %}</section>
<pre><code>todo
rel todo 12</code></pre>

<section id="milestone"><div class="step-heading"><span class="step-number">04</span><h3>Record a completed issue with a patch tag</h3></div><p>In this module, a development “milestone” is represented by a GitHub Project, while an issue delivery is recorded with <code>rel p</code>. Commit and push the intended changes to the default branch before tagging. The command creates the next patch tag, tries to mark the issue Done and comments on the issue with the tag. It does not create a GitHub Release.</p>{% include software-figure.html folder="github-version-control" file="gitvc04.png" alt="Patch tag and linked issue delivery comment" caption="An issue receives a traceable delivery point." %}</section>
<pre><code>rel p 12</code></pre>

<section id="minor"><div class="step-heading"><span class="step-number">05</span><h3>Publish the next minor release</h3></div><p>Review the completed work, push the intended code and run <code>rel m</code>. The command builds release notes from the Project, publishes a short tag such as <code>v0.1</code>, renames the current Project to the released version and closes it. If unfinished work remains, it moves the backlog to the next development line.</p>{% include software-figure.html folder="github-version-control" file="gitvc05.png" alt="Minor GitHub Release and next development line" caption="Completed work becomes a release; the remaining backlog continues in the next line." %}</section>
<pre><code>rel m</code></pre>

<section id="major"><div class="step-heading"><span class="step-number">06</span><h3>Open a new major chapter</h3></div><p>Review the scope of the transition and run <code>rel M</code> with an uppercase M. The command publishes a tag such as <code>v1.0.0</code>, renames and closes the current Project, marks all its items Done and may open the next maintenance line.</p>{% include software-figure.html folder="github-version-control" file="gitvc06.png" alt="Major release and closed project" caption="A major publication starts a new version line." %}</section>
<pre><code>rel M</code></pre>
<aside class="guide-callout"><strong>Before a major release:</strong> reconcile unfinished tasks first. The current implementation marks every item Done, so this command changes the planning state as well as publishing the release. Release tags target the remote default branch HEAD.</aside>
<div class="table-scroll"><table class="guide-table"><thead><tr><th scope="col">Action</th><th scope="col">Command</th><th scope="col">Result</th></tr></thead><tbody><tr><td>Feature tasks</td><td><code>rel init "Task"</code></td><td>Issues in an active Project</td></tr><tr><td>List work</td><td><code>todo</code></td><td>Terminal status overview</td></tr><tr><td>Issue delivery</td><td><code>rel p 12</code></td><td>Patch tag; issue traceability</td></tr><tr><td>Minor release</td><td><code>rel m</code></td><td>GitHub Release; backlog transition</td></tr><tr><td>Major release</td><td><code>rel M</code></td><td>GitHub Release; all current items marked Done</td></tr></tbody></table>
</div>
<footer class="guide-footer">Source documentation: <a href="https://github.com/automation-scripting/github-version-control">README and module source</a>. Interface labels may appear in Portuguese; this guide provides their English meaning.</footer>
</div>
