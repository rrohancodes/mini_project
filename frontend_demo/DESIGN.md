---
name: Civic Standard
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dadf'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f9'
  surface-container: '#ebeef3'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#e0e3e8'
  on-surface: '#181c20'
  on-surface-variant: '#3f4850'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f6'
  outline: '#707881'
  outline-variant: '#bfc7d2'
  surface-tint: '#006398'
  primary: '#006194'
  on-primary: '#ffffff'
  primary-container: '#007bb9'
  on-primary-container: '#fdfcff'
  inverse-primary: '#93ccff'
  secondary: '#545f73'
  on-secondary: '#ffffff'
  secondary-container: '#d5e0f8'
  on-secondary-container: '#586377'
  tertiary: '#585d60'
  on-tertiary: '#ffffff'
  tertiary-container: '#707579'
  on-tertiary-container: '#fbfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#cce5ff'
  primary-fixed-dim: '#93ccff'
  on-primary-fixed: '#001d31'
  on-primary-fixed-variant: '#004b73'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#dfe3e7'
  tertiary-fixed-dim: '#c3c7cb'
  on-tertiary-fixed: '#171c1f'
  on-tertiary-fixed-variant: '#43474b'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#e0e3e8'
typography:
  headline-xl:
    fontFamily: Public Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Public Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Public Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: '0'
  headline-md:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: '0'
  headline-sm:
    fontFamily: Public Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: '0'
  body-lg:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: '0'
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  body-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: '0'
  label-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Public Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.03em
  caption:
    fontFamily: Public Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: '0'
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system embodies official credibility, high accessibility, and structural precision, drawing directly from the heritage of public sector design systems like the US Web Design System and GOV.UK. It prioritizes clarity over ornamentation, ensuring every citizen, regardless of ability or device, can complete critical civil tasks without visual friction.

The aesthetic is strictly architectural and institutional:
- **Tone:** Authoritative, impartial, predictable, and transparent.
- **Visual Movement:** Pure flat functionalism. Interfaces are governed by strict grid alignments, hard 90-degree corners, deliberate rule lines, and a total absence of non-semantic decoration.
- **Accessibility Posture:** Built from the ground up for Section 508 and WCAG 2.1 AAA compliance, emphasizing unmistakable hit targets, explicit state styling, and unyielding textual contrast.

## Colors

The palette enforces a 60-30-10 distribution to balance civic authority with unmistakable affordance:

- **Base & Canvas (60%):** `#F8F9FA` acts as the overall document background. Main transactional surfaces, form panels, and content cards use pure `#FFFFFF` to emphasize focus. `#F1F5F9` is reserved for alternating data rows, inset callouts, and secondary content groupings.
- **Structure & Governance (30%):** `#1E293B` (Slate Navy) anchors the masthead, persistent utility bar, navigation menus, and global footer. This establishes an institutional frame that immediately signals official authority.
- **Action & Accent (10%):** `#0284C7` (Institutional Blue) is strictly operational. It is reserved for primary actions, active navigation states, interactive text links, and standard focus rings. It must never be diluted with purely decorative applications.
- **Text & Contrast:** Primary text is `#212529`, delivering a minimum contrast ratio of 12:1 against light surfaces. Secondary descriptive text uses `#475569`, never falling below the 4.5:1 ratio required for AAA compliance.
- **Structural Lines:** Dividers, container boundaries, and table rules utilize `#CBD5E1`.

## Typography

The design system standardizes entirely on **Public Sans**, an open, neutral typeface modeled on classic governmental signage and publication conventions. It provides clean vertical metrics, open apertures, and distinct character glyphs (such as capital 'I' vs lowercase 'l') that eliminate ambiguity across identity documentation, forms, and tables.

- **Scale Behavior:** Headings scale down responsively using designated mobile tokens to prevent horizontal overflow and awkward line breaks on compact screens.
- **Vertical Rhythm:** Headings enforce tight, readable leading (`1.2` to `1.33`) while narrative body copy uses an expansive `1.5` line height to ensure fatigue-free reading across lengthy policy and statutory text.
- **Hierarchy:** Weight steps are restrained strictly to `400` (Regular), `600` (Semibold), and `700` (Bold). Avoid medium (`500`) or thin weights to preserve contrast standards.

