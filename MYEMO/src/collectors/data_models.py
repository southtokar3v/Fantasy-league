from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class GeneralStanding:
    date: str
    team: str
    total_rank: int
    average_rank: int
    total_points: float
    average_points: float
    prev_day_diff: float
    important_event: Optional[str] = None

@dataclass
class StatStanding:
    date: str
    team: str
    stat_name: str  # PTS, REB, AST, etc.
    daily_total: float
    daily_average: float
    stat_rank: int
    prev_day_diff: float
    annotation: Optional[str] = None

@dataclass
class RosterHistory:
    date: str
    team: str
    player: str
    status: str  # active/bench/IR
    origin: str  # drafted/FA/Trade
    arrival_date: str
    departure_date: Optional[str] = None
    annotation: Optional[str] = None

@dataclass
class PlayerTracking:
    date: str
    player: str
    fantasy_team: str
    nba_opponent: Optional[str]
    points: float
    rebounds: float
    assists: float
    blocks: float
    threes_made: float
    status: str  # INJ/GTD/active/bench
    game_played: bool
    injury_status: Optional[str]
    next_game: Optional[str]
    back_to_back: bool
    change_source: Optional[str] = None

@dataclass
class FreeAgentMarket:
    date: str
    player: str
    nba_team: str
    last_week_stats: dict
    rolling_14d_stats: dict
    rolling_30d_stats: dict
    roster_percentage: float
    start_percentage: float
    team_fit_score: Optional[float] = None
    pickup_stats: Optional[dict] = None
    annotation: Optional[str] = None
