#!/bin/bash

set -e

ANTHROPIC_KEY="$1"

# Install or update llm
FRESH_INSTALL=false
if command -v llm &> /dev/null; then
    echo "llm is already installed."
    read -p "Would you like to update it? [y/N] " update_llm
    if [[ "$update_llm" =~ ^[Yy]$ ]]; then
        echo "Updating llm..."
        uv tool upgrade llm
    fi
else
    echo "Installing llm..."
    uv tool install llm
    FRESH_INSTALL=true
fi

# Install anthropic plugin
llm install llm-anthropic

# Set anthropic key if provided
if [ -n "$ANTHROPIC_KEY" ]; then
    llm keys set anthropic --value "$ANTHROPIC_KEY"
fi

# Run template setup scripts
for script in templates/*.sh; do
    if [ -f "$script" ]; then
        echo "Running $script..."
        bash "$script"
    fi
done

# Interactive alias setup for each template
echo ""
echo "Setting up aliases for llm templates..."

for template in $(llm templates | awk '{print $1}'); do
    read -p "Add alias for '$template' template to ~/.bashrc? [y/N] " add_alias
    if [[ "$add_alias" =~ ^[Yy]$ ]]; then
        read -p "Alias name [$template]: " alias_name
        alias_name="${alias_name:-$template}"

        read -p "Model to use [claude-haiku-4.5]: " model_name
        model_name="${model_name:-claude-haiku-4.5}"

        ALIAS_LINE="alias $alias_name='llm -t $template -m $model_name'"

        if ! grep -qF "alias $alias_name=" ~/.bashrc; then
            echo "" >> ~/.bashrc
            echo "# llm $template template alias" >> ~/.bashrc
            echo "$ALIAS_LINE" >> ~/.bashrc
            echo "Added '$alias_name' alias to ~/.bashrc"
        else
            echo "Alias '$alias_name' already exists in ~/.bashrc, skipping"
        fi
    fi
done

echo ""
echo "Setup complete. Run 'source ~/.bashrc' to load new aliases."

if [ -z "$ANTHROPIC_KEY" ] && [ "$FRESH_INSTALL" = true ]; then
    echo ""
    echo -e "\033[33mNOTE:\033[0m No API key was provided. Set your Anthropic key with \`llm keys set anthropic\`"
fi
