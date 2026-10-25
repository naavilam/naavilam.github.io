---
layout: post
title:  "Zotero WebDAV Server"
description: "A self-hosted serverless alternative to Zotero Cloud ($10/month), storing and syncing up to 100 GB of Zotero attachments across computers and mobile devices on AWS + Cloudflare for ~$0.60/month."
date:   2026-10-25
type: card-img-top
image: zotero-webdav-server.png # for local images, place in /assets/img/posts/
caption:
last-updated: 2026-10-25
tag: Infrastructure
author: Nara Avila
card: card-6
repo: automation-scripting/zotero-webdav-server
categories: [software]
---

<link rel="stylesheet" href="{{ '/assets/css/software-guides.css' | relative_url }}">
<div class="software-guide guide-webdav">
<header class="guide-hero">
	<span class="eyebrow">Serverless attachment synchronization</span>
	<h2>Sync your Zotero library across desktop and mobile for ~$0.60/month</h2>
	<p class="lead">We are building a self-hosted serverless storage service analogous to <strong>Zotero Cloud / Zotero Storage</strong> (which costs around <strong>$10/month</strong> on the unlimited tier) — for roughly <strong>$0.60 USD/month</strong>. Built with Terraform, Cloudflare Workers and AWS (API Gateway, Lambda in Go and private S3) on a practically free compute tier, Zotero WebDAV Server stores and synchronizes up to 100 GB of PDF attachments and library archives across computers and mobile devices with zero idle server costs.</p>
</header>
<nav class="guide-nav" aria-label="Guide sections">
	<a href="{{ page.url | relative_url }}#architecture">Architecture &amp; Cost</a>
	<a href="{{ page.url | relative_url }}#prerequisites">Accounts Needed</a>
	<a href="{{ page.url | relative_url }}#variables">Variables</a>
	<a href="{{ page.url | relative_url }}#deploy">Deployment</a>
	<a href="{{ page.url | relative_url }}#zotero">Zotero Setup</a>
</nav>

