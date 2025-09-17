#!/usr/bin/env python3
"""
Ideas to Tickets Generator

This script converts idea files into structured project tickets with basic implementation plans.
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path


def parse_idea_file(idea_path):
    """Parse an idea file and extract structured information."""
    with open(idea_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract information using regex patterns
    patterns = {
        'headline': r'## Headline\s*\n([^\n]+)',
        'category': r'## Category\s*\n.*?- \[x\] ([^\n]+)',
        'description': r'## Description\s*\n(.*?)(?=\n## |$)',
        'target_audience': r'## Target Audience\s*\n(.*?)(?=\n## |$)',
        'technologies': r'## Technologies/Stack\s*\n(.*?)(?=\n## |$)',
        'complexity': r'## Estimated Complexity\s*\n.*?- \[x\] ([^\n]+)',
        'similar_projects': r'## Similar Projects\s*\n(.*?)(?=\n## |$)',
        'notes': r'## Notes\s*\n(.*?)(?=\n## |$)'
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            extracted[key] = match.group(1).strip()
        else:
            extracted[key] = '[Not specified]'
    
    return extracted


def generate_goals(description, category):
    """Generate basic goals based on description and category."""
    goals = []
    
    # Basic goals based on category
    category_goals = {
        'Web Application': [
            'Create responsive user interface',
            'Implement backend API',
            'Deploy to production environment'
        ],
        'Mobile App': [
            'Design user-friendly mobile interface',
            'Implement core app functionality',
            'Publish to app stores'
        ],
        'CLI Tool': [
            'Design command-line interface',
            'Implement core functionality',
            'Package for distribution'
        ],
        'Library/Framework': [
            'Design public API',
            'Implement core functionality',
            'Create documentation and examples'
        ],
        'API/Service': [
            'Design REST/GraphQL API',
            'Implement backend logic',
            'Set up monitoring and scaling'
        ]
    }
    
    # Use category-specific goals or generic ones
    if category in category_goals:
        goals = category_goals[category]
    else:
        goals = [
            'Plan and design project architecture',
            'Implement core functionality',
            'Test and deploy solution'
        ]
    
    return goals


def create_ticket(idea_data, output_path):
    """Create a ticket file from idea data."""
    # Load ticket template
    template_path = Path(__file__).parent.parent / 'templates' / 'ticket-template.md'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate goals
    goals = generate_goals(idea_data['description'], idea_data['category'])
    
    # Replace placeholders
    replacements = {
        '{HEADLINE}': idea_data['headline'],
        '{IDEA_FILE}': os.path.basename(output_path).replace('.md', ''),
        '{DATE}': datetime.now().strftime('%Y-%m-%d'),
        '{CATEGORY}': idea_data['category'],
        '{DESCRIPTION}': idea_data['description'],
        '{GOAL_1}': goals[0] if len(goals) > 0 else 'Define project goals',
        '{GOAL_2}': goals[1] if len(goals) > 1 else 'Implement solution',
        '{GOAL_3}': goals[2] if len(goals) > 2 else 'Test and deploy',
        '{TARGET_AUDIENCE}': idea_data['target_audience'],
        '{TECHNOLOGIES}': idea_data['technologies'],
        '{COMPLEXITY}': idea_data['complexity'],
        '{SIMILAR_PROJECTS}': idea_data['similar_projects'],
        '{NOTES}': idea_data['notes']
    }
    
    ticket_content = template
    for placeholder, value in replacements.items():
        ticket_content = ticket_content.replace(placeholder, value)
    
    # Write ticket file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ticket_content)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Convert idea files to project tickets')
    parser.add_argument('idea_file', help='Path to the idea file to convert')
    parser.add_argument('-o', '--output', help='Output directory for tickets (default: tickets/)')
    
    args = parser.parse_args()
    
    # Set up paths
    idea_path = Path(args.idea_file)
    if not idea_path.exists():
        print(f"Error: Idea file '{idea_path}' not found")
        return 1
    
    output_dir = Path(args.output) if args.output else Path('tickets')
    output_dir.mkdir(exist_ok=True)
    
    # Generate ticket filename
    ticket_name = idea_path.stem.replace('idea-', 'ticket-') + '.md'
    ticket_path = output_dir / ticket_name
    
    try:
        # Parse idea and create ticket
        idea_data = parse_idea_file(idea_path)
        create_ticket(idea_data, ticket_path)
        
        print(f"✅ Successfully created ticket: {ticket_path}")
        print(f"📝 Headline: {idea_data['headline']}")
        print(f"🏷️  Category: {idea_data['category']}")
        
    except Exception as e:
        print(f"❌ Error creating ticket: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())