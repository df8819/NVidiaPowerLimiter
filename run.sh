#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The command to run in the new terminal
CMD="cd \"$SCRIPT_DIR\" && sudo python3 nvidia_power_limiter.py"

# List of common terminal emulators
TERMINALS=(
    "konsole"
    "gnome-terminal"
    "xfce4-terminal"
    "xterm"
    "mate-terminal"
    "lxterminal"
    "tilix"
    "alacritty"
    "urxvt"
    "kitty"
    "terminator"
    "deepin-terminal"
    "qterminal"
    "st"
    "eterm"
    "roxterm"
    "guake"
    "tilda"
    "hyper"
)

# Find the first available terminal emulator
for term in "${TERMINALS[@]}"; do
    if command -v "$term" &> /dev/null; then
        TERMINAL="$term"
        break
    fi
done

if [ -z "$TERMINAL" ]; then
    echo "No supported terminal emulator found. Please run this script from your terminal."
    exit 1
fi

# Use the user's default shell, fallback to bash
USER_SHELL="${SHELL:-/bin/bash}"

# Launch the terminal with the command
case "$TERMINAL" in
    konsole)
        "$TERMINAL" --title="NVIDIA Power Limiter" -e "$USER_SHELL" -c "$CMD"
        ;;
    gnome-terminal|tilix|mate-terminal|terminator|deepin-terminal|qterminal|hyper)
        "$TERMINAL" -- "$USER_SHELL" -c "$CMD"
        ;;
    xfce4-terminal)
        "$TERMINAL" --hold -e "$USER_SHELL" -c "$CMD"
        ;;
    xterm|lxterminal|alacritty|urxvt|kitty|st|eterm|roxterm|tilda|guake)
        "$TERMINAL" -e "$USER_SHELL" -c "$CMD"
        ;;
    *)
        echo "Terminal emulator $TERMINAL is not supported in this script."
        exit 1
        ;;
esac
