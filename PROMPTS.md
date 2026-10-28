# Short prompts for task-focused Codex workflows

Use only within the tool and model permissions of the actual environment. These are examples, not instructions to override platform rules.

## 1. Initial task analysis

> Read the actual task instructions and identify (a) mandatory deliverables, (b) acceptance criteria, (c) constraints, and (d) uncertainties. List the smallest set of files needed to begin. Do not modify anything yet. Keep your answer concise and cite file names/line ranges when possible.

## 2. Implementation

> Implement only the highest-priority uncompleted requirements. Reuse working local code where it helps. Explain changed files and run targeted tests. Do not transmit data externally, change system security settings, or install unrelated dependencies.

## 3. Diagnose a failure

> Here is the exact error and command: [paste]. Reproduce if possible, identify the likely root cause, make the minimum targeted fix, and rerun the failing test. Report the observed result.

## 4. Review deliverables

> Compare the final files against each acceptance criterion. Separate verified requirements, unverified assumptions, and remaining defects. Report exact file paths and test commands/results. Do not claim success without evidence.

## 5. Summarize decisions

> In 5-8 concise points, summarize the problem, alternative approaches, chosen approach, evidence, known limitations, and checks actually performed. Use only the observed work record. Do not invent successful tests.
