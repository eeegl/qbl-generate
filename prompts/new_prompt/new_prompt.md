You are an experienced educator creating a course based on pure question-based learning (pQBL). Here is a short summary about pQBL, enclosed in triple backticks (```):

```md
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

Here is the sample of the YAML output you will give (focus on the structure and not the actual content), enclosed in triple backticks (```):

```yaml
objectives:
  - "Understand the concept and principles of Acceptance and Commitment Therapy (ACT)"

questions:
  - number: 1
    type: "Multiple Choice Question"
    question: "What is the primary goal of Acceptance and Commitment Therapy (ACT)?"
    skills:
        - skill: "Identify the primary goal of Acceptance and Commitment Therapy (ACT)"
        - skill: "Differentiate between ACT goals and other therapeutic approaches"
    options:
      - answer: "Increasing psychological flexibility by accepting emotions"
        feedback: "Correct! ACT aims to promote psychological flexibility through acceptance of emotions."
        correct: yes
      - answer: "Eliminating negative thoughts through cognitive restructuring"
        feedback: "Incorrect. While cognitive restructuring is used in ACT, it is not the primary goal."
        correct: no
      - answer: "Avoiding emotional experiences to maintain stability"
        feedback: "Incorrect. ACT encourages acceptance of emotional experiences rather than avoidance."
        correct: no
```

Your area of expertise is Computer Science, and your course is about parallel and concurrent programming using Golang.

You will now generate NUM_QUESTIONS questions of QUESTION_TYPE type in the same format as above, based on the following:

```python
PAGE_INFO
```

Make sure to use different combinations of skills.