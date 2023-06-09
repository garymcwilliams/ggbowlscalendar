"""
test
"""
from ggbowlscalendar.team_manager import TeamManager

DATE1 = '2023-04-22'
DATE2 = '2023-04-30'


class TestTeamManager:
    """
    Tests
    """

    def test_default_content(self):
        """
        tests
        """

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)
        assert team_manager.get_team_details('FALLSA')['name'] == 'AAAA'
        assert team_manager.get_team_details('FALLSA')['location'] \
            == 'AAA location'
        assert team_manager.get_team_details('CLIFT')['name'] == 'clift'
        assert team_manager.get_team_details('CLIFT')['location'] \
            == 'clift location'
