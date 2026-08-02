from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.build import (
    aggregate_refs,
    item_badges,
    render_item_detail,
    render_relation_tree,
    validate_asset_filename,
    validate_item_id,
    write_page,
)
from scripts.verify import expected_relation_labels


class ItemTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.items = {
            "1004": {"_id": "1004", "name": "요정의 부적", "image": {"full": "1004.png"}, "gold": {"base": 125, "total": 125, "purchasable": True}},
            "3028": {"_id": "3028", "name": "조화의 성배", "image": {"full": "3028.png"}, "gold": {"base": 100, "total": 880, "purchasable": True}, "from": ["1004", "1033", "1004"], "into": []},
            "loop": {"_id": "loop", "name": "순환 표본", "image": {"full": "loop.png"}, "gold": {}, "from": ["loop"]},
        }

    def test_aggregate_refs_preserves_order_and_counts_duplicates(self) -> None:
        self.assertEqual(aggregate_refs(["1004", "1033", "1004"]), [("1004", 2), ("1033", 1)])

    def test_badges_report_map_restrictions_and_unpurchasable(self) -> None:
        badges = item_badges({"maps": {"1": True, "8": False}, "gold": {"purchasable": False}})
        self.assertIn("구매 불가", badges)
        self.assertIn("맵 8 제외", badges)

    def test_node_accessible_name_includes_data_badges(self) -> None:
        items = {
            "2009": {
                "_id": "2009",
                "name": "특수 아이템",
                "image": {"full": "2009.png"},
                "gold": {"base": 0, "total": 0, "purchasable": False},
                "maps": {"8": False},
            }
        }
        rendered = render_relation_tree(["2009"], items, "from")
        self.assertIn("배지: 구매 불가, 맵 8 제외", rendered)

    def test_node_reads_purchase_status_from_gold(self) -> None:
        rendered = render_relation_tree(["1004"], self.items, "from")
        self.assertIn("구매 가능", rendered)

    def test_tree_reports_missing_reference_without_fabricating_item(self) -> None:
        rendered = render_relation_tree(["missing"], self.items, "from")
        self.assertIn("데이터 없음", rendered)
        self.assertIn("missing", rendered)

    def test_tree_stops_cycle_with_visited_set(self) -> None:
        rendered = render_relation_tree(["loop"], self.items, "from", visited=frozenset({"loop"}))
        self.assertIn("순환 관계 중단", rendered)
        self.assertEqual(expected_relation_labels(["loop"], self.items, "from", visited=frozenset({"loop"})), [])

    def test_tree_stops_at_maximum_depth(self) -> None:
        rendered = render_relation_tree(["1004"], self.items, "from", depth=8, max_depth=8)
        self.assertIn("최대 깊이 도달", rendered)

    def test_tree_renders_duplicate_quantity_once(self) -> None:
        rendered = render_relation_tree(["1004", "1004"], self.items, "from")
        self.assertEqual(rendered.count("<strong>요정의 부적</strong>"), 1)
        self.assertIn("×2", rendered)
        self.assertIn('aria-label="요정의 부적 2개 필요 아이템 ID 1004 총 가격 125 · 조합 비용 125 구매 가능"', rendered)

    def test_detail_separates_material_current_and_upgrade_stages(self) -> None:
        rendered = render_item_detail(self.items["3028"], self.items)
        self.assertIn("하위 조합 재료", rendered)
        self.assertIn("현재 아이템", rendered)
        self.assertIn("상위 업그레이드", rendered)
        self.assertIn("상위 업그레이드 없음", rendered)
        self.assertIn("×2", rendered)
        self.assertIn('role="group"', rendered)
        self.assertIn('aria-label="조화의 성배 아이템 ID 3028 총 가격 880 · 조합 비용 100 구매 가능"', rendered)

    def test_item_id_rejects_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            validate_item_id("../../../escape")

    def test_asset_filename_rejects_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            validate_asset_filename("../../escape.png")

    def test_write_page_rejects_destination_outside_site(self) -> None:
        with TemporaryDirectory() as temp_dir, patch("scripts.build.SITE", Path(temp_dir) / "site"):
            with self.assertRaises(ValueError):
                write_page("/../../escape", "unsafe")


if __name__ == "__main__":
    unittest.main()
