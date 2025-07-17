import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rug_filters import is_token_safe

def test_safe_token(monkeypatch):
    # Patch get_blacklisted_creators to return an empty list
    monkeypatch.setattr('rug_filters.get_blacklisted_creators', lambda: [])
    token = {
        'liquidity': 2.0,
        'mint_authority': 'renounced',
        'lp_locked': True,
        'creator': 'good_creator'
    }
    assert is_token_safe(token) is True

def test_rug_token(monkeypatch):
    monkeypatch.setattr('rug_filters.get_blacklisted_creators', lambda: ['bad_creator'])
    token = {
        'liquidity': 0.5,
        'mint_authority': 'not_renounced',
        'lp_locked': False,
        'creator': 'bad_creator'
    }
    assert is_token_safe(token) is False