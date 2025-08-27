"""
test custom Django management command
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

""" utiliser le decorateur @patch pour mocker le comportement de la BD,
    la methode check contenu dans BaseCommande
    nous permet de v/rifier letat de la bd"""


@patch('core.management.commands.wait_for_db.Command.check')
class commandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """ le fait dajouter le decorateur nous oblige a
            le passer en parametre de la methode """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
