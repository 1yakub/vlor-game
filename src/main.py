"""Main entry point for the game.

This script serves as the entry point for starting the game.
It handles initialization and any command line arguments.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.append(str(src_dir.parent))

from client.game import main as game_main
from shared.logger import get_logger

logger = get_logger(__name__)

def parse_args():
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Varygen: Lords of Resolution")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    return parser.parse_args()

def main():
    """Main entry point."""
    try:
        args = parse_args()
        if args.debug:
            logger.setLevel("DEBUG")
        
        logger.info("Starting Varygen: Lords of Resolution")
        game_main()
        
    except Exception as e:
        logger.exception("Game failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main() 