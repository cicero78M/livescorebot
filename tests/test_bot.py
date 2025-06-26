import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import parse_lineups, find_missing_players

SAMPLE_HTML = """
<html>
<div id="lineups">
  <div class="team home">
     <span>Walkup</span><span>PlayerB1</span><span>PlayerB2</span>
  </div>
  <div class="team away">
     <span>Sloukas</span><span>PlayerC1</span><span>PlayerC2</span>
  </div>
</div>
</html>
"""

def test_parse_lineups():
    lineups = parse_lineups(SAMPLE_HTML)
    assert lineups["home"] == ["Walkup", "PlayerB1", "PlayerB2"]
    assert lineups["away"] == ["Sloukas", "PlayerC1", "PlayerC2"]

def test_find_missing_players():
    roster = ["Walkup", "PlayerB1", "PlayerB2", "Extra"]
    lineup = ["Walkup", "PlayerB1", "PlayerB2"]
    missing = find_missing_players(roster, lineup)
    assert missing == ["Extra"]