## Layout & Spacing

Layouts follow an 8px base rhythm with an accessible 12-column fixed-max-width responsive grid capped at `1200px` to maintain optimal line lengths.

- **Breakpoints:**
  - `Mobile` (< 640px): 4 columns, `margin-mobile` (16px), `gutter-mobile` (16px). Form controls span full width.
  - `Tablet` (640px – 1024px): 8 columns, `margin` (32px), `gutter` (24px).
  - `Desktop` (> 1024px): 12 columns, `margin` (32px), `gutter` (24px).
- **Whitespace Logic:** Structural boundaries and section divisions use deliberate `space-xl` (32px) and `space-lg` (24px) spacing, giving pages a calm, uncluttered feel. Within components, density remains compact (`space-xs` to `space-md`) to ensure critical form metadata fits above the fold.

## Elevation & Depth

This design system operates strictly on a **flat structural model** with zero decorative drop shadows, zero ambient diffusions, and zero skeuomorphic gradients. 

Visual hierarchy and layer separation are established purely through:
1. **1px Rule Lines:** Crisp boundaries utilizing `#CBD5E1` distinguish containers, cards, and field borders.
2. **Surface Contrasts:** Inset panels and secondary modules use `#F1F5F9` against the `#FFFFFF` main card canvas or `#F8F9FA` background.
3. **High-Contrast Focus Outlines:** Interactive states avoid glowing drop shadows. Elements in focus receive a mandatory, high-visibility 3px solid focus ring in `#0284C7` with a 2px white offset (`outline: 3px solid #0284C7; outline-offset: 2px;`).

## Shapes

All UI elements utilize strict **0px border-radius** (Sharp / Level 0). 

- **Geometry:** Every button, card, modal, input, and badge is defined by true 90-degree right angles.
- **Rationale:** Hard edges evoke bureaucratic structure, archival printing standards, and institutional stability. They eliminate visual fluff and reinforce crisp grid lines across complex administrative tables and data forms.

## Components

### Buttons
- **Primary:** Solid `#0284C7` background, white bold text, 0px border radius, 0px shadow. Padding: `12px 24px`. Hover: darken to `#0369A1`. Active: darken to `#075985`. Focus: 3px `#0284C7` ring with 2px white gap.
- **Secondary:** Transparent background, 2px solid `#1E293B` border, `#1E293B` text. Hover: `#1E293B` fill with white text.
- **Destructive:** Solid `#DC2626` background, white text.

### Form Inputs & Fields
- **Text Inputs / Selects:** 44px min-height for touch compliance. Pure white fill, 1px solid `#475569` border, 0px radius. Padding: `8px 12px`. Hover: border darkens to `#1E293B`. Focus: 2px solid `#0284C7` border with full accessibility outline.
- **Error State:** 2px solid `#DC2626` border accompanied by an inline alert text item and left-aligned red bar indicator.

### Checkboxes & Radios
- Box/Circle dimensions: `24px x 24px` for high-target compliance.
- Unchecked: 2px solid `#1E293B` border, white fill.
- Checked: `#1E293B` background with crisp white tick or center square mark.

### Cards & Inset Panels
- Flat white `#FFFFFF` surface enclosed by a 1px solid `#CBD5E1` border. No shadow. 
- Padded with `space-lg` (24px). Headers within cards sit atop a 1px divider rule.

### Status Banners & Callouts
- Rectangular block with a prominent 4px solid left border:
  - *Information:* `#0284C7` left border, `#F0F9FF` background.
  - *Warning:* `#D97706` left border, `#FFFBEB` background.
  - *Success:* `#15803D` left border, `#F0FDF4` background.
  - *Official Notice:* `#1E293B` left border, `#F1F5F9` background.

### Tables
- Dense, flat structure with a 2px `#1E293B` bottom border on header rows (`<th>`). 
- Alternating zebra rows using `#F8F9FA` and `#FFFFFF` for complex tabular citizen records.