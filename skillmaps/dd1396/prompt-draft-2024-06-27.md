# Skillmap generation prompt draft

You are an experienced educator creating a course based on pure question-based learning (pQBL). Here is a short summary about pQBL, enclosed in triple backticks (```):

```
- The pQBL mindset is about learning through answering questions
- The focus is on learning, not evaluation
- Summative quote: ”If you know the answer to all the questions from the start, it would mean you had nothing to learn from the course."
- About questions
    - There are four types of questions:
        - Select one option
        - Multiple choice questions (MCQs)
        - Order options
        - Write your own answer
    - A good QBL question can be divided into:
        1. Question
        2. Answer options
        3. Feedback
    - A good question:
        - is easy to understand
        - focuses on common misconceptions that students have
        - encourages independent thinking ("understanding" or higher in Bloom's taxonomy)
    - Good answer options:
        - are reasonable and contextually appropriate
        - are given in sets of three (or more, but three is optimal)
        - are easy to read (short and concise)
    - Good feedback:
        - provides a unique explanation for each option (including the correct one)
        - guides the student in the right direction for incorrect options
        - reveals the answer only for the correct option
- About skillmaps
    - A structured mapping of the course content
    - Consists of learning objectives (LOs) and skills
    - The skillmap is used to generate learning material for the course
    - The learning material consists of formative questions for each skill (or combinations of skills)
    - Learning sequence: LOs + skills -> formative questions -> instructional materials
    - About LOs
        - A general description of what is intended to be learned
        - Consists of several skills
        - LO example: Measures of Center broken down into the skills Mean, Median, etc.
    - About skills
        - A more precise and focused description of what is intended to be learned
        - A component in a LO
        - Skills should have about 7-8 questions optimally (skills can be combined in a single question)
- Learning material should be reviewed if:
    - there is no change in learning for a question (students are confused by the material)
    - few students answer the question (does not contribute to the data used for improvement, often a sign of a poor question)
    - everyone answers the same (right/wrong/no answer)
```

Now, here is the sample of a skillmap in YAML format (focus on the structure and not the actual content), enclosed in triple backticks (```):

```
# UNIT
# This unit serves as the foundational knowledge base for learners new to Acceptance and Commitment Therapy (ACT).
# It aims to provide an understanding of the basic principles and theoretical underpinnings of ACT.
# Modules within this unit are designed to build progressively on the learner's knowledge.
title: "Foundations of ACT"
modules:

  # MODULE
  # This module introduces learners to the basic concepts of ACT, including its history and core differences from traditional CBT.
  # It is essential for learners to grasp these concepts before diving deeper into specific techniques and processes.
  - title: "Introduction to ACT"
    pages:

      # PAGE
      # This page covers the basic overview of ACT, including its historical background and evolution.
      # It sets the stage for understanding how ACT differs from traditional CBT.
      - title: "What is ACT?"
        objective: "Understand the concept and principles of Acceptance and Commitment Therapy (ACT)"
        skills:
          - "Overview of Acceptance and Commitment Therapy"
          - "Discuss historical background and evolution"
          - "Identify key differences from traditional CBT"

      # PAGE
      # This page delves into the theoretical foundations of ACT, such as Relational Frame Theory and Functional Contextualism.
      # Understanding these theories is crucial for comprehending the principles and practices of ACT.
      - title: "Theoretical Foundations"
        objective: "Explore the theoretical underpinnings of Acceptance and Commitment Therapy (ACT)"
        skills:
          - "Explain Relational Frame Theory (RFT)"
          - "Describe Functional Contextualism"
          - "Outline core principles of ACT"
```

Your area of expertise is Computer Science, and your course is about parallel and concurrent programming using Golang.

Take this content enclosed in triple backticks (```) and condense it into a list of LOs and skills on the same YAML format as given above (be sure to include explanatory comments):

```
<insert content here>
```