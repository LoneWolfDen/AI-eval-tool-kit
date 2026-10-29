import copy
import json
import re

import pytest

from tools.load_data import MapDataError, validate_map
from tools.render_html import render_html
from tools.render_markdown import render_markdown


def test_real_data_is_valid_and_has_five_stages(map_data):
    assert [s["id"] for s in map_data["stages"]] == ["basics", "evals", "agents", "privacy", "team"]


def test_every_stage_has_a_start_here_stop(map_data):
    for stage in map_data["stages"]:
        assert any(r["tier"] == "start" for r in stage["resources"]), stage["id"]


def test_external_links_are_https_and_internal_ones_are_relative(map_data):
    for stage in map_data["stages"]:
        for resource in stage["resources"]:
            if resource.get("internal"):
                assert resource["url"].startswith("../")
            else:
                assert resource["url"].startswith("https://")


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda d: d["stages"][0]["resources"][0].update(type="video"), "type must be one of"),
        (lambda d: d["stages"][0]["resources"][0].update(tier="later"), "tier must be one of"),
        (lambda d: d["stages"][0]["resources"][0].update(url="http://insecure.example"), "https://"),
        (lambda d: d["stages"][0]["resources"][0].pop("note"), "missing: note"),
        (lambda d: d["stages"][1]["resources"][0].update(id="prompt-tutorial"), "duplicate id"),
        (lambda d: d["stages"].clear(), "at least one stage"),
    ],
)
def test_bad_data_is_rejected_with_a_clear_message(map_data, mutate, message):
    broken = copy.deepcopy(map_data)
    mutate(broken)
    with pytest.raises(MapDataError, match=message):
        validate_map(broken)


def test_html_is_self_contained_and_embeds_valid_json(map_data):
    html = render_html(map_data)
    assert "{{" not in html  # every placeholder was filled
    assert "<link" not in html and "src=" not in html  # no external requests

    embedded = re.search(r'<script type="application/json" id="map-data">(.*?)</script>', html, re.S).group(1)
    assert json.loads(embedded)["title"] == map_data["title"]


def test_json_in_script_tag_cannot_close_the_tag(map_data):
    map_data = copy.deepcopy(map_data)
    map_data["stages"][0]["goal"] = "evil </script><b>x</b>"
    html = render_html(map_data)
    embedded = re.search(r'<script type="application/json" id="map-data">(.*?)</script>', html, re.S).group(1)
    assert "</script" not in embedded
    assert json.loads(embedded)["stages"][0]["goal"] == "evil </script><b>x</b>"


def test_markdown_lists_every_resource_link(map_data):
    text = render_markdown(map_data)
    for stage in map_data["stages"]:
        assert f"## {stage['title']}" in text
        for resource in stage["resources"]:
            assert f"]({resource['url']})" in text
