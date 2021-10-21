# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.trial import unittest

from buildbot.process.results import SUCCESS
from buildbot.steps.source import gerrit
from buildbot.test.fake.remotecommand import ExpectListdir
from buildbot.test.fake.remotecommand import ExpectShell
from buildbot.test.fake.remotecommand import ExpectStat
from buildbot.test.util import config
from buildbot.test.util import sourcesteps
from buildbot.test.util.misc import TestReactorMixin


class TestGerrit(sourcesteps.SourceStepMixin, config.ConfigErrorsMixin,
                 TestReactorMixin, unittest.TestCase):

    def setUp(self):
        self.setUpTestReactor()
        return self.setUpSourceStep()

    def tearDown(self):
        return self.tearDownSourceStep()

    def test_mode_full_clean(self):
        self.setup_step(
            gerrit.Gerrit(repourl='http://github.com/buildbot/buildbot.git',
                          mode='full', method='clean'))
        self.build.setProperty("event.change.project", "buildbot")
        self.sourcestamp.project = 'buildbot'
        self.build.setProperty("event.patchSet.ref", "gerrit_branch")

        self.expectCommands(
            ExpectShell(workdir='wkdir',
                        command=['git', '--version'])
            .stdout('git version 1.7.5')
            .exit(0),
            ExpectStat(file='wkdir/.buildbot-patched', logEnviron=True)
            .exit(1),
            ExpectListdir(dir='wkdir')
            .update('files', ['.git'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'clean', '-f', '-f', '-d'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'fetch', '-f', '-t',
                                 'http://github.com/buildbot/buildbot.git',
                                 'gerrit_branch', '--progress'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-f', 'FETCH_HEAD'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-B', 'gerrit_branch'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'rev-parse', 'HEAD'])
            .stdout('f6ad368298bd941e934a41f3babc827b2aa95a1d')
            .exit(0)
        )
        self.expectOutcome(result=SUCCESS)
        self.expectProperty(
            'got_revision', 'f6ad368298bd941e934a41f3babc827b2aa95a1d', 'Gerrit')
        return self.runStep()

    def test_mode_full_clean_force_build(self):
        self.setup_step(
            gerrit.Gerrit(repourl='http://github.com/buildbot/buildbot.git',
                          mode='full', method='clean'))
        self.build.setProperty("event.change.project", "buildbot")
        self.sourcestamp.project = 'buildbot'
        self.build.setProperty("gerrit_change", "1234/567")

        self.expectCommands(
            ExpectShell(workdir='wkdir',
                        command=['git', '--version'])
            .stdout('git version 1.7.5')
            .exit(0),
            ExpectStat(file='wkdir/.buildbot-patched', logEnviron=True)
            .exit(1),
            ExpectListdir(dir='wkdir')
            .update('files', ['.git'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'clean', '-f', '-f', '-d'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'fetch', '-f', '-t',
                                 'http://github.com/buildbot/buildbot.git',
                                 'refs/changes/34/1234/567', '--progress'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-f', 'FETCH_HEAD'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-B', 'refs/changes/34/1234/567'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'rev-parse', 'HEAD'])
            .stdout('f6ad368298bd941e934a41f3babc827b2aa95a1d')
            .exit(0)
        )
        self.expectOutcome(result=SUCCESS)
        self.expectProperty(
            'got_revision', 'f6ad368298bd941e934a41f3babc827b2aa95a1d', 'Gerrit')
        return self.runStep()

    def test_mode_full_clean_force_same_project(self):
        self.setup_step(
            gerrit.Gerrit(repourl='http://github.com/buildbot/buildbot.git',
                          mode='full', method='clean', codebase='buildbot'))
        self.build.setProperty("event.change.project", "buildbot")
        self.sourcestamp.project = 'buildbot'
        self.build.setProperty("gerrit_change", "1234/567")

        self.expectCommands(
            ExpectShell(workdir='wkdir',
                        command=['git', '--version'])
            .stdout('git version 1.7.5')
            .exit(0),
            ExpectStat(file='wkdir/.buildbot-patched', logEnviron=True)
            .exit(1),
            ExpectListdir(dir='wkdir')
            .update('files', ['.git'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'clean', '-f', '-f', '-d'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'fetch', '-f', '-t',
                                 'http://github.com/buildbot/buildbot.git',
                                 'refs/changes/34/1234/567', '--progress'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-f', 'FETCH_HEAD'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-B', 'refs/changes/34/1234/567'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'rev-parse', 'HEAD'])
            .stdout('f6ad368298bd941e934a41f3babc827b2aa95a1d')
            .exit(0)
        )
        self.expectOutcome(result=SUCCESS)
        self.expectProperty(
            'got_revision', {'buildbot': 'f6ad368298bd941e934a41f3babc827b2aa95a1d'}, 'Gerrit')
        return self.runStep()

    def test_mode_full_clean_different_project(self):
        self.setup_step(
            gerrit.Gerrit(repourl='http://github.com/buildbot/buildbot.git',
                          mode='full', method='clean', codebase='buildbot'))
        self.build.setProperty("event.change.project", "buildbot")
        self.sourcestamp.project = 'not_buildbot'
        self.build.setProperty("gerrit_change", "1234/567")

        self.expectCommands(
            ExpectShell(workdir='wkdir',
                        command=['git', '--version'])
            .stdout('git version 1.7.5')
            .exit(0),
            ExpectStat(file='wkdir/.buildbot-patched', logEnviron=True)
            .exit(1),
            ExpectListdir(dir='wkdir')
            .update('files', ['.git'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'clean', '-f', '-f', '-d'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'fetch', '-f', '-t',
                                 'http://github.com/buildbot/buildbot.git',
                                 'HEAD', '--progress'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'checkout', '-f', 'FETCH_HEAD'])
            .exit(0),
            ExpectShell(workdir='wkdir',
                        command=['git', 'rev-parse', 'HEAD'])
            .stdout('f6ad368298bd941e934a41f3babc827b2aa95a1d')
            .exit(0)
        )
        self.expectOutcome(result=SUCCESS)
        return self.runStep()
