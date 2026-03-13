#!/usr/bin/env python3
"""CLI for pyffice."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="pyffice")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print("pyffice CLI")


if __name__ == "__main__":
    main()
