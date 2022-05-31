import json

SPLIT_TYPE_DICT = {
    "TypA": {"split_var": [{"vaa10": "ao1"}], "timestamp_var": "vaa11splitDate"},
    "TypB": {"split_var": [{"vaa12": "ao1"}], "timestamp_var": "vaa13splitDate"},
    "TypC": {"split_var": [{"vaa14": "ao1"}], "timestamp_var": "vaa15splitDate"}
}

# JSON_ARRAY_01: regular episode
JSON_ARRAY_01 = json.loads("""[
    {
    "id": "0",
    "startDate": "2017-12-01T01-00-00.000Z",
    "endDate": "2020-05-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot2",
    "flags": [],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa10": "ao1",
    "vaa11splitDate": "2019-02-01T01-00-00.000Z",
    "vaa02": "a04",
    "vaa12": "ao1",
    "vaa13splitDate": "2019-01-01T01-00-00.000Z",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao1",
    "vaa15splitDate": "2019-01-01T01-00-00.000Z",
    "vaa05": "Ein Blindtext hier 123."
    }
    ]""")

JSON_ARRAY_01_1st_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "currentSplit": ["TypB", "TypC"],
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "splitStack": {"2019-02-01T01-00-00.000Z": ["TypA"]},
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "new",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  }
  ]""")

JSON_ARRAY_01_2nd_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["2"],
  "endDate": "2019-01-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "currentSplit": ["TypA"],
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "2",
  "parent": "1",
  "startDate": "2019-02-01T01-00-00.000Z",
  "state": "new",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  }
  ]""")

JSON_ARRAY_01_max_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["2"],
  "endDate": "2019-01-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "currentSplit": ["TypA"],
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "2",
  "parent": "1",
  "startDate": "2019-02-01T01-00-00.000Z",
  "state": "new",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  }
  ]""")

JSON_ARRAY_01_modifed_2nd_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {"children": ["2"],
  "endDate": "2019-01-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "currentSplit": ["TypA", "TypC"],
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "2",
  "parent": "1",
  "splitStack": {"2019-04-01T01-00-00.000Z": ["TypA"]},
  "startDate": "2019-02-01T01-00-00.000Z",
  "state": "new",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  }
  ]""")

JSON_ARRAY_01_modifed_3rd_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["2"],
  "endDate": "2019-01-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["3"],
  "endDate": "2019-03-31T01-00-00.000Z",
  "flags": [],
  "id": "2",
  "parent": "1",
  "startDate": "2019-02-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123.",
  "vaa12": "ao2"
  },
  {
  "currentSplit": ["TypA"],
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "3",
  "parent": "2",
  "startDate": "2019-04-01T01-00-00.000Z",
  "state": "new",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123.",
  "vaa12": "ao2"
  }
  ]""")

JSON_ARRAY_01_modified_max_split = json.loads("""[
  {
  "children": ["1"],
  "endDate": "2018-12-31T01-00-00.000Z",
  "flags": [],
  "id": "0",
  "startDate": "2017-12-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["2"],
  "endDate": "2019-01-31T01-00-00.000Z",
  "flags": [],
  "id": "1",
  "parent": "0",
  "startDate": "2019-01-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123."
  },
  {
  "children": ["3"],
  "endDate": "2019-03-31T01-00-00.000Z",
  "flags": [],
  "id": "2",
  "parent": "1",
  "startDate": "2019-02-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123.",
  "vaa12": "ao2"
  },
  {
  "endDate": "2020-05-31T01-00-00.000Z",
  "flags": [],
  "id": "3",
  "parent": "2",
  "startDate": "2019-04-01T01-00-00.000Z",
  "state": "done",
  "type": "Slot2",
  "vaa00": "ao2",
  "vaa01": "Blindtext dort 987.",
  "vaa02": "a04",
  "vaa03": "MISSING",
  "vaa04": "425",
  "vaa05": "Ein Blindtext hier 123.",
  "vaa12": "ao2"
  }
  ]""")

# JSON_ARRAY_02: second split timestamp "vaa13splitDate" lies out of episode
JSON_ARRAY_02 = json.loads("""[
    {
    "id": "0",
    "startDate": "2017-12-01T01-00-00.000Z",
    "endDate": "2020-05-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot2",
    "flags": ["eHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa10": "ao1",
    "vaa11splitDate": "2017-02-01T01-00-00.000Z",
    "vaa02": "a04",
    "vaa12": "ao1",
    "vaa13splitDate": "2021-01-01T01-00-00.000Z",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao1",
    "vaa15splitDate": "2019-01-01T01-00-00.000Z",
    "vaa05": "Ein Blindtext hier 123."
    }]""")

# JSON_ARRAY_03: last split var is "vaa14": "ao2", not "ao1"
JSON_ARRAY_03 = json.loads("""[
    {
    "id": "0",
    "startDate": "2017-12-01T01-00-00.000Z",
    "endDate": "2020-05-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot2",
    "flags": ["sHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa10": "ao1",
    "vaa11splitDate": "2019-02-01T01-00-00.000Z",
    "vaa02": "a04",
    "vaa12": "ao2",
    "vaa13splitDate": "2019-01-01T01-00-00.000Z",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao2",
    "vaa15splitDate": "2019-01-01T01-00-00.000Z",
    "vaa05": "Ein Blindtext hier 123."
    }
    ]""")

# JSON_ARRAY_04: both flags "sHO" and "eHO" set for first episode
JSON_ARRAY_04 = json.loads("""[
    {
    "id": "0",
    "startDate": "2017-12-01T01-00-00.000Z",
    "endDate": "2020-05-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot2",
    "flags": ["sHO", "eHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa10": "ao1",
    "vaa11splitDate": "2019-02-01T01-00-00.000Z",
    "vaa02": "a04",
    "vaa12": "ao2",
    "vaa13splitDate": "2019-01-01T01-00-00.000Z",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao2",
    "vaa15splitDate": "2019-01-01T01-00-00.000Z",
    "vaa05": "Ein Blindtext hier 123."
    },
    {
    "id": "1",
    "startDate": "2020-06-01T01-00-00.000Z",
    "endDate": "2022-01-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot1",
    "flags": ["eHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa02": "a04",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa05": "Ein Blindtext hier 123."
    }
    ]""")

JSON_ARRAY_04_first_split = json.loads("""[
    {
    "id": "0",
    "startDate": "2017-12-01T01-00-00.000Z",
    "endDate": "2019-01-31T01-00-00.000Z",
    "state": "done",
    "type": "Slot2",
    "flags": ["sHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa02": "a04",
    "vaa12": "ao2",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao2",
    "vaa05": "Ein Blindtext hier 123.",
    "children": ["2"]
    },
    {
    "id": "1",
    "startDate": "2020-06-01T01-00-00.000Z",
    "endDate": "2022-01-31T01-00-00.000Z",
    "state": "new",
    "type": "Slot1",
    "flags": ["eHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa02": "a04",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa05": "Ein Blindtext hier 123."
    },
    {
    "id": "2",
    "startDate": "2019-02-01T01-00-00.000Z",
    "endDate": "2020-05-31T01-00-00.000Z",
    "state": "done",
    "type": "Slot2",
    "flags": ["eHO"],
    "vaa00": "ao2",
    "vaa01": "Blindtext dort 987.",
    "vaa02": "a04",
    "vaa12": "ao2",
    "vaa03": "MISSING",
    "vaa04": "425",
    "vaa14": "ao2",
    "vaa05": "Ein Blindtext hier 123.",
    "currentSplit": ["TypA"],
    "parent": "0"
    }]""")
