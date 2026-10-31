# pUI: the shared look of the p* apps

One palette, type scale, shape set and component styles for every public p* app, taken from the icon
suite (graphite `#1F232B` → `#121418`, white, violet `#8B5CF6`). Light and dark palettes follow the
system dark mode through `values-night`.

Apply or update it in a project (copies only `p_*` resources and `<namespace>/pui/PUi.kt`):

```
python -I configs/android/pui/apply.py <project-dir> [module]
```

## Tokens (`p_colors.xml`)

| Token | Use |
|---|---|
| `p_bg` | window, status and navigation bars |
| `p_surface` | cards, dialogs, sheets |
| `p_surface2` / `p_surface3` | keys, inputs, chips, neutral buttons / pressed or secondary keys |
| `p_line` | dividers, outlines |
| `p_text` / `p_text2` / `p_text3` | primary / secondary / hint and faint glyphs |
| `p_accent` + `p_on_accent` | filled primary action, active indicator |
| `p_accent_text` | accent-colored text and icons on bg/surface |
| `p_accent_soft` + `p_on_accent_soft` | tonal buttons, selected tab/chip/row |
| `p_danger`, `p_success`, `p_warning` | status |

Apps keep their own semantic color names but define them as aliases, in `values/colors.xml` only:
`<color name="card">@color/p_surface</color>`. No app color file in `values-night` is needed.

## Themes

- `Theme.P`: no action bar (screens draw their own top bar with `pTopBar` or a layout).
- `Theme.P.Bar`: flat framework action bar in `p_bg`.
- `Theme.P.Dialog`: rounded `p_surface` alert dialogs (set automatically by both themes).

Both set `buttonStyle` → tonal pill, `borderlessButtonStyle` → text pill, `editTextStyle` → filled field.

## Components

| XML style | Code (`PUi.kt`) | Look |
|---|---|---|
| `P.Button` / `.Tonal` / `.Neutral` / `.Outline` / `.Text` / `.Danger` | `pButton(text, PButton.X)` | 44dp pill, medium 14sp, no caps |
| `P.Card` | `pCard()` | `p_surface`, 20dp corners, 16dp padding |
| `P.Row` | `pRow()` | 56dp min, 14dp corners ripple |
| `P.Chip` | `pChip(text, selected)` | 36dp pill; selected = accent-soft |
| `P.Input` | (theme default) | `p_surface2` fill, 8dp corners, 2dp accent outline on focus |
| `P.Text.Display/Title/Subtitle/Body/Secondary/Label/Caption/Section` | `pTitle`, `pBody`, `pSection`... | 34/22/17/15/15/14/12/12sp |
| `P.TopBar` | `pTopBar(title, actions)` | 56dp, title 22sp medium on `p_bg` |
| — | `pKey(text, fill, fg)` | keypad tile, 14dp corners |

Spacing is a 4dp grid (`p_space_xs..xl` = 4/8/12/16/24), screen gutter 16dp, touch targets ≥ 48dp.

## Rules

- Never hard-code colors in an app: use `p_*` tokens or aliases of them.
- Accent is for the one primary action and the active state on a screen, not for every label.
- Primary actions are pills; containers are rounded rectangles (20dp cards, 14dp rows/keys).
- Keep `p_*` files untouched in apps; change the kit here and re-apply.
