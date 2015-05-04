#! /usr/bin/env python

from app import create_app


manager = create_app()

if __name__ == '__main__':
    manager.run()
