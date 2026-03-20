# AI Resume Shortlisting & Interview Assistant #

This project is a backend AI system that will check resumes based on a job description, give a score, and explain the rationale behind the score, categorize candidates by tier, and create personalized interview questions.
The system doesn’t rely on keyword matching; rather, it uses different factors such as skill matching, semantic matching, achievements, and ownership to mimic how a recruiter would truly assess a candidate.

## 1. Project Overview

The system processes a **resume** (PDF or text) against a **job description** to generate the following outputs:

* **Final Score & Tier Classification:** A numerical ranking and categorical placement.
* **Skill Analysis:** A detailed breakdown of both **matched** and **missing** skills.
* **Contextual Insights:**
    * A **human-readable explanation** of the fit.
    * **Tailored interview questions** specific to the candidate's background.

---

## 2. System Architecture

### 🏗️ **High-Level Flow**

The system follows a linear pipeline designed to transform raw document data into actionable hiring intelligence:

![System Architecture Flowchart]
