# -*- coding: utf-8 -*-

from link_migration import example_migrations
import inspect

from os.path import basename
from importlib import import_module
from modulefinder import ModuleFinder

from types import MethodType


class DiscovererMigration(object):

    def __init__(self, execute=True, version_to=0, config=None, **kwargs):
        self.execute = execute
        self.version_to = int(version_to)
        self.current_version = config.get_current_version()
        self.config = config

        self.migrate_types = {
            'upgrade': self.up_migrations,
            'downgrade': self.down_migrations,
            'specified': self.migrate_version
        }

        self.downgrade = 'downgrade'
        self.upgrade = 'upgrade'
        self.specified = 'specified'
        self.migrate_type = None

    def migrations(self, migrate_type):
        self.migrate_type = migrate_type
        return self.migrate_types[migrate_type]()

    def migrate_version(self):
        if self.is_up():
            return self.up_migrations()
        if self.is_down():
            return self.down_migrations()

        return []

    def down_migrations(self):
        for migration_file in self.migrations_files(reverse=True):
            migration = MigrationWrapper(migration_file, execute=self.execute, config=self.config)
            if self.current_version >= migration.version >= self.version_to:
                yield migration

    def up_migrations(self):
        for migration_file in self.migrations_files():
            migration = MigrationWrapper(migration_file,  execute=self.execute, config=self.config)
            if self.current_version < migration.version <= self.version_to:
                yield migration

    def migrations_files(self, reverse=False):
        # List comprehension import for each migration file and inline sort based on version
        submodules = sorted(
            [
                import_module(f'{self.config.MIGRATIONS_DIR}.{name}')
                for name in ModuleFinder().find_all_submodules(import_module(self.config.MIGRATIONS_DIR))
                if self._submodule_name_valid(name)
            ],
            key=lambda s: s.version,  # use version property for sorting
            reverse=reverse
        )
        if not len(submodules):
            self.version_to = self.current_version
            return []

        if not self.migrate_type == self.specified:
            self.version_to = submodules[-1].version

        # Check for duplicate version numbers, fail if found
        versions = set()
        if any(s.version in versions or versions.add(s.version) for s in submodules):
            versions = set()
            raise Exception(
                'Duplicate version numbers %s' % (
                    list(set(
                        s.version for s in submodules if s.version in versions or versions.add(s.version)
                    ))
                )
            )

        return submodules

    def _submodule_name_valid(self, name):
        return not (name.startswith('.') or  name.startswith('_') or name == "conf")

    def is_up(self):
        return self.version_to > self.current_version

    def is_down(self):
        return self.version_to < self.current_version


class MigrationWrapper(object):

    def __init__(self, migration_file, execute=True, config=None):
        self.up = MethodType(migration_file.up, self)
        self.down = MethodType(migration_file.down, self)
        self.migration_file = migration_file
        self.execute = execute
        self.config = config

    def __repr__(self):
        return self.filename()

    def __eq__(self, migration):
        return self.migration_file == migration.migration_file

    def upgrade(self):
        if self.execute:
            try:
                self.up()
            except TypeError as e:
                self.migration_file.up()
            self.config.set_current_version(self.version)

    def downgrade(self):
        if self.execute:
            try:
                self.down()
            except TypeError as e:
                self.migration_file.down()
            self.config.set_current_version(self.version)

    def header(self):
        if inspect.getdoc(self.migration_file):
            return inspect.getdoc(self.migration_file)
        else:
            return "No docstring found"

    def doc_up(self):
        if inspect.getdoc(self.migration_file.up):
            return inspect.getdoc(self.migration_file.up)
        else:
            return "No upgrade docstring found"

    def doc_down(self):
        if inspect.getdoc(self.migration_file.down):
            return inspect.getdoc(self.migration_file.down)
        else:
            return "No downgrade docstring found"

    @property
    def version(self):
        return self.migration_file.version

    def filename(self):
        return basename(self.migration_file.__file__.replace('.pyc', '.py'))
