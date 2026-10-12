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
<header class="guide-hero"><span class="eyebrow">The delivery workshop</span><h2>From an empty backlog to a published version</h2><p class="lead">GitHub Version Control is a Zsh module that connects GitHub issues, versioned Projects and release history. Start in a repository with no open development line, create the first task and grow the backlog. Deliver an issue with a patch tag, publish a minor release and prepare the next major version. Git records the code; this workflow connects that code to the work planned and shipped.</p></header>
<nav class="guide-nav" aria-label="Release workflow steps"><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#setup">1 · Inspect →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#first-task">2 · First task →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#tasks">3 · Backlog →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#pending">4 · Review →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#milestone">5 · Patch →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#minor">6 · Minor →</a><a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#major">7 · Major →</a></nav>
<aside class="guide-callout"><strong>One continuous example.</strong> Follow the fictional <code>example-lab/atlas-tools</code> repository on <code>main</code>. The module is already loaded, the repository is connected to GitHub, and your account can manage its issues, Projects and releases. The transcript illustrations follow the supplied sessions; abbreviated output and conceptual state summaries are labeled.</aside>
<section id="setup">
<div class="step-heading"><span class="step-number">01</span><h3>Inspect the repository before creating anything</h3></div>
<p>Run <code>todo</code> inside the target repository. A message saying no open development line was found means there is no linked open Project named <code>vX.Y.x</code>. It does not create a Project or modify the repository.</p>
{% include release-terminal.html example="gitvc01" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#first-task">Create the first task →</a>
</section>
<section id="first-task">
<div class="step-heading"><span class="step-number">02</span><h3>Let the first task open the development line</h3></div>
<p>Use <code>rel init</code> with an actionable task title. With no existing development line or version tags, the module creates and links <code>v0.0.x</code>, creates issue #1 and adds it to the Project. Run <code>todo</code> again to verify the result. Project number #19 is an example; GitHub assigns the actual number.</p>
{% include release-terminal.html example="gitvc-first" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#tasks">Add a fix and a feature →</a>
</section>
<section id="tasks">
<div class="step-heading"><span class="step-number">03</span><h3>Build a backlog around the same Project</h3></div>
<p>Use <code>rel fix</code> to register a fix and <code>rel init</code> to register another feature. Both commands reuse the open development line. For multiple tasks in one call, separate titles with <code>--</code>, for example <code>rel init "Add search" -- "Document the API"</code>.</p>
{% include release-terminal.html example="gitvc02" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#pending">Review pending work →</a>
</section>
<section id="pending">
<div class="step-heading"><span class="step-number">04</span><h3>Read the queue before choosing a delivery</h3></div>
<p>The standalone <code>todo</code> lists the development line and its items. Here #1 and #3 are feature tasks, while #2 is labeled FIX. Use <code>rel progress 1</code> to mark work in progress, <code>rel todo 1</code> to reset its status or <code>rel done 1</code> to mark it complete. Those commands update planning status; they do not commit or publish code.</p>
{% include release-terminal.html example="gitvc03" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#milestone">Deliver issue #1 →</a>
</section>
<section id="milestone">
<div class="step-heading"><span class="step-number">05</span><h3>Attach a patch tag to the first completed task</h3></div>
<p>Implement issue #1, commit it and push the intended code to the default branch. Then run <code>rel p 1</code>. The command creates the next patch tag at the remote default branch HEAD, attempts to mark the Project item Done and comments on the issue with the tag. It creates a tag rather than a GitHub Release. The development “milestone” in this module is the versioned Project.</p>
{% include release-terminal.html example="gitvc04" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#minor">Publish the minor version →</a>
</section>
<section id="minor">
<div class="step-heading"><span class="step-number">06</span><h3>Publish what shipped and carry the backlog forward</h3></div>
<p>Run <code>rel m</code> to publish <code>v0.1</code> with notes from the current Project. Completed issue #1 stays in the released Project. The command moves unfinished #2 and #3 to <code>v0.1.x</code> and closes the old Project. Run <code>todo</code> afterward to review the remaining work in the next development line.</p>
{% include release-terminal.html example="gitvc05" %}
<a class="btn btn-outline-secondary" href="{{ page.url | relative_url }}#major">Prepare the major version →</a>
</section>
<section id="major">
<div class="step-heading"><span class="step-number">07</span><h3>Finish the remaining work before a major release</h3></div>
<p>Implement and push issues #2 and #3, then mark them Done. Use uppercase <code>rel M</code> to publish <code>v1.0.0</code>, rename and close the current Project, and mark all its items Done. The module asks whether to open <code>v1.0.x</code>; that next line is optional. Reconcile unfinished work before this command because it marks every current item Done.</p>
{% include release-terminal.html example="gitvc06" %}

</section>
<details><summary>Command reference: why rel task shows help</summary>{% include release-terminal.html example="gitvc-help" %}</details>
<details><summary>Before this walkthrough: load the module in Zsh</summary><p>Install Git, GitHub CLI and jq, authenticate with repository and Project permissions, and load the functions from a local checkout of the module. Replace the final path with your own target repository. This setup block loads functions; it does not create tasks or releases.</p>
<div class="release-setup-code"><pre><code>gh auth login
gh auth refresh -s project
git clone https://github.com/automation-scripting/github-version-control.git &quot;$HOME/github-version-control&quot;

source &quot;$HOME/github-version-control/rel/rel-lib.zsh&quot;
source &quot;$HOME/github-version-control/rel/rel-release.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-init.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-todo.zsh&quot;
source &quot;$HOME/github-version-control/prj/prj-set-item-status.zsh&quot;
source &quot;$HOME/github-version-control/rel/rel.zsh&quot;

cd /path/to/your/github-project</code></pre></div></details>
<footer class="guide-footer">Source: <a href="https://github.com/automation-scripting/github-version-control">GitHub Version Control</a>. Commands were checked against the local module and the supplied terminal sessions on October 5, 2026. Examples do not execute commands or change repositories.</footer>
</div>
