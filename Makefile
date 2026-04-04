.PHONY: help install setup clean run test lint format

help:
	@echo "Available targets:"
	@echo "  make install    - Install/setup the project"
	@echo "  make setup      - Setup and copy files to ~/.claude"
	@echo "  make run        - Run the project"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Lint the code"
	@echo "  make format     - Format the code"
	@echo "  make clean      - Clean up artifacts"
	@echo "  make help       - Show this help message"

install: setup
	@echo "✓ Installation complete"

setup:
	@mkdir -p ~/.claude
	@cp -r agents commands hooks.settings.json skills ~/.claude
	@echo "✓ Files copied to ~/.claude"

run:
	@echo "Running the project..."

test:
	@echo "Running tests..."

lint:
	@echo "Linting code..."

format:
	@echo "Formatting code..."

clean:
	@echo "Cleaning up..."
	@rm -rf ~/.claude/agents ~/.claude/commands ~/.claude/hooks.settings.json ~/.claude/skills 2>/dev/null || true
	@echo "✓ Cleanup complete"