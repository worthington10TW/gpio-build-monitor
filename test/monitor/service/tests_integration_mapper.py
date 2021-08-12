#!/usr/bin/env python3

import unittest
import pytest
from unittest import mock

import monitor.ci_gateway.constants as cons
from monitor.service.integration_mapper import IntegrationMapper, MismatchError
from monitor.ci_gateway import integration_actions as available_integrations


class IntegrationMapperTests(unittest.TestCase):
    def test_fails_when_integration_is_unknown(self):
        integrations = {
            dict(type='BLURGH', username='meee', repo='super-repo')
        }

        with pytest.raises(MismatchError) as excinfo:
            IntegrationMapper(
                available_integrations.get_all()).get(integrations)

        msg = 'Integration error: we currently do not integrate with BLURGH.'  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))

    def test_maps_correct_function(self):
        integrations = {
            dict(type='GITHUB', username='meee', repo='super-repo'),
            dict(type='GITHUB', username='you', repo='another-repo')
        }
        result = IntegrationMapper(integrations, 1).get()
        self.assertEqual(2, len(result))
        [self.assertEqual(
            cons.IntegrationType.GITHUB, r['type']) for r in result]
        [self.assertIsNotNone(r['action']) for r in result]

    @mock.patch('monitor.ci_gateway.github.CircleCI')
    @mock.patch('monitor.ci_gateway.github.GitHubAction')
    def test_executes_correct_function(self,
                                       mocked_git_action,
                                       mocked_circle_ci):
        integrations = [
            dict(type='GITHUB', username='meee', repo='super-repo'),
            dict(type='GITHUB', username='you', repo='another-repo'),
            dict(type='CIRCLECI', username='them', repo='special-repo')
        ]

        mocked_git_action.return_value.get_latest = mock.MagicMock()  # noqa: E501
        mocked_circle_ci.return_value.get_latest = mock.MagicMock()  # noqa: E501

        result = IntegrationMapper(available_integrations.get_all())\
            .get(integrations)

        self.assertEqual(2, mocked_git_action.call_count)
        self.assertEqual(mock.call('meee', 'super-repo'),
                         mocked_git_action.call_args_list[0])
        self.assertEqual(mock.call('you', 'another-repo'),
                         mocked_git_action.call_args_list[1])
        self.assertEqual(mock.call('them', 'special-repo'),
                         mocked_circle_ci.call_args_list[1])

        mocked_git_action.return_value.get_latest.assert_not_called()
        result[0]['action']()
        self.assertEqual(1,
                         mocked_git_action.return_value.get_latest.call_count)
        result[1]['action']()
        self.assertEqual(2,
                         mocked_git_action.return_value.get_latest.call_count)
        result[2]['action']()
        self.assertEqual(1,
                         mocked_circle_ci.return_value.get_latest.call_count)

        # Asserting that setup is only called once
        self.assertEqual(2, mocked_git_action.call_count)


if __name__ == '__main__':
    unittest.main()
