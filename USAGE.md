# Usage Guide

## Step-by-Step Process

### 1. 📝 Create an Idea

Start with the idea template:
```bash
cp templates/idea-template.md ideas/idea-your-project-name.md
```

Fill out all sections:
- Give it a catchy headline
- Select the appropriate category (check the box with `[x]`)
- Provide a detailed description
- Specify target audience
- List technologies you'd like to use
- Estimate complexity (check the box with `[x]`)
- Mention similar projects for reference

### 2. 🎫 Generate Tickets

#### Single Idea
```bash
python3 scripts/ideas_to_tickets.py ideas/idea-your-project-name.md
```

#### All Ideas
```bash
./scripts/convert_all_ideas.sh
```

### 3. 📊 Review and Customize

The generated ticket will be in `tickets/ticket-your-project-name.md` and includes:
- Structured overview
- Category-specific goals
- Technology stack
- 4-phase implementation plan
- Acceptance criteria

Feel free to customize the generated ticket to better fit your needs!

## Best Practices

### Writing Good Ideas
- **Be specific** in your description
- **Include context** about why this project is needed
- **Mention constraints** or special requirements
- **Think about users** and their needs

### Using Generated Tickets
- Review and adjust goals as needed
- Modify the implementation plan based on your resources
- Add specific technical requirements
- Include design mockups or references

## Example Workflow

```bash
# 1. Create a new idea
cp templates/idea-template.md ideas/idea-weather-dashboard.md

# 2. Edit the idea file (use your favorite editor)
nano ideas/idea-weather-dashboard.md

# 3. Generate the ticket
python3 scripts/ideas_to_tickets.py ideas/idea-weather-dashboard.md

# 4. Review the generated ticket
cat tickets/ticket-weather-dashboard.md

# 5. Start implementing your project!
```

## Troubleshooting

### Common Issues

**Q: Script says "No idea files found"**
A: Make sure your idea files start with `idea-` and are in the `ideas/` directory.

**Q: Generated ticket has missing information**
A: Check that you've filled out all sections in your idea template and selected categories/complexity with `[x]`.

**Q: Permission denied when running scripts**
A: Make scripts executable with `chmod +x scripts/*.sh`

### Getting Help

If you encounter issues:
1. Check that your idea file follows the template format
2. Ensure Python 3 is installed
3. Verify file paths are correct
4. Check that you've marked checkboxes with `[x]` not just `[x]`