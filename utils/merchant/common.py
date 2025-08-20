from typing import Optional, List
import json

from models.schema import ScoreSummary


def _as_list(risk_tags_text: Optional[str]) -> List[str]:
    if not risk_tags_text:
        return []
    try:
        v = json.loads(risk_tags_text)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _to_score_summary_list(latest_row) -> ScoreSummary:
    return ScoreSummary(
        score=latest_row.score,
        tier=latest_row.tier,
        decision=latest_row.decision,
        limit_suggestion=latest_row.limit_suggestion,
        risk_tags=_as_list(latest_row.risk_tags),
        explanation=latest_row.explanation,
        heat_score=latest_row.heat_score,
        created_at=latest_row.created_at,
    )
