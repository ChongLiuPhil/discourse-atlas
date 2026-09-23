# Cloudflare migration plan — management-only

Status: **planning only**. This file records a future hosting/access migration and does not change the existing GitHub Pages production site, public source repository, current URL, content, release state, or provider actual state.

## Current-state preservation
- Preserve the public GitHub source repository.
- Preserve the existing GitHub Pages production resource and URL until a separately verified restricted Worker cutover.
- Do not disable Pages, delete branches, change canonical links, or redirect traffic in this phase.

## Target management state
- Target provider: Cloudflare Workers / Workers Static Assets.
- Planned Worker: `discourse-atlas`.
- Target Web visibility: restricted while source remains public.
- Reader policy reference: `shared-reader-access`.
- Preview visibility: private; preview builds disabled until real Access acceptance.
- Production branch: `main`; commit-triggered only; no scheduled polling.
- Public bypass: disabled; no custom domain selected.
- Paid services: not authorized.

## Content/build boundary
This phase does not modify application/source content, docs, schemas, release process, Pages workflow, or build commands. A later deployment phase must separately verify the actual build/output contract and live asset set.

## Manual/provider gates
Cloudflare login/MFA, account-wide Access verification, approved readers, GitHub App authorization, Worker/Builds reconciliation, real build/output verification, anonymous denial, approved-reader access, direct-asset protection, and final cutover authorization remain separate gates.

## Rollback
Pages remains untouched and is therefore the pre-cutover recovery path. After a future verified Worker cutover, retain the previous verified Worker version. No DNS/domain, paid-plan, or old-site-retirement action is authorized here.
