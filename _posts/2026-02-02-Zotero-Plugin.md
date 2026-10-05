---
layout: post
title:  "Zotero Mirroring Plugin"
description: "A Zotero plugin that mirrors the hierarchical library structure onto the filesystem."
date:   2026-02-02
type: card-img-top
image: zotero-plugin.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-05
tag: Plugin
author: Nara Avila
card: card-5
repo: automation-scripting/zotero-mirroring-plugin
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-zotero">
<header class="guide-hero"><span class="eyebrow">The library companion</span><h2>Let your library become a folder tree</h2><p class="lead">FS Mirror is a Zotero plugin that mirrors the collection hierarchy onto the filesystem and maintains linked PDF attachments. It connects the way you organize references in Zotero with the way you navigate files on disk. Install the packaged extension, choose a mirror root and use the collection context menu to reconcile an existing library tree.</p></header>
<nav class="guide-nav" aria-label="Guide sections"><a href="{{ page.url | relative_url }}#download">Download</a><a href="{{ page.url | relative_url }}#install">Install</a><a href="{{ page.url | relative_url }}#configure">Configure</a><a href="{{ page.url | relative_url }}#sanitize">Sanitize</a><a href="{{ page.url | relative_url }}#features">Features</a></nav>
<div class="guide-grid">
<div class="guide-card"><h4>Library</h4><p>Organize references into Zotero collections.</p></div>
<div class="guide-card"><h4>Filesystem</h4><p>Mirror that hierarchy into folders and linked attachments.</p></div>
<div class="guide-card"><h4>Maintenance</h4><p>Reconcile a selected collection with its filesystem tree.</p></div></div>
<section id="download"><div class="step-heading"><span class="step-number">01</span><h3>Download the packaged release</h3></div><p>Open the repository’s <strong>Releases</strong> page, choose a release compatible with your Zotero version, expand <strong>Assets</strong> and download its <code>.xpi</code> plugin package. The source archive is intended for development. If a release has no XPI asset, use a release that provides the packaged extension.</p>{% include software-figure.html folder="zotero-plugin" file="zoter01.png" alt="GitHub release assets with the XPI plugin package" caption="Download the installable package from release assets." %}</section>
<p><a class="btn btn-outline-secondary" href="https://github.com/automation-scripting/zotero-mirroring-plugin/releases">Browse releases</a></p>
<section id="install"><div class="step-heading"><span class="step-number">02</span><h3>Install it inside Zotero</h3></div><p>In Zotero, open <strong>Tools → Plugins</strong> (or <strong>Add-ons</strong>, depending on the version). Open the gear menu, choose <strong>Install Plugin From File…</strong>, select the downloaded XPI and confirm installation. Restart Zotero if prompted. Check that <strong>FS Mirror</strong> appears in the plugin list. The inspected manifest declares compatibility with Zotero 7 through 8.</p>{% include software-figure.html folder="zotero-plugin" file="zoter02.png" alt="Zotero plugin manager installing the downloaded XPI" caption="Install the package and verify that FS Mirror is enabled." %}</section>

<section id="configure"><div class="step-heading"><span class="step-number">03</span><h3>Choose the root of your mirrored library</h3></div><p>Set the filesystem destination before sanitizing a collection. The plugin reads <code>extensions.fs-mirror.rootDir</code> for the mirror root and <code>extensions.fs-mirror.logsDir</code> for its logs. If your release has no dedicated settings panel, use Zotero’s advanced Config Editor to locate and set those preferences. Choose a writable folder and inspect a small collection first.</p>{% include software-figure.html folder="zotero-plugin" file="zoter03.png" alt="Mirror root and log directory configuration" caption="Configure the destination where the library hierarchy will be mirrored." %}</section>
<div class="table-scroll"><table class="guide-table"><thead><tr><th scope="col">Preference</th><th scope="col">Purpose</th></tr></thead><tbody><tr><td>extensions.fs-mirror.rootDir</td><td>Root folder for the mirrored library.</td></tr><tr><td>extensions.fs-mirror.logsDir</td><td>Folder used for plugin logs.</td></tr><tr><td>extensions.fs-mirror.sanitizeRecursive</td><td>Include descendant collections; default true.</td></tr><tr><td>extensions.fs-mirror.safeTrashDirName</td><td>Internal recovery folder; default _FSMirror_Trash.</td></tr><tr><td>extensions.fs-mirror.unfiledFolder</td><td>Folder for items without a collection; default _FSMirror_Unfiled.</td></tr></tbody></table>
</div>
<section id="sanitize"><div class="step-heading"><span class="step-number">04</span><h3>Sanitize a collection from its context menu</h3></div><p>In Zotero’s collection tree, right-click the collection you want to reconcile and select <strong>FS Mirror: Sanitize this collection</strong>. This is the action referred to as “Sanear arquivos”. With recursive sanitizing enabled, the scan includes its child collections. Let the operation finish, then inspect the destination folders, linked PDFs and logs.</p>{% include software-figure.html folder="zotero-plugin" file="zoter04.png" alt="Collection context menu with the sanitize action" caption="Right-click a collection to reconcile its attachments and mirrored folders." %}</section>
<aside class="guide-callout">Sanitizing can reorganize attachments: the implementation copies stored PDFs into planned filesystem paths, creates linked attachments, transfers annotations and archives/removes the superseded stored attachments. Back up the library and attachments before the first large migration.</aside>

<section id="features"><div class="step-heading"><span class="step-number">05</span><h3>A library you can navigate in two places</h3></div><div class="guide-grid">
<div class="guide-card"><h4>Collection hierarchy</h4><p>Collection names and keys determine the mirrored folder tree, giving references an organized filesystem location.</p></div>
<div class="guide-card"><h4>Attachment reconciliation</h4><p>Sanitizing distinguishes stored and linked PDFs and reconciles them with their planned destination paths.</p></div>
<div class="guide-card"><h4>Ongoing changes</h4><p>Observers handle collection, item and collection-membership changes so the mirror can follow library activity.</p></div>
<div class="guide-card"><h4>Inspection and recovery</h4><p>Logs help you inspect operations. The internal trash folder and unfiled folder support maintenance workflows.</p></div></div>{% include software-figure.html folder="zotero-plugin" file="zoter05.png" alt="Zotero collection hierarchy beside the mirrored filesystem tree" caption="Compare the library organization with its corresponding folders." %}</section>
<details><summary>After sanitizing: a quick inspection</summary><ul class="list-group list-group-flush"><li class="list-group-item">Open a linked PDF from Zotero and confirm that the file resolves.</li><li class="list-group-item">Check representative annotations after migrating stored attachments.</li><li class="list-group-item">Inspect collection folders and any errors in the plugin logs.</li></ul></details>
<footer class="guide-footer">Source documentation: <a href="https://github.com/automation-scripting/zotero-mirroring-plugin">Plugin source and manifest</a> · <a href="https://github.com/automation-scripting/zotero-mirroring-plugin/blob/main/plugin/core/ui.js">Context-menu implementation</a>. Interface labels may appear in Portuguese; this guide provides their English meaning.</footer>
</div>
