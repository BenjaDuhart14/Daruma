#!/usr/bin/env python3
"""
Generate a bcrypt password hash for Daruma authentication.

Usage:
    python generate_password_hash.py

This will prompt you to enter a password and output the bcrypt hash.
Copy this hash to your Streamlit secrets:

    [auth]
    email = "your@email.com"
    password_hash = "$2b$12$..."  # paste hash here
"""

import bcrypt
import getpass


def generate_hash():
    """Generate a bcrypt hash for a password."""
    print("\n🔐 Daruma Password Hash Generator\n")
    print("=" * 40)
    
    # Get password securely (hidden input)
    password = getpass.getpass("Enter your password: ")
    confirm = getpass.getpass("Confirm password: ")
    
    if password != confirm:
        print("\n❌ Passwords don't match!")
        return
    
    if len(password) < 8:
        print("\n⚠️  Warning: Password is less than 8 characters.")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Generate hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  # Cost factor of 12 (good balance)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    print("\n" + "=" * 40)
    print("✅ Password hash generated successfully!\n")
    print("Add this to your Streamlit secrets:\n")
    print("```toml")
    print("[auth]")
    print('email = "your@email.com"')
    print(f'password_hash = "{hashed.decode()}"')
    print("```")
    print("\n" + "=" * 40)
    print("⚠️  IMPORTANT: Never share your password hash publicly!")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    generate_hash()
