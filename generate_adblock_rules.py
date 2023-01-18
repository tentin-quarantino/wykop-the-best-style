import re
from pathlib import Path


def generate_adblock_rules_from_css(input_filename, output_filename):
    stylesheet = Path(input_filename).read_text().replace('\n', '')

    rules = re.finditer(
        r'(?P<selectors>[^\{]+)\{(?P<declarations>[^}]+)\}',
        stylesheet,
    )

    lines = []

    for rule in rules:
        selectors = rule.group('selectors').split(',')
        declarations = ';'.join(
            declaration if declaration.endswith('!important') else f'{declaration} !important'
            for declaration in rule.group('declarations').strip(';').split(';')
        )

        for selector in selectors:
            lines.append(
                f'wykop.pl##{selector.strip()}:style({declarations})'
            )

    Path(output_filename).write_text('\n'.join(lines))


if __name__ == '__main__':
    generate_adblock_rules_from_css('style.css', 'adblock.rules.txt')
