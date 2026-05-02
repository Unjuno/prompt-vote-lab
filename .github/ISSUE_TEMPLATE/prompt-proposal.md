---
name: Prompt proposal
description: Propose a prompt candidate for Prompt Vote Lab
title: "[Prompt]: "
labels: ["prompt-proposal"]
body:
  - type: markdown
    attributes:
      value: |
        Propose one prompt candidate. Voting happens with GitHub reactions after the issue is created.
  - type: textarea
    id: voted-prompt
    attributes:
      label: Voted prompt
      description: The exact prompt you want the implementation model to run.
      placeholder: Make the lab page explain the experiment clearly.
    validations:
      required: true
  - type: textarea
    id: expected-result
    attributes:
      label: Expected result
      description: What should be visibly different if this prompt works?
      placeholder: A first-time visitor should understand the experiment within 10 seconds.
    validations:
      required: true
  - type: checkboxes
    id: scope-check
    attributes:
      label: Scope check
      options:
        - label: This can be implemented with static HTML, CSS, and vanilla JavaScript only.
          required: true
        - label: This does not require backend, login, payment, database, external API, or secrets.
          required: true
        - label: This can be implemented by editing only lab/index.html, lab/style.css, and lab/app.js.
          required: true
---
