from pathlib import Path

# 1. Define the file path safely using pathlib
file_path = Path("Python") / "File-Handling" / "novel.txt"

# Ensure the parent directory exists before writing
file_path.parent.mkdir(parents=True, exist_ok=True)

# 2. Write the short story to the file
story = "It was a dark and stormy night. Rain lashed relentlessly against the old windowpanes, casting eerie, dancing shadows across the empty room. Arthur clutched his lantern tightly, his heart pounding with every rumble of thunder. He knew he wasn't alone in the abandoned house. A floorboard creaked softly behind him, freezing him in place as a cold gust of wind blew out the flame."

file_path.write_text(story, encoding="utf-8")

print(f"Success! Story written to: {file_path.resolve()}")