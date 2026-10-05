---
layout: post
title:  "Literature Alert"
description: "A lightweight Python script that retrieves newly published papers from arXiv and posts them to a Discord channel."
date:   2026-01-10
type: card-img-top
image: literature-alert-bot.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-05
tag: Automation
author: Nara Avila
card: card-4
repo: automation-scripting/literature-alert-bot
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-lit">
<header class="guide-hero"><span class="eyebrow">Your research radar</span><h2>Let the papers come to you</h2><p class="lead">Literature Alerts is a Python runner that retrieves papers from arXiv using YAML topic queries and publishes them to Discord through webhooks. GitHub Actions runs the fetch on a schedule or on demand, while date filters and message modes shape the stream. The result is a configurable reading radar for research areas you want to follow.</p></header>
<nav class="guide-nav" aria-label="Guide sections"><a href="#topics">Topics</a><a href="#destination">Discord</a><a href="#schedule">Schedule</a><a href="#parameters">Parameters</a><a href="#report">Run report</a></nav>
<ol class="guide-flow"><li>arXiv query</li><li>Date filter</li><li>Discord destination</li><li>Execution report</li></ol>

<section id="topics"><div class="step-heading"><span class="step-number">01</span><h3>Create a stream for a research topic</h3></div><p>Fork the repository and create or edit a YAML file under <code>topics/</code>. Each entry identifies a research topic with an <code>id</code>, a display <code>title</code>, an <code>arxiv_url</code> query and a <code>webhook_env</code> destination variable. These are research streams defined by queries, rather than arXiv discussion threads. The runner consumes the query URL as supplied.</p>{% include software-figure.html folder="literature-alerts" file="lital01.png" alt="Topic YAML with arXiv query and destination variable" caption="A research stream is a query paired with a delivery destination." %}</section>
<pre><code>topics:
  - id: quantum
    title: &quot;Quantum Physics&quot;
    webhook_env: &quot;DISCORD_WEBHOOK_QUANTUM&quot;
    arxiv_url: &quot;https://export.arxiv.org/api/query?search_query=cat:quant-ph&amp;sortBy=submittedDate&amp;sortOrder=descending&amp;max_results=100&quot;</code></pre>

<section id="destination"><div class="step-heading"><span class="step-number">02</span><h3>Connect the topic to Discord</h3></div><p>In your Discord channel, open <strong>Settings → Integrations → New Webhook</strong> and copy its URL. In your GitHub repository, open <strong>Settings → Secrets and variables → Actions</strong> and create a repository secret for that URL. Expose the secret as the environment variable named by <code>webhook_env</code> in the workflow step.</p>{% include software-figure.html folder="literature-alerts" file="lital02.png" alt="Discord webhook and corresponding GitHub Actions secret" caption="The YAML destination name must match the environment variable in the workflow." %}</section>
<pre><code>env:
  DISCORD_WEBHOOK_QUANTUM: {% raw %}${{ secrets.DISCORD_WEBHOOK_QUANTUM }}{% endraw %}
run: python runner.py topics/quantum.yml</code></pre>

<section id="schedule"><div class="step-heading"><span class="step-number">03</span><h3>Choose when the fetch runs</h3></div><p>Edit <code>.github/workflows/check-new-papers.yml</code>. Its existing schedule is <code>0 8 * * *</code>: daily at 08:00 UTC, or 05:00 in São Paulo (UTC−3). For a daily run at 09:00 São Paulo time, use the example below. Commit the workflow to the default branch. You can also run it manually from Actions with the topic and time-frame inputs.</p>{% include software-figure.html folder="literature-alerts" file="lital03.png" alt="Scheduled workflow and manual run inputs" caption="Set the automation clock and keep a manual route for checking a topic." %}</section>{% raw %}<pre><code>on:
  schedule:
    - cron: &quot;0 12 * * *&quot;  # 09:00 São Paulo (UTC-3)
  workflow_dispatch:</code></pre>{% endraw %}
<section id="parameters"><div class="step-heading"><span class="step-number">04</span><h3>Tune the signal and the delivery pace</h3></div><div class="table-scroll"><table class="guide-table"><thead><tr><th scope="col">Environment variable</th><th scope="col">Default</th><th scope="col">What it controls</th></tr></thead><tbody><tr><td>TIME_FRAME</td><td>1</td><td>Days of papers to include; use all to disable date filtering.</td></tr><tr><td>ONLY_TOPIC</td><td>all</td><td>Run only the matching topic id, or every topic.</td></tr><tr><td>MODE</td><td>auto</td><td>auto, per_paper or summary delivery.</td></tr><tr><td>REQUEST_TIMEOUT</td><td>20</td><td>HTTP timeout in seconds.</td></tr><tr><td>MAX_RETRIES_429</td><td>8</td><td>Extra attempts after Discord HTTP 429 rate limits.</td></tr><tr><td>POST_DELAY_SECONDS</td><td>0.4</td><td>Delay between individual paper posts.</td></tr><tr><td>MAX_POSTS_PER_TOPIC</td><td>0</td><td>Post cap after date filtering; 0 means no cap.</td></tr><tr><td>DISCORD_CHUNK_LIMIT</td><td>1800</td><td>Maximum summary chunk size.</td></tr><tr><td>SUMMARY_THRESHOLD</td><td>50</td><td>Force summary delivery above this paper count.</td></tr></tbody></table>
</div>{% include software-figure.html folder="literature-alerts" file="lital04.png" alt="Runner environment parameters in the workflow" caption="Tune date coverage, message format and rate-limit handling." %}</section>
<pre><code>env:
  TIME_FRAME: &quot;7&quot;
  MODE: &quot;summary&quot;
  MAX_RETRIES_429: &quot;5&quot;
  REQUEST_TIMEOUT: &quot;30&quot;
  POST_DELAY_SECONDS: &quot;0.8&quot;</code></pre>
<aside class="guide-callout"><code>MAX_RETRIES_429</code> retries Discord rate limits using the server’s retry delay. It is not a general retry count for every failed arXiv fetch or network error. Other failures need inspection in the run logs.</aside>

<section id="report"><div class="step-heading"><span class="step-number">05</span><h3>Read the report before expanding the stream</h3></div><p>When adding a topic file, add a workflow step that binds its required webhook variables and passes the file to <code>runner.py</code>. Run the workflow manually, then open <strong>Actions → arXiv → Discord → run details</strong>. Check fetched and filtered article counts, posted messages and errors. Confirm delivery in Discord before expanding the queries.</p>{% include software-figure.html folder="literature-alerts" file="lital05.png" alt="Actions execution report and delivered Discord papers" caption="Verify both the fetch report and the destination messages." %}</section>
<footer class="guide-footer">Source documentation: <a href="https://github.com/automation-scripting/literature-alert-bot">README and runner</a> · <a href="https://github.com/automation-scripting/literature-alert-bot/blob/main/.github/workflows/check-new-papers.yml">Scheduled workflow</a>. Interface labels may appear in Portuguese; this guide provides their English meaning.</footer>
</div>
