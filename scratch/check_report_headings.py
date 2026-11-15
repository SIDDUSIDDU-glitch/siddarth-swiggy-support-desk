with open("c:/ai work place/ai projects/SWIGGY SUPPORT DESK/Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
headings = [l.strip() for l in lines if l.startswith("#")]
print("\nHeadings found:")
for h in headings:
    print(h)
