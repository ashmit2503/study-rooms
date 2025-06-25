#!/usr/bin/env python
"""
Django SECRET_KEY generator utility.

Usage: python contrib/secret_gen.py
"""

from django.utils.crypto import get_random_string

chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
print(get_random_string(50, chars))
