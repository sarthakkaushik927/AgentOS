# AgentOS Design System

## Typography
- Display (`font-display`): `Space Grotesk` - bold, geometric, used only for headings and the system status bar, restrained (never body copy).
- Body (`font-body`): `Manrope` - everything readable: paragraphs, labels, forms.
- Mono (`font-mono`): `JetBrains Mono` - reserved for anything that reads as a system readout: status chips, timestamps, memory/CPU-style stats, code.

## Colors
Light Theme:
- Paper: rgb(250, 250, 248)
- Surface: rgb(242, 242, 237)
- Ink: rgb(28, 28, 26)
- Slate: rgb(107, 107, 101)
- Hairline: rgb(228, 228, 223)
- Signal (Amber Accent): rgb(232, 135, 30)
- Signal-Ink: rgb(28, 20, 8)

Dark Theme:
- Paper: rgb(24, 24, 27)
- Surface: rgb(32, 32, 36)
- Ink: rgb(240, 240, 235)
- Slate: rgb(148, 148, 140)
- Hairline: rgb(42, 42, 46)
- Signal (Amber Accent): rgb(232, 135, 30)
- Signal-Ink: rgb(28, 20, 8)

## Geometry
- Small border radius (6px).
- Generous whitespace.
- Hairline 1px borders used only to separate genuinely distinct panels.
- Precise, not bubbly.

## Signature Element
- SystemStatusBar: a slim, mono-font strip showing live-looking readouts with an amber status dot, state label, and time.
