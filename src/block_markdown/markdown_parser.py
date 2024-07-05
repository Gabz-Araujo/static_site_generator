from typing import List


def clean_block(block: str) -> str:
    return "\n".join(line.strip() for line in block.split("\n")).strip()


def markdown_to_blocks(markdown: str) -> List[str]:
    normalized_markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    blocks = normalized_markdown.split("\n\n")
    cleaned_blocks = [clean_block(block) for block in blocks if block.strip()]
    return cleaned_blocks
