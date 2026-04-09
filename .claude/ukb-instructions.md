# UKB Pipeline Instructions

## When to Escalate

You are operating autonomously. Push through routine implementation, testing,
and debugging on your own. But STOP and escalate in these cases:

### Must Escalate (write escalation file)
- **UI/UX design decisions**: Layout choices, user flows, visual design, component
  selection that isn't specified in the issue. Don't guess at design — ask.
- **Architecture decisions**: New services, significant schema changes, new API
  endpoints not described in the issue, cross-service communication patterns.
- **Billing/paywall/monetization**: Anything touching pricing, subscription logic,
  payment flows, or feature gating.
- **Scalability concerns**: If you foresee a performance bottleneck, data growth
  issue, or infrastructure requirement that the current approach won't handle.
- **Security-sensitive changes**: Auth flows, permission models, secrets handling,
  CORS/CSP changes, new external API integrations.
- **Ambiguous requirements**: If the issue description is too vague to implement
  without making significant assumptions.

### Do NOT Escalate (handle yourself)
- Missing dependencies — install them.
- Failing tests — fix them.
- Merge conflicts — resolve them.
- Linting errors — fix them.
- Build errors — debug and fix them.
- Choosing between equivalent implementation approaches — pick the simpler one.

## How to Escalate

Write a file at `.claude/escalation.json`:

```json
{
  "type": "needs_human",
  "category": "architecture|ui_ux|billing|scalability|security|ambiguous",
  "summary": "One-line summary of what you need",
  "detail": "Full explanation of the decision point and your recommendation",
  "options": ["Option A: ...", "Option B: ..."],
  "recommendation": "Which option you'd pick and why",
  "blocking": true
}
```

After writing the file, STOP WORKING. Do not continue past the escalation point.
The pipeline will detect this file and notify an admin.

## How to Report a Snag

If you encounter an environment problem you cannot fix (missing system package
that requires sudo, network access denied, SSH key missing, etc.), write:

`.claude/snag.json`:
```json
{
  "type": "environment",
  "error": "The actual error message",
  "attempted_fix": "What you tried",
  "needs": "What would fix it (e.g., 'sudo apt install libpq-dev')"
}
```

Then STOP. Do not loop retrying the same failing operation.

