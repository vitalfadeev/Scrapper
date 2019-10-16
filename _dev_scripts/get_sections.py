def get_section_names(page):
    import json
    with open("./sections-templates/en/sections.json", encoding="utf-8") as f:
        st = json.load(f)
        sections = list(st.keys())
        sections.sort()
        print(sections)
