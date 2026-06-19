"""Smoke tests for the MCP server's core (no `mcp` dependency required).
Run: python tests/test_quizcore.py   (exit 0 = pass)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mcp"))
import quizcore as q

def main():
    srcs = q.load_sources(); ex = q.load_examples(); meta = q.load_meta()
    assert len(srcs) >= 50, f"only {len(srcs)} sources"
    assert len(ex) >= 50, f"only {len(ex)} examples"
    assert len(meta["domains"]) == 7 and len(meta["formats"]) == 6

    # retrieval returns something for a known topic
    picks = q.rank("dbt retry run_results", srcs, 3)
    assert picks and any(p["id"] == "retry" for p in picks)

    # generation prompt is grounded + version-pinned
    pr = q.gen_prompt("state:modified", "hard", "mcq", picks, q.example_for("mcq", ex))
    assert "SOURCES" in pr and q.VERSION_TARGET in pr

    # present() never leaks the answer; grade() round-trips per format
    checks = 0
    for it in ex:
        f = it["format"]
        pres = q.present(it, "q-test")
        if f == "mcq":
            assert all("correct" not in o for o in pres["options"]), "mcq answer leaked"
            key = {"selected": [o["id"] for o in it["options"] if o["correct"]]}
            assert q.grade(it, key)["correct"]
            assert not q.grade(it, {"selected": []})["correct"]; checks += 1
        elif f == "build_list":
            assert q.grade(it, {"order": it["answer"]["order"]})["correct"]
            assert not q.grade(it, {"order": list(reversed(it["answer"]["order"]))})["correct"]; checks += 1
        elif f == "matching":
            assert q.grade(it, {"pairs": dict(it["key"])})["correct"]; checks += 1
        elif f == "fitb":
            ans = {b["id"]: (b.get("answer") or b["accepted"][0]) for b in it["blanks"]}
            assert q.grade(it, {"blanks": ans})["correct"]; checks += 1
        elif f == "domc":
            resp = {o["text"]: bool(o["correct"]) for o in it["options"][:it.get("present_n", 2)]}
            assert q.grade(it, {"responses": resp})["correct"]; checks += 1
        ok, errs = q.validate_item(it); assert ok, f"{it['id']}: {errs}"
    assert checks >= 5, "did not exercise enough formats"
    print(f"OK — {len(srcs)} sources, {len(ex)} items, {checks} format round-trips, no answer leaks.")

if __name__ == "__main__":
    main()
