# -*- coding: utf-8 -*-

from link_migration.views import TerminalMessages
from unittestcase import UnitTestCase
from link_migration.model import DiscovererMigration, MigrationWrapper
from example_migrations import hello_world


class TestTerminalMessages(UnitTestCase):

    def test_should_get_message_of_current_version(self):
        migrations = DiscovererMigration()
        terminal_message = TerminalMessages(migrations=migrations)
        with self.get_stdout() as stdout:
            terminal_message.current_version()
        self.assertEqual("0.0.1\n", stdout.getvalue())

    def test_should_return_message_up(self):
        migration = MigrationWrapper(hello_world)
        message = TerminalMessages(DiscovererMigration())
        with self.get_stdout() as stdout:
            message.make_message("up", migration)
        self.assertTextEqual("""
0.0.1           - hello_world.py
                  migrate all the world of test
                  greetings world
                  up - HeLo World
                       and migrate the world
""", stdout.getvalue())

    def test_should_return_message_down(self):
        migration = MigrationWrapper(hello_world)
        message = TerminalMessages(DiscovererMigration())
        with self.get_stdout() as stdout:
            message.make_message("down", migration)
        self.assertTextEqual("""
0.0.1           - hello_world.py
                  migrate all the world of test
                  greetings world
                  down - roolback the world
""", stdout.getvalue())

    def test_should_return_message_error_of_up(self):
        migration = MigrationWrapper(hello_world)
        message = TerminalMessages(DiscovererMigration())
        with self.get_stdout() as stdout:
            message.error_message("up", migration, "AttributeError")
        self.assertTextEqual("""
\x1b[31m\n0.0.1           - hello_world.py
                  migrate all the world of test
                  greetings world
                  up - HeLo World
                       and migrate the world

AttributeError\x1b[0m
""".strip(), stdout.getvalue().strip())

    def test_should_return_message_error_of_down(self):
        migration = MigrationWrapper(hello_world)
        message = TerminalMessages(DiscovererMigration())
        with self.get_stdout() as stdout:
            message.error_message("down", migration, "AttributeError")
        self.assertTextEqual("""
\x1b[31m\n0.0.1           - hello_world.py
                  migrate all the world of test
                  greetings world
                  down - roolback the world

AttributeError\x1b[0m
""".strip(), stdout.getvalue().strip())