# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Skills Repository** for Claude Code - a collection of modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Skills are "onboarding guides" for specific domains that transform Claude into a specialized agent.

See [README.md](README.md).

## Agent Instructions

Always Use the searching-docs skill for searching external library/API documentation and references.

When writing commit messages, name the affected skill in the subject as prose (e.g. "Add X to ansible skill", "Remove Y from writing-commit-messages skill"). Omit the scope only when the change spans the whole repository.
