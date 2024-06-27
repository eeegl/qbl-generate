# Skillmap drafts

This folder contains drafts for the new skillmap format.

As of writing (2024-06-27) there are two main alternatives proposed:

1. Using a [single file](./skillmap-new-single-file/skillmap-)
2. Using a [modular approach](./skillmap-new-modular/) (each unit has its own file)

Out of the two, going modular seems to be the most maintanable option, especially for more lengthy courses. Keeping everything in a single file becomes messy very quickly.

There is also a [generated skillmap](./skillmap-new-modular-dd1396-chatgpt/) for DD1396. This was done using Chat GPT-4o, with each unit generated separately. The prompt used is included.

For reference, the [old format](./skillmap-old/) is also included.

## Motivation

The problem with the old format is that it seems to conflate learning objectives and skills, using only one "level" of description.

Hopefully the new format will give a more focused and clear description for generating questions, which could reduce the trial and error needed to generate specific types of questions.

## Explanation

In the example below from the old version, `aim` should probably be a learning goal, but is used a bit fuzzy as both a learning goal and a skill (and the list is called `skills`).

```yaml
name: "DD1396 Skillmap"
units:

  # New unit
  - name: "Week 1 - Introduction to Go"
    skills:
      - name: "Go Language Basics 1"
        aim: "Show an understanding of Go's syntax, such as basic data types, control structures (loops, conditionals), as well as arrays."
      - name: "Go Language Basics 2"
        aim: "Show an understanding of Go's syntax, such as slices, maps, structs, and functions."
      - name: "Deeper Go Concepts"
        aim: "Be familiar with deeper Go concepts, such as anonymous functions, first order functions, scope, closures, and functions vs. methods."
      - name: "Concurrency vs. Parallelism"
        aim: "Show a grasp of the basic concepts of concurrency and parallelism, as well as their differences."
      - name: "Handling Concurrency in Go"
        aim: "Show a grasp of how concurrency and parallelism are implemented in Go with goroutines and channels."
      - name: "Testing in Go"
        aim: "Be able to use Go's testing framework for writing and running tests."
      - name: "Algorithm implementation"
        aim: "Ability to split a problem into concurrent parts and combine results, specifically implementing a function to sum an array concurrently."
```


So this is what the new format tries to improve upon, by simply letting each page have a learning goal, and a list with skills. Below is what a sample from a unit in the modular version looks like.

```yaml
# UNIT
# This unit introduces Go programming language and its built-in concurrency features, goroutines and channels.
# It provides foundational knowledge in parallel and concurrent programming concepts using Go.
title: "Introduction to Parallel and Concurrent Programming in Go"
modules:

  # MODULE
  # This module covers the basics of Go programming language and its comparison with other languages like Java or Python.
  # It sets the foundation for understanding Go's unique concurrency model using goroutines and channels.
  - title: "Fundamentals of Go Programming"
    pages:

      # PAGE
      # This page introduces Go as a programming language, including its syntax and key features.
      - title: "Introduction to Go"
        objective: "Learn the basics of Go programming language"
        skills:
          - "Setup a functioning Go environment"
          - "Compare and contrast Go with either Java or Python"

      # PAGE
      # This page explores goroutines and channels as fundamental components of Go's concurrency model.
      - title: "Concurrency in Go: Goroutines and Channels"
        objective: "Understand and use goroutines and channels for concurrent programming"
        skills:
          - "Use goroutines to achieve concurrency"
          - "Utilize channels for communication between goroutines"
```
