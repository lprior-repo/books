#!/usr/bin/env python3
"""
Extract all Go code snippets from markdown files.
"""

import re
import os
from pathlib import Path
from collections import defaultdict

# List of files to process
FILES = [
    "/home/user/books/markdown_output/ansible-for-kubernetes/ansible-for-kubernetes.md",
    "/home/user/books/markdown_output/Writing_an_Interpreter_In_Go_-_Thorsten_Ball/Writing_an_Interpreter_In_Go_-_Thorsten_Ball.md",
    "/home/user/books/markdown_output/Writing_a_Compiler_in_Go_-_Thorsten_Ball/Writing_a_Compiler_in_Go_-_Thorsten_Ball.md",
    "/home/user/books/markdown_output/Ultimate_Microservices_with_Go_-_Nir_Shtein/Ultimate_Microservices_with_Go_-_Nir_Shtein.md",
    "/home/user/books/markdown_output/The_ultimate_Go_Notebook_-_WIlliam_Kennedy/The_ultimate_Go_Notebook_-_WIlliam_Kennedy.md",
    "/home/user/books/markdown_output/The_Art_of_Unit_Testing_3E_-_Roy_Osherove/The_Art_of_Unit_Testing_3E_-_Roy_Osherove.md",
    "/home/user/books/markdown_output/Terraform_in_Depth_Infrastructure_as_Code_-_Robert_Hafner/Terraform_in_Depth_Infrastructure_as_Code_-_Robert_Hafner.md",
    "/home/user/books/markdown_output/System_Programming_Essentials_with_Go_-_Alex_Rios/System_Programming_Essentials_with_Go_-_Alex_Rios.md",
    "/home/user/books/markdown_output/Shipping_Go_-_Joel_Holmes/Shipping_Go_-_Joel_Holmes.md",
    "/home/user/books/markdown_output/Mastering_Go_-_Mihalis_Tsoukalos/Mastering_Go_-_Mihalis_Tsoukalos.md",
    "/home/user/books/markdown_output/Learning_Go_An_Idiomatic_Approach_to_Real-World_Go_Programming_2nd_Edition_-_Jon_Bodner/Learning_Go_An_Idiomatic_Approach_to_Real-World_Go_Programming_2nd_Edition_-_Jon_Bodner.md",
    "/home/user/books/markdown_output/Go_for_DevOps_-_John_Doak_David_Justice/Go_for_DevOps_-_John_Doak_David_Justice.md",
    "/home/user/books/markdown_output/Go_Systems_Programming_-_Mihalis_Tsoukalos/Go_Systems_Programming_-_Mihalis_Tsoukalos.md",
    "/home/user/books/markdown_output/Go_Programming_Cookbook_Over_75_recipes_-_Ian_Taylor/Go_Programming_Cookbook_Over_75_recipes_-_Ian_Taylor.md",
    "/home/user/books/markdown_output/Functional_Programming_in_Go_-_Dylan_Meeus/Functional_Programming_in_Go_-_Dylan_Meeus.md",
    "/home/user/books/markdown_output/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram/Full-Stack_Web_Development_with_Go_-_Nanik_Tolaram.md",
    "/home/user/books/markdown_output/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz/Engineering_Resilient_Systems_on_AWS_-_Kevin_Schwarz.md",
    "/home/user/books/markdown_output/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka/Efficient_Go_Data-Driven_Optimization_-_Bartlomiej_Plotka.md",
    "/home/user/books/markdown_output/Domain-Driven_Design_with_Golang_-_Matthew_Boyle/Domain-Driven_Design_with_Golang_-_Matthew_Boyle.md",
    "/home/user/books/markdown_output/Designing Distributed Systems/Designing Distributed Systems.md",
    "/home/user/books/markdown_output/Data_Structures_and_Algorithms_with_Go_-_Dusan_Stojanovic/Data_Structures_and_Algorithms_with_Go_-_Dusan_Stojanovic.md",
    "/home/user/books/markdown_output/Concurrency_in_Go_-_Katherine_Cox-Buday/Concurrency_in_Go_-_Katherine_Cox-Buday.md",
    "/home/user/books/markdown_output/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino/Building_Modern_CLI_Applications_in_Go_-_Marian_Montagnino.md",
    "/home/user/books/markdown_output/Build_an_Orchestrator_in_Go_From_Scratch_-_Tim_Boring/Build_an_Orchestrator_in_Go_From_Scratch_-_Tim_Boring.md",
    "/home/user/books/markdown_output/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi/100_Go_Mistakes_and_How_to_Avoid_Them_-_Teiva_Harsanyi.md",
]

