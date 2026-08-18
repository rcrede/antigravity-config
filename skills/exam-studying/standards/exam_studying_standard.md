---
type: normative
description: Operational rules for the exam-studying skill.
---

# Exam Studying Standard

This document outlines the standard operating procedures for the `exam-studying` skill.

## 1. Evidence-Based Learning Methods
- **Feynman Technique**: Use this for building initial understanding of new concepts. Force the user to explain the concept in their own words. Identify knowledge gaps and simplify using analogies.
- **Active Recall**: Use this for reinforcing memory. Generate practice tests or short-answer quizzes. Do not provide the answer until the user attempts it.
- **Spaced Repetition (Anki)**: After a concept is understood, extract the knowledge into Anki flashcards (Front/Back) format and export as CSV.

## 2. Oral Exam Protocol
- The simulation must be strict.
- Do not just stick to the provided syllabus; introduce curveball questions that extend beyond the core material to prepare the user for "extra credit" level performance.
- Log the user's performance and grades in an artifact or a tracking note in the vault (e.g. `10_Projects/Masters_Program_Planning.md` or a dedicated grading note).

## 3. Strict State Enforcement
- The skill operates via `scripts/exam_studying_referee.py`.
- Agents must ALWAYS use this referee to transition between the modes (Feynman, Quizzing, Oral Exam, Anki). No freeform interactions unless the referee explicitly allows it.
