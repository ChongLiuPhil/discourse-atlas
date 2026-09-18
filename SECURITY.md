# Security Policy

Discourse Atlas is research software with a static hosted web application, local CLI tooling, and portable Agent instructions.

## Sensitive material

Do not place secrets, API keys, private manuscripts, confidential source text, copyrighted material without redistribution permission, or personally sensitive research data in public issues, pull requests, examples, benchmark fixtures, or repository artifacts.

## Hosted Interactive Atlas trust boundary

The official GitHub Pages application is a static client-side Vite build. Local analysis JSON and source Markdown/text selected in the browser are intended to be processed in the browser; Discourse Atlas does not currently provide a project backend upload API.

Do not load confidential material into an untrusted fork, modified build, or third-party mirror. If a future feature introduces server-side storage, remote processing, telemetry, or external API transmission, this policy and privacy/trust-boundary documentation must be updated before release.

## Supply chain

GitHub Actions and JavaScript/Python dependencies are part of the software supply-chain boundary. Dependency and workflow changes should be reviewed and exercised through CI.

## Reporting

For security-sensitive reports, contact a maintainer privately rather than opening a public issue. Do not include exploit secrets or private source material in a public report.