# Go-specific patterns to identify Go code
GO_PATTERNS = [
    r'\bpackage\s+\w+',
    r'\bfunc\s+\w*\s*\(',
    r'\bfunc\s+\([^)]+\)\s+\w+',  # method
    r'\bimport\s+\(',
    r'\bimport\s+"',
    r'\btype\s+\w+\s+(struct|interface)',
    r'\bvar\s+\w+',
    r'\bconst\s+\w+',
    r'\bgo\s+\w+\(',  # goroutine
    r'\bchan\s+',
    r'\bdefer\s+',
    r'\bselect\s*{',
    r':=\s*',
    r'\bmake\s*\(',
    r'\bnil\b',
    r'\.Println\(',
    r'\.Printf\(',
    r'\berror\b',
    r'\binterface{}\b',
]

def is_go_code(code):
    """Check if a code snippet is likely Go code."""
    if not code or len(code.strip()) < 5:
        return False

    # Check for Go-specific patterns
    for pattern in GO_PATTERNS:
        if re.search(pattern, code):
            return True
    return False

def extract_code_blocks(content):
    """Extract code blocks from markdown content."""
    snippets = []

    # Pattern for fenced code blocks with optional language identifier
    # Matches ```go, ```golang, or just ``` followed by code
    pattern = r'```(\w*)\n(.*?)```'

    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        lang = match.group(1).lower()
        code = match.group(2)

        # Include if it's explicitly marked as Go or if it looks like Go code
        if lang in ['go', 'golang'] or is_go_code(code):
            snippets.append(code)

    return snippets

def get_book_name(filepath):
    """Extract a readable book name from the filepath."""
    path = Path(filepath)
    # Get the directory name or filename without extension
    name = path.parent.name if path.parent.name != 'markdown_output' else path.stem
    return name

def extract_context_before(content, snippet_start_pos, max_lines=5):
    """Extract context (headings) before a code snippet."""
    before_content = content[:snippet_start_pos]
    lines = before_content.split('\n')

    # Look for the most recent headings
    context_parts = []
    for line in reversed(lines[-50:]):  # Look at last 50 lines
        if line.startswith('#'):
            context_parts.insert(0, line.strip())
            if len(context_parts) >= 2:  # Get up to 2 heading levels
                break

    return ' > '.join(context_parts) if context_parts else "No context"

def process_file(filepath):
    """Process a single markdown file and extract Go snippets."""
    print(f"Processing: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading file: {e}")
        return [], 0

    snippets_with_context = []

    # Find all code blocks
    pattern = r'```(\w*)\n(.*?)```'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    go_count = 0
    for match in matches:
        lang = match.group(1).lower()
        code = match.group(2)

        # Check if it's Go code
        if lang in ['go', 'golang'] or is_go_code(code):
            go_count += 1
            # Extract context
            context = extract_context_before(content, match.start())
            snippets_with_context.append({
                'code': code,
                'context': context,
                'number': go_count
            })

    print(f"  Found {go_count} Go code snippets")
    return snippets_with_context, go_count

def main():
    """Main processing function."""
    print("=" * 80)
    print("Extracting Go Code Snippets from Markdown Files")
    print("=" * 80)
    print()

    all_results = {}
    total_snippets = 0
    files_processed = 0

    for filepath in FILES:
        book_name = get_book_name(filepath)
        snippets, count = process_file(filepath)

        if count > 0:
            all_results[filepath] = {
                'book_name': book_name,
                'snippets': snippets,
                'count': count
            }
            total_snippets += count
            files_processed += 1
        else:
            # Still track files with no snippets
            all_results[filepath] = {
                'book_name': book_name,
                'snippets': [],
                'count': 0
            }
            files_processed += 1

        print()

    # Write output file
    output_path = "/home/user/books/go_code_snippets_extracted.md"
    print(f"Writing results to: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Go Code Snippets Extracted from Books\n\n")
        f.write("## Summary\n")
        f.write(f"- Total files processed: {files_processed}\n")
        f.write(f"- Total Go code snippets found: {total_snippets}\n\n")

        f.write("## Snippets by Book\n\n")

        for filepath, data in all_results.items():
            book_name = data['book_name']
            snippets = data['snippets']
            count = data['count']

            f.write(f"### {book_name}\n")
            f.write(f"**File:** `{filepath}`\n")
            f.write(f"**Total snippets:** {count}\n\n")

            if count > 0:
                for snippet in snippets:
                    f.write(f"#### Snippet {snippet['number']}\n")
                    if snippet['context'] != "No context":
                        f.write(f"**Context:** {snippet['context']}\n\n")
                    f.write("```go\n")
                    f.write(snippet['code'])
                    if not snippet['code'].endswith('\n'):
                        f.write('\n')
                    f.write("```\n\n")
            else:
                f.write("*No Go code snippets found in this file.*\n\n")

            f.write("---\n\n")

    print(f"\nCompleted!")
    print(f"Total files processed: {files_processed}")
    print(f"Total Go snippets extracted: {total_snippets}")
    print(f"Output written to: {output_path}")

    # Print summary by book
    print("\n" + "=" * 80)
    print("Summary by Book:")
    print("=" * 80)
    for filepath, data in all_results.items():
        print(f"{data['book_name']}: {data['count']} snippets")

if __name__ == "__main__":
    main()