<figure class="guide-figure">
	<a href="{{ '/assets/img/apps/zotero-webdav-server.png' | relative_url }}">
		<img src="{{ '/assets/img/apps/zotero-webdav-server.png' | relative_url }}" alt="Zotero File Syncing preferences configured to use WebDAV with https://webdav.zotero.workers.dev/zotero/" loading="lazy" decoding="async">
	</a>
	<figcaption>Where to find it in Zotero (<strong>Settings → Sync → File Syncing</strong>): switch attachment syncing from Zotero Storage to <strong>WebDAV</strong> and point it to your Cloudflare Worker endpoint (<code>https://webdav.zotero.workers.dev/zotero/</code>).</figcaption>
</figure>

<div class="guide-grid">
	<div class="guide-card">
		<h4>~$0.60/mo vs. $10/mo</h4>
		<p>Replaces a $10/month Zotero Cloud subscription for large libraries. Cloudflare Workers, API Gateway and Lambda run inside practically free tiers; you only pay low-cost S3 storage (~$0.60/month for 100 GB).</p>
	</div>
	<div class="guide-card">
		<h4>Desktop &amp; Mobile Sync</h4>
		<p>Works natively with the standard WebDAV client inside Zotero Desktop (macOS, Windows, Linux) as well as Zotero on iOS, iPadOS and Android.</p>
	</div>
	<div class="guide-card">
		<h4>Private S3 + Presigned URLs</h4>
		<p>The S3 bucket stays strictly private with TLS enforcement and AES-256 encryption. Lambda validates HTTP Basic Auth and signs short-lived SigV4 URLs.</p>
	</div>
</div>

<section id="architecture">
	<div class="step-heading"><span class="step-number">01</span><h3>How the AWS + Cloudflare hybrid infrastructure works</h3></div>
	<p>Standard serverless gateways impose tight payload limits on incoming HTTP bodies (10 MB on API Gateway and 6 MB on synchronous Lambda invocations), which breaks large Zotero attachment uploads while keeping a dedicated EC2 or container running 24/7 would cost $15–$35/month. This project combines <strong>Cloudflare Workers</strong> at the edge with <strong>AWS Lambda + S3</strong> in a single Terraform state to stay practically free:</p>
	<ol class="guide-flow">
		<li>Zotero Client</li>
		<li>Cloudflare Worker</li>
		<li>API Gateway + Go Lambda</li>
		<li>Private Amazon S3</li>
	</ol>
	<ul>
		<li><strong>Lightweight DAV operations (<code>OPTIONS</code>, <code>PROPFIND</code>, <code>MKCOL</code>, <code>HEAD</code>, <code>DELETE</code>):</strong> The Cloudflare Worker forwards metadata requests to API Gateway and the Go Lambda (`arm64` on `provided.al2023`), which translates S3 prefixes and objects under <code>zotero/</code> into WebDAV XML responses.</li>
		<li><strong>Large attachment uploads (<code>PUT</code>):</strong> Instead of sending the binary ZIP through API Gateway or Lambda, the Worker sends only the file metadata (path, content type and size) plus an internal bridge token to Lambda's <code>/_worker/upload</code> endpoint. Lambda authenticates the user, generates a 120-second presigned S3 <code>PutObject</code> URL, and the Worker streams the upload directly to S3 via <code>FixedLengthStream</code> (or issues a <code>307 Temporary Redirect</code>).</li>
		<li><strong>Direct downloads (<code>GET</code>):</strong> Lambda verifies the object and returns a <code>307 Temporary Redirect</code> with a presigned S3 <code>GetObject</code> URL, allowing Zotero on computers and mobile devices to download the attachment archive directly from S3.</li>
	</ul>
	<aside class="guide-callout">
		<strong>Why ~$0.60 USD / month?</strong> Cloudflare Workers Free includes 100,000 requests/day ($0.00), and AWS Lambda + HTTP API Gateway calls for personal research libraries amount to fractions of a cent per month. Storing and syncing up to 100 GB of Zotero attachments in S3 with lifecycle optimization and AWS free data transfer allowances keeps the effective monthly bill around <strong>$0.60 USD/month</strong>, with zero charge when idle.
	</aside>
</section>

<section id="prerequisites">
	<div class="step-heading"><span class="step-number">02</span><h3>What you need before deploying</h3></div>
	<p>To provision and run your own instance of <code>zotero-webdav-server</code>, you need three accounts:</p>
	<div class="guide-grid">
		<div class="guide-card">
			<h4>1. AWS Account</h4>
			<p>Provides the private S3 storage bucket, the HTTP API Gateway, the Go Lambda handler, CloudWatch logs and the IAM OIDC role for GitHub Actions deployments.</p>
		</div>
		<div class="guide-card">
			<h4>2. Cloudflare Account</h4>
			<p>Hosts the edge Worker on your free <code>*.workers.dev</code> subdomain (no custom domain purchase required). You will need your <strong>Account ID</strong> and an <strong>API Token</strong> with <em>Workers Scripts: Edit</em> permission.</p>
		</div>
		<div class="guide-card">
			<h4>3. Terraform Cloud (HCP) Account</h4>
			<p>Manages the unified infrastructure state (workspace <code>zotero-webdav-server</code>) and securely stores the sensitive variables shared between AWS and Cloudflare.</p>
		</div>
	</div>
</section>

<section id="variables">
	<div class="step-heading"><span class="step-number">03</span><h3>Define the required variables</h3></div>
	<p>Configure the following variables in your Terraform workspace (or <code>terraform.tfvars</code>) and execution environment so Terraform can wire the Cloudflare Worker, API Gateway, Lambda and S3 together automatically:</p>

	<h4>Required Credentials &amp; Account Variables</h4>
	<div class="table-scroll">
		<table class="guide-table">
			<thead>
				<tr>
					<th scope="col">Variable</th>
					<th scope="col">Type / Scope</th>
					<th scope="col">Description</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td><code>webdav_username</code></td>
					<td>Terraform (<code>sensitive</code>)</td>
					<td>HTTP Basic Auth username that you will enter inside Zotero's sync settings.</td>
				</tr>
				<tr>
					<td><code>webdav_password</code></td>
					<td>Terraform (<code>sensitive</code>)</td>
					<td>HTTP Basic Auth password for Zotero (minimum 5 characters; use a strong secret).</td>
				</tr>
				<tr>
					<td><code>webdav_worker_token</code></td>
					<td>Terraform (<code>sensitive</code>)</td>
					<td>Shared internal secret (at least 32 random characters) used to authenticate requests between the Cloudflare Worker and the Lambda bridge (<code>X-WebDAV-Worker-Token</code>).</td>
				</tr>
				<tr>
					<td><code>cloudflare_account_id</code></td>
					<td>Terraform (<code>string</code>)</td>
					<td>Your Cloudflare Account ID where the Worker script will be published.</td>
				</tr>
				<tr>
					<td><code>cloudflare_api_token</code> / <code>CLOUDFLARE_API_TOKEN</code></td>
					<td>Terraform or Environment (<code>sensitive</code>)</td>
					<td>Cloudflare API Token scoped to your account with <strong>Workers Scripts: Edit</strong> permission.</td>
				</tr>
				<tr>
					<td><code>AWS_ACCESS_KEY_ID</code> &amp; <code>AWS_SECRET_ACCESS_KEY</code></td>
					<td>Environment / OIDC</td>
					<td>AWS credentials (or dynamic OIDC role credentials in Terraform Cloud) authorized to provision S3, Lambda, API Gateway, IAM and CloudWatch resources.</td>
				</tr>
			</tbody>
		</table>
	</div>

	<h4 class="mt-4">Optional Tuning Variables (with defaults in <code>infra/_variables.tf</code>)</h4>
	<div class="table-scroll">
		<table class="guide-table">
			<thead>
				<tr>
					<th scope="col">Variable</th>
					<th scope="col">Default</th>
					<th scope="col">What it controls</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td><code>cloudflare_workers_subdomain</code></td>
					<td><code>"zotero"</code></td>
					<td>Your existing Cloudflare account <code>workers.dev</code> subdomain (without <code>.workers.dev</code>).</td>
				</tr>
				<tr>
					<td><code>cloudflare_worker_name</code></td>
					<td><code>"webdav"</code></td>
					<td>Name of the deployed Cloudflare Worker script.</td>
				</tr>
				<tr>
					<td><code>cloudflare_upload_mode</code></td>
					<td><code>"stream"</code></td>
					<td>Upload path: <code>stream</code> (Worker streams PUT to S3 via <code>FixedLengthStream</code>) or <code>redirect</code> (307 redirect to S3).</td>
				</tr>
				<tr>
					<td><code>cloudflare_max_upload_bytes</code></td>
					<td><code>100000000</code></td>
					<td>Application upload size cap in bytes (100 MB default matching Cloudflare Free/Pro ingress limit).</td>
				</tr>
				<tr>
					<td><code>project_name</code></td>
					<td><code>"zotero-webdav-server"</code></td>
					<td>Base naming prefix for AWS resources.</td>
				</tr>
				<tr>
					<td><code>env</code></td>
					<td><code>"prod"</code></td>
					<td>Deployment environment suffix (<code>prod</code> sets Lambda log level to <code>INFO</code>).</td>
				</tr>
				<tr>
					<td><code>aws_region</code></td>
					<td><code>"us-east-2"</code></td>
					<td>AWS region for the S3 bucket, API Gateway and Lambda function.</td>
				</tr>
				<tr>
					<td><code>presigned_get_expiration_seconds</code></td>
					<td><code>300</code></td>
					<td>Lifetime in seconds (60–3600) for presigned S3 download URLs.</td>
				</tr>
				<tr>
					<td><code>presigned_put_expiration_seconds</code></td>
					<td><code>120</code></td>
					<td>Lifetime in seconds (60–300) for short-lived presigned S3 upload URLs.</td>
				</tr>
				<tr>
					<td><code>lambda_memory_size</code> / <code>lambda_timeout_seconds</code></td>
					<td><code>128</code> / <code>15</code></td>
					<td>Memory (MB) and execution timeout (seconds) for the ARM64 Go Lambda handler.</td>
				</tr>
				<tr>
					<td><code>api_throttling_rate_limit</code> / <code>api_throttling_burst_limit</code></td>
					<td><code>20</code> / <code>50</code></td>
					<td>Sustained requests/second and burst limit on API Gateway.</td>
				</tr>
			</tbody>
		</table>
	</div>

	<details>
		<summary>Example: generating <code>webdav_worker_token</code> and setting variables</summary>
		<p>Generate a 32+ character random token locally and register the required values in your Terraform workspace (never commit secrets to Git):</p>
		<pre><code># Generate a 64-character hex secret for webdav_worker_token
openssl rand -hex 32

# Example terraform.tfvars (keep local / set in Terraform Cloud UI)
webdav_username              = "nara"
webdav_password              = "your-strong-zotero-password"
webdav_worker_token          = "paste-your-64-char-random-hex-token-here"
cloudflare_account_id        = "your-cloudflare-account-id"
cloudflare_workers_subdomain = "your-subdomain"</code></pre>
	</details>
</section>

<section id="deploy">
	<div class="step-heading"><span class="step-number">04</span><h3>Build the Go handler and apply Terraform</h3></div>
	<p>In <code>infra/_main.tf</code>, update the <code>cloud</code> block with your Terraform Cloud organization and workspace name. Build the ARM64 Go binary for the initial Lambda package, then initialize and apply the Terraform configuration:</p>
	<pre><code># 1. Run tests for the Worker and Go WebDAV handler
node --test worker/worker.test.mjs
cd infra/handler_webdav &amp;&amp; go test ./...

# 2. Build the initial ARM64 Lambda bootstrap binary
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 \
  go build -trimpath -ldflags="-s -w" -o bootstrap .

# 3. Provision AWS + Cloudflare infrastructure via Terraform
cd ..
terraform init
terraform validate
terraform apply</code></pre>
	<p>When the apply finishes, Terraform outputs <code>zotero_worker_base_url</code> (for example, <code>https://webdav.your-subdomain.workers.dev</code>) and <code>aws_lambda_github_role_arn</code>. If you use the included GitHub Actions workflow (<code>.github/workflows/deploy-lambda-function.yml</code>) for continuous Lambda code updates, save that IAM role ARN as the repository secret <code>AWS_LAMBDA_ROLE_TO_ASSUME_PROD</code>.</p>
</section>

<section id="zotero">
	<div class="step-heading"><span class="step-number">05</span><h3>Connect Zotero on computers and mobile devices</h3></div>
	<p>Open Zotero on your desktop computer or mobile device (iOS, iPadOS or Android) and go to <strong>Settings → Sync → File Syncing</strong>:</p>
	<ul>
		<li>Set <strong>Sync attachment files in My Library using</strong> to <strong>WebDAV</strong>.</li>
		<li>Select <strong>https</strong> and enter the host/path from <code>zotero_worker_base_url</code> (without the trailing <code>/zotero/</code>, as Zotero appends <code>/zotero/</code> automatically).</li>
		<li>Enter your <code>webdav_username</code> and <code>webdav_password</code>.</li>
		<li>Click <strong>Verify Server</strong>. Zotero performs an <code>OPTIONS</code> check, a <code>PROPFIND</code> lookup, and creates/deletes <code>zotero-test-file.prop</code> to confirm full read/write access.</li>
	</ul>
	<aside class="guide-callout">
		<strong>Avoid interactive browser challenges on the Worker route.</strong> Do not enable Cloudflare Access login screens, CAPTCHA challenges or aggressive caching rules on the WebDAV Worker hostname — native Zotero clients on desktop and mobile require direct HTTP Basic authentication, <code>207 Multi-Status</code> XML responses and uncached presigned redirects.
	</aside>
</section>

<footer class="guide-footer">Source repository: <a href="https://github.com/automation-scripting/zotero-webdav-server">automation-scripting/zotero-webdav-server</a> · Infrastructure definitions: <code>infra/_variables.tf</code>, <code>infra/cloudflare_worker.tf</code> and <code>infra/lambda_webdav.tf</code>.</footer>
</div>

