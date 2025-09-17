#!/bin/bash
# Batch convert all ideas to tickets

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IDEAS_DIR="$PROJECT_ROOT/ideas"
TICKETS_DIR="$PROJECT_ROOT/tickets"

echo "🚀 Converting all ideas to tickets..."
echo

# Create tickets directory if it doesn't exist
mkdir -p "$TICKETS_DIR"

# Convert each idea file
converted=0
for idea_file in "$IDEAS_DIR"/idea-*.md; do
    if [ -f "$idea_file" ]; then
        echo "📝 Converting: $(basename "$idea_file")"
        python3 "$SCRIPT_DIR/ideas_to_tickets.py" "$idea_file"
        ((converted++))
        echo
    fi
done

if [ $converted -eq 0 ]; then
    echo "❌ No idea files found in $IDEAS_DIR"
    echo "💡 Create idea files using the template: templates/idea-template.md"
else
    echo "✅ Successfully converted $converted idea(s) to tickets!"
    echo "📁 Tickets saved in: $TICKETS_DIR"
fi