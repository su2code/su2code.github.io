"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const html = fs.readFileSync(path.join(__dirname, "../search.html"), "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const pages = [
  { title: "Wall treatment", text: "wall function transition", url: "/SU2/docs_v7/Wall-Treatment/", section: "docs_v7" },
  { title: "Omega", text: "omega equation", url: "/SU2/docs_v7/Turbulence-Models/", section: "docs_v7" }
];

function openSearch(fetch, query = "") {
  const box = { value: "", addEventListener: (_, callback) => { box.run = callback; } };
  const count = { textContent: "" };
  const list = { rows: [], appendChild: row => list.rows.push(row.innerHTML) };
  Object.defineProperty(list, "innerHTML", { set: () => { list.rows = []; } });
  const document = {
    getElementById: id => ({ "search-box": box, "search-count": count, "search-results": list })[id],
    createElement: () => ({ innerHTML: "" })
  };
  vm.runInNewContext(script, { document, fetch, URLSearchParams, location: { search: query } });
  return { box, count, list, search: query => { box.value = query; box.run(); } };
}

const settled = () => new Promise(resolve => setImmediate(resolve));

(async () => {
  let resolve;
  const page = openSearch(() => new Promise(done => { resolve = done; }), "?q=wall+function");
  assert.match(page.count.textContent, /loading/i);
  assert.equal(page.box.value, "wall function");
  page.search("omega");
  assert.match(page.count.textContent, /loading/i);
  resolve({ ok: true, json: () => Promise.resolve(pages) });
  await settled();
  assert.equal(page.box.value, "omega");
  assert.equal(page.count.textContent, "1 page found.");
  assert.match(page.list.rows[0], /Turbulence-Models/);
  page.search("wall function");
  assert.equal(page.count.textContent, "1 page found.");
  assert.match(page.list.rows[0], /Wall-Treatment/);
  page.search("wall omega");
  assert.equal(page.count.textContent, "0 pages found.");
  page.search("k omega");
  assert.equal(page.count.textContent, "1 page found.");
  page.search("k");
  assert.match(page.count.textContent, /at least two characters/i);
  assert.equal(page.list.rows.length, 0);
  page.search("ω");
  assert.match(page.count.textContent, /at least two characters/i);
  page.search("  ");
  assert.equal(page.count.textContent, "");

  const failures = [
    () => Promise.reject(new Error("Network unavailable")),
    () => Promise.resolve({ ok: false, json: () => Promise.resolve([]) }),
    () => Promise.resolve({ ok: true, json: () => Promise.reject(new SyntaxError("Invalid JSON")) }),
    () => Promise.resolve({ ok: true, json: () => Promise.resolve({ error: "No index" }) })
  ];
  for (const fetch of failures) {
    const failed = openSearch(fetch);
    await settled();
    assert.match(failed.count.textContent, /could not load/i);
    failed.search("wall");
    assert.match(failed.count.textContent, /could not load/i);
    assert.equal(failed.list.rows.length, 0);
  }
  console.log("Search checks passed: loading, matching, short queries and four index failures.");
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
