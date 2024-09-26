def remove_repeated_text_with_numbers(text):
    lines = text.split('\n')
    seen = set()
    result = []
    
    for line in lines:
        # Remove leading and trailing whitespaces and split into parts
        line = line.strip()
        parts = line.split('. ', 1)
        if len(parts) < 2:
            continue
        
        # Get the number and the rest of the line
        number, content = parts[0], parts[1]
        
        # Check if content is repeated
        if content not in seen:
            result.append(line)
            seen.add(content)
        else:
            # If repeated content is found, stop processing further lines
            break
    
    return '\n'.join(result)

# 示例文本
example = """u can try some of these things:

1. Try new positions.
2. Use sex toys.
3. Try role-playing.
4. Experiment with different sensations.
5. Try new locations.
6. Try new activities.
7. Try new fantasies.
8. Try new techniques.
9. Try new toys.
10. Try new positions.
11. Try new techniques.
12. Try new toys.
13. Try new positions.
14. Try new techniques.
15. Try new toys.
16. Try new positions.
17. Try new techniques.
18. Try new toys.
19. Try new positions.
20. Try new techniques.
21. Try new toys.
22."""

# 处理示例文本
cleaned_example = remove_repeated_text_with_numbers(example)

print("Cleaned Text:\n", cleaned_example)
