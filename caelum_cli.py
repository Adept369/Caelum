# caelum_cli.py
"""
Caelum CLI — A command-line interface for testing the Caelum AI Assistant.
This script allows you to interact with the LLM using a selected archetype,
with options for auto-detection based on recent mood logs.
"""
import os
import sqlite3
from app.llm import LLMEngine
import openai
from app.config import Config




def main():
    """
    Main function to run the Caelum CLI.
    Prompts the user for input and outputs the response from the LLM.
    """
    llm = LLMEngine()



    print("🧠 Caelum CLI is ready for development testing.")
    



if __name__ == "__main__":
    main()
