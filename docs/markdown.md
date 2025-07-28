# Markdown Quick Tutorial

Markdown is a lightweight markup language that's easy to read and write. Here's a quick guide to the most common formatting:

## Headers

Use `#` for headers. More `#` symbols create smaller headers:

```markdown
# Header 1 (largest)
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6 (smallest)
```

## Text Formatting

- **Bold text**: `**bold**` or `__bold__`
- *Italic text*: `*italic*` or `_italic_`
- ***Bold and italic***: `***text***`
- ~~Strikethrough~~: `~~strikethrough~~`
- `Inline code`: `` `code` ``

## Lists

### Unordered Lists
Use `-`, `*`, or `+`:
```markdown
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2
```

### Ordered Lists
Use numbers:
```markdown
1. First item
2. Second item
3. Third item
```

## Links and Images

- Links: `[Link text](https://example.com)`
- Images: `![Alt text](image-url.jpg)`
- Email links: `<email@example.com>`

## Code

### Inline Code
Use backticks: `` `code` ``

### Code Blocks
Use triple backticks with optional language:
````markdown
```python
def hello():
    print("Hello, World!")
```
````

## Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Data     | Data     |
```

## Blockquotes

Use `>` for quotes:
```markdown
> This is a blockquote.
> It can span multiple lines.
```

## Horizontal Rules

Use three or more dashes, asterisks, or underscores:
```markdown
---
***
___
```

## Line Breaks

- Two spaces at the end of a line create a line break
- Empty line creates a paragraph break

## Escape Characters

Use backslash `\` to escape special characters:
```markdown
\*This won't be italic\*
\# This won't be a header
```

## Quick Tips

1. **Preview**: In VS Code, use `Cmd+Shift+V` to preview Markdown
2. **Live preview**: Use `Cmd+K V` for side-by-side preview
3. **Keep it simple**: Markdown is meant to be readable as plain text
4. **Consistent spacing**: Use consistent spacing around headers and elements

Markdown is designed to be intuitive.  If it looks right in plain text, it probably is right.