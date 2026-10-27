# AI Usage and Prompt History

## 1. Purpose

This document describes the AI tools used during the development of the YottaFlex AI Lead Scoring and Sales Pipeline project. It summarizes the main prompt topics, explains how AI assistance was used, and records the implementation activities and validation results performed during development.

## 2. AI Tools Used

| AI Tool | Approximate Share of AI Assistance | Primary Purpose |
|---|---:|---|
| ChatGPT | 90% | Implementation guidance, debugging, testing, explanations, and documentation |
| Google Gemini | 10% | Understanding testing and anomaly-related files |

These percentages are approximate estimates of AI assistance, not measurements of code authorship.

## 3. ChatGPT Prompt History

ChatGPT was the primary AI assistant used during project development. The following entries summarize the major prompt topics from the available project conversation. They are organized by development activity and are not guaranteed to reproduce every original message verbatim.

### 3.1 Project Setup and Data Generation

- Requested step-by-step guidance for building the lead-scoring and sales-pipeline project in VS Code.
- Requested assistance with structuring a Python project and organizing its source files.
- Requested help generating synthetic CRM datasets for companies, contacts, leads, campaigns, consents, and activities.
- Requested guidance on using a fixed random seed to make generated data reproducible.
- Shared terminal output and requested troubleshooting when commands or modules failed.

### 3.2 Lead Scoring and Sales Pipeline

- Requested help implementing rule-based lead scoring using company fit, buying intent, and engagement.
- Requested guidance on assigning lead scores and categorizing leads by priority.
- Requested assistance implementing territory-aware and product-aware sales routing.
- Requested help applying consent restrictions and generating follow-up tasks.
- Requested assistance generating opportunities and recording sales-stage history.
- Requested validation of record counts, identifiers, relationships, score ranges, routing decisions, and opportunity records.

### 3.3 Anomaly Fixtures and Testing

- Requested help generating five anomaly fixtures covering opted-out lead contact, post-conversion activity used in scoring, incorrect territory assignment, duplicate opportunity associations, and missing stage transitions.
- Shared a Python traceback and requested help fixing an undefined variable in the territory-anomaly fixture logic.
- Requested assistance creating automated tests for anomaly-fixture completeness and ground-truth consistency.
- Requested help implementing fixture-level anomaly detection checks.
- Requested help interpreting pytest results and structural validation output.

### 3.4 Reproducibility and Documentation

- Requested instructions for comparing generated CSV files using SHA-256 checksums.
- Requested help preparing the README and data dictionary.
- Requested help documenting dataset fields, relationships, source modules, validation results, and limitations.
- Requested guidance for reviewing the documentation against the candidate submission requirements.
- Requested assistance preparing the project for a public GitHub repository.

### 3.5 Debugging and Iterative Development

During development, ChatGPT was given terminal output and Python tracebacks so it could suggest targeted corrections. The implementation was updated and rerun locally to check whether the issues were resolved.

The prompt topics above are summaries of the available project conversation, not a verbatim export of every ChatGPT message.

## 4. Google Gemini Prompt History

Google Gemini was used for approximately 10% of the AI assistance during development. Its use was focused specifically on understanding the testing and anomaly-related files in the project.

### 4.1 Purpose of Use

Gemini was used to help understand:

- The purpose and structure of the project's testing files.
- How anomaly fixtures represent business-rule violations.
- How anomaly cases and ground-truth labels are organized.
- How anomaly-related files fit into the project's validation and testing workflow.

### 4.2 Prompt Topics

The following entries summarize the topics of the Gemini requests. They are summaries rather than verbatim quotations of the original prompts.

1. **Understanding testing files:** Requests to explain the purpose and structure of the project's test files.
2. **Understanding anomaly files:** Requests to explain how anomaly cases are represented and how their details are organized.
3. **Understanding ground truth:** Requests to clarify the role of ground-truth labels and their relationship to anomaly fixtures.

### 4.3 Scope of Gemini Assistance

Gemini's contribution was limited to understanding the testing and anomaly-related files. ChatGPT was the primary AI assistant for implementation guidance, debugging, validation, and documentation.

## 5. How AI Assistance Was Used

AI assistance helped break the project into manageable steps, explain implementation concepts, suggest code changes, troubleshoot errors, improve test coverage, and organize the documentation.

Suggestions were applied in the local development environment, and the project modules were run to inspect their behavior. Terminal output, validation results, and test results were used to check the implementation at the recorded development stage.

AI-generated suggestions were treated as assistance rather than proof of correctness. The implementation, design choices, and limitations remain the responsibility of the project author.

## 6. Personal Implementation and Validation Activities

During development, I:

- Set up a local Python virtual environment and installed project dependencies.
- Applied code changes in VS Code and executed project modules locally.
- Investigated errors using Python tracebacks and terminal output.
- Generated the core datasets using the fixed random seed `20261022`.
- Compared SHA-256 checksums and confirmed that six core generated CSV files were byte-for-byte identical across two recorded runs.
- Ran the structural validation module and observed 22 passed checks and 0 failed checks.
- Ran pytest and observed 5 passed tests.

These results document the verification performed at that stage. They do not establish that every possible business-rule violation has been tested against the production pipeline.

## 7. Current Testing Limitations

The current automated tests verify anomaly-fixture completeness, expected anomaly types, ground-truth labels, fixture-level detection behavior, and handling of unknown issue types.

The anomaly detector evaluates the supplied fixture details. The tests do not yet demonstrate that every production scoring, routing, opportunity, and stage-history rule detects real violations introduced into altered production datasets.

The recorded validation results demonstrate the checks that were executed, not the absence of every possible defect.

## 8. Individual Responsibility

I am responsible for reviewing the implementation, understanding the scoring and routing rules, explaining the design choices, and discussing the validation approach and known limitations during the project walkthrough.

AI assistance does not replace the need to understand the submitted project or verify its behavior.
