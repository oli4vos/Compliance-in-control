Agent instruction
Before creating, styling, redesigning, or polishing any user-facing interface:
1. Read this file completely.
2. Inspect the product, audience, content, workflows, existing brand/assets, and technical constraints.
3. Define a project-specific visual thesis before writing UI code.
4. Do not fall back to generic SaaS/AI-builder aesthetics when design direction is missing.
5. Prefer purposeful composition, typography, content hierarchy, and interaction over decorative effects.
6. Treat accessibility, responsiveness, states, real content, and performance as part of the design.
7. Before shipping, run the Anti-AI Design Gate at the end of this file.
If another project-specific design document conflicts with this file, the more specific intentional project rule wins, except accessibility and usability requirements.
1. The core principle
A page should look as if its visual decisions came from the product, its content, and its audience — not from the average of modern landing-page templates.
The goal is not:
- “make it look less AI”
- “make it weird”
- “remove all cards”
- “avoid all gradients”
- “never use Inter”
- “make everything asymmetrical”
- “use brutalism”
The goal is:
Every visible design choice must either support hierarchy, usability, brand character, content, or interaction.
If a choice exists only because it is a fashionable default, remove it or justify it.
2. Mandatory design brief before implementation
For every new project or substantial redesign, establish these fields first.
Product truth
- What does the product/site actually do?
- Who is the primary user?
- What is the primary user action?
- What information must be understood within the first screen?
- Is this primarily a brand surface or a product surface?
Visual thesis
Write one sentence:
“This interface should feel like [specific world/reference], translated into a digital product for [audience], with [one defining trait] and without [one anti-reference].”

Good:
- “A calm specialist journal translated into a tax-research workspace: dense but legible, restrained, evidence-led, never startup-glossy.”
- “A contemporary cycling catalogue translated into a training app: technical, tactile, fast, with editorial photography and no neon gamer UI.”
- “Municipal wayfinding translated into a public-service dashboard: extremely clear hierarchy, strong labels, modest color, no decorative glass.”
Bad:
- “Modern, premium and clean.”
- “Sleek SaaS.”
- “Apple-like.”
- “Futuristic.”
- “Minimalist with gradients.”
Three concrete adjectives
Use adjectives that imply observable design consequences.
Good:
- editorial
- utilitarian
- tactile
- archival
- technical
- quiet
- compact
- typographic
- playful
- institutional
- cinematic
- handmade
- industrial
- bookish
Weak unless clarified:
- modern
- premium
- clean
- beautiful
- professional
- innovative
Signature move
Choose one recognizable device for the project:
- unusual typographic scale relationship
- distinctive rule/divider system
- image cropping language
- asymmetric navigation
- a specific data-visualization treatment
- a recognizable accent shape
- one purposeful motion behavior
- a recurring annotation style
- editorial captions/marginalia
- tactile controls
- unusual but usable density
Do not choose five signature moves.
Restraint
Name one thing the interface deliberately does less of:
- almost no shadows
- almost no rounded containers
- no gradients
- minimal animation
- only one accent color
- very limited iconography
- no decorative illustration
- no full-width cards
Anti-reference
Name at least one visual outcome to avoid:
- generic AI SaaS landing page
- crypto dashboard
- glassmorphism showcase
- default shadcn demo
- Framer-template portfolio
- “purple startup”
- oversized editorial fashion site
- dense enterprise admin panel
3. Hard defaults to avoid
These are not universally forbidden. They are forbidden as automatic defaults.
Layout and composition
Do not automatically:
- center the entire hero
- place an eyebrow pill above every H1
- use the sequence badge → huge heading → gray paragraph → two CTAs
- build every section inside the same centered max-width container
- use identical vertical padding for every section
- create three equal feature cards because there are three bullets
- create a bento grid merely because the page needs “visual interest”
- put every piece of information inside a card
- nest cards inside cards
- make every content block the same height
- use a split hero with text left and generic product mockup right without a content reason
- use a giant floating browser-frame screenshot as the default product visual
- frame screenshots with fake macOS traffic-light dots unless the browser context matters
- make a dashboard from sidebar + topbar + four stat cards + chart + recent activity by default
- use an alternating left/right marketing-section rhythm mechanically
- end every page with a giant rounded CTA panel
- create a “logo cloud” when credible logos do not exist
- create empty decorative whitespace just to make the page feel “premium”
- force asymmetry when the content benefits from regular structure
Numbering
Do not use decorative leading-zero numbering:
- 01
- 02
- 03
- 01 / 04
- STEP 01
Use numbering only when sequence, rank, chronology, or reference genuinely matters. Prefer normal numerals unless the brand system specifically requires another format.
4. Card discipline
Cards are containers, not a design language.
Use a card only when at least one is true:
- the item is independently actionable
- the item can move/reorder independently
- it has a distinct state
- it is a separate object/entity
- grouping materially improves comprehension
- it needs a boundary because the surrounding surface is complex
Avoid cards when:
- a divider would work
- spacing alone would work
- a table/list is semantically better
- headings and indentation already establish hierarchy
- the card exists only to create rounded corners and a shadow
Never automatically combine:
- rounded rectangle
- 1px gray border
- soft shadow
- small icon tile
- eyebrow
- heading
- two-line description
- arrow link
If five adjacent objects all have the same card treatment, reconsider whether they should be a list, grid, table, timeline, annotated canvas, or one shared surface.
5. Shape language
Define a small, intentional radius system.
Do not:
- use rounded-xl / rounded-2xl everywhere
- make buttons, cards, inputs, screenshots, navbars and modals all equally rounded
- turn every label into a pill
- use pills for non-interactive text simply because they look polished
A project should normally have:
- one small radius
- one medium radius
- optionally one expressive radius for a specific component family
- square/near-square geometry where appropriate
Full pills are appropriate for:
- compact filters
- segmented controls
- tags with interaction
- status chips
- small actions where the shape aids recognition
They are not the universal default for buttons.
6. Color rules
Start from semantic roles, not fashionable hex values.
Define:
- canvas
- primary text
- secondary text
- subtle text
- divider/border
- primary action
- secondary action
- status colors
- selection/focus
- optional brand accent
Avoid default AI palettes:
- purple → blue hero gradients
- cyan/purple glow on black
- indigo everywhere
- zinc/slate + violet with no brand rationale
- multiple blurred radial color blobs
- rainbow gradients as “innovation”
- gradient text as the primary source of hierarchy
A gradient is allowed only when it has a role:
- material/light simulation
- data scale
- brand asset
- spatial depth
- intentional illustration
- meaningful transition
Do not use a gradient merely to signal “technology” or “AI”.
Prefer a color system that can be described in one sentence.
7. Typography rules
Typography must carry more of the design than decoration does.
Before selecting fonts, decide:
- editorial vs utilitarian
- warm vs technical
- compact vs airy
- display-heavy vs interface-neutral
- numeric/data requirements
- language coverage
- variable-font needs
- loading/performance constraints
Do not automatically default to:
- Inter
- Geist
- Roboto
- Space Grotesk
- Satoshi
These fonts are not banned. They require a reason.
If using a common UI font, create identity through:
- scale
- width
- weight contrast
- tracking
- line height
- casing
- alignment
- measure
- pairing
- numeric style
- labels/captions
Avoid the generic hierarchy:
- 64px/72px bold H1
- 20px muted lead
- 16px body
- 14px card text
- all headings semibold
- everything else gray
Do not make every heading a short marketing slogan.
Use real editorial structure where useful:
- kicker
- headline
- deck
- caption
- source
- footnote
- metadata
- annotation
- section label
But do not convert every label into uppercase microtext.
8. Copy is part of the visual design
Generic AI copy makes otherwise good UI feel generated.
Avoid filler such as:
- “Unlock the power of…”
- “Supercharge your…”
- “Elevate your…”
- “Transform the way you…”
- “Seamlessly…”
- “Effortlessly…”
- “Next-generation…”
- “Powerful, intuitive…”
- “Everything you need…”
- “Built for X. Designed for Y.”
- “One platform. Endless possibilities.”
- “Get started in minutes.”
- “Join thousands of…”
- “The future of…”
- “AI-powered” repeated as decoration
Avoid invented:
- customer counts
- revenue
- testimonials
- logos
- star ratings
- growth percentages
- uptime claims
- awards
- press quotes
Use domain language, actual product nouns, real actions, realistic examples, and specific states.
Button labels should name the action:
- “Compare versions”
- “Upload invoice”
- “Open analysis”
- “Create project”
Avoid using “Learn more” everywhere.
9. Iconography rules
Icons should clarify, not decorate.
Avoid the AI starter-pack effect:
- Sparkles
- Wand
- Zap
- Bot
- Rocket
- ShieldCheck
- Brain
- Stars
- generic ArrowRight after every text link
Especially avoid placing every icon inside the same rounded colored square above a heading.
Libraries such as Lucide or Tabler are acceptable foundations, but:
- define one icon family per interface
- define size and stroke rules
- use icons only where the symbol is recognizable
- do not substitute an icon for a label when comprehension suffers
- consider custom icons/marks for signature product concepts
- avoid mixing outline styles casually
10. Borders, shadows and depth
Depth should reflect hierarchy or interaction.
Do not:
- put a 1px #e5e7eb border around every object
- add a soft shadow to every card
- combine border + shadow + tinted background + glow by default
- use glassmorphism for ordinary navigation
- blur every sticky surface
- use “premium” shadows with huge blur radii everywhere
Prefer one dominant depth model:
- mostly flat with rules/dividers
- layered surfaces
- restrained shadows
- tonal elevation
- spatial/3D treatment
Use stronger depth only where the object actually floats, overlays, drags, opens, or demands focus.
11. Background decoration
Do not automatically add:
- dot grids
- graph-paper grids
- radial glow blobs
- mesh gradients
- blurred circles
- noise texture
- animated particles
- star fields
- aurora backgrounds
- gradient borders
- spotlight-following cursor glows
- giant abstract SVG loops
A background device must reinforce the product world or composition.
If removing the decoration has no impact on hierarchy, meaning, or brand, it is probably unnecessary.
12. Motion
Motion must explain:
- cause and effect
- spatial relationship
- change of state
- hierarchy
- feedback
- continuity
Avoid:
- fade-up on every section
- staggered entrance on every grid
- floating cards forever
- looping marquee because the hero feels empty
- scale(1.02) on every hover
- translateY(-4px) on every card
- magnetic buttons everywhere
- text scramble/typewriter effects without conceptual reason
- scroll-jacking
- gratuitous parallax
- transition-all as a blanket rule
Use one motion grammar per product.
For product UI:
- prioritize fast feedback
- keep navigation predictable
- animate state changes, not decoration
For brand/editorial surfaces:
- slower expressive movement is acceptable if it does not block reading or interaction
Always respect prefers-reduced-motion.
Use Motion/Framer Motion, GSAP, or similar libraries as implementation tools — not as a source of aesthetic direction.
13. Content density
Do not equate “clean” with “empty”.
Choose density based on task:
- marketing can breathe
- research tools need scannability
- operations tools may need compact tables
- consumer apps may prioritize touch
- editorial content needs readable measure
- data products need comparison
Avoid turning useful structured information into a collection of oversized cards just to make the interface look modern.
Ask:
What is the highest-information form that remains easy to understand?

Sometimes the answer is a table.
14. Real content before decorative polish
Use realistic content as early as possible.
Before polishing:
- populate real headings
- use plausible field lengths
- include long and short values
- include empty/loading/error states
- include actual unit formats
- include real dates/currencies if the domain uses them
- test localization if relevant
- test long names
- test missing images
- test dense datasets
Generic placeholder copy causes generic layouts.
15. Responsive behavior must be designed, not stacked
Do not simply turn desktop columns into one vertical column.
At each breakpoint decide:
- what becomes primary
- what can collapse
- what becomes a drawer
- what becomes horizontally scrollable
- what becomes sticky
- what can be abbreviated
- what changes order
- what should disappear
- what needs larger touch targets
- which comparison relationships must remain side-by-side
Mobile should feel composed for mobile, not like desktop after flex-col.
16. Component libraries: how to use them without inheriting a look
Preferred foundation: headless / unstyled primitives
Good default foundations:
- Base UI
- Radix Primitives
- React Aria
- Ark UI
- Headless UI
- Ariakit
- Floating UI for positioning/interaction primitives
Reason:
They provide behavior, accessibility, state management, and interaction while leaving more visual authorship to the project.
shadcn/ui
Allowed and often useful.
Rule:
Use shadcn as source code, not as the finished visual identity.
If shadcn is used:
- replace default theme values
- define project-specific radius
- define project-specific typography
- revisit component padding
- revisit borders/shadows
- do not use Card as the universal wrapper
- audit the default button/input look
- do not inherit the demo-page composition
- customize before duplicating components across the app
Tools such as tweakcn can help break theme-default convergence, but the final system still needs a product-specific thesis.
Styled/inspiration registries
Useful for individual ideas:
- 21st.dev
- Cult UI
- React Bits
- Park UI
- Kibo UI / similar registries
Use them as:
- implementation reference
- interaction reference
- isolated component source
Do not:
- import several “wow” components just to create personality
- combine incompatible visual grammars
- let animated component galleries determine the brand
- build a page that looks like a component-library showcase
Motion libraries
Motion is a good general-purpose animation foundation.
Rule:
First describe the interaction in plain language. Then choose the library.
Never start with:
“What cool Motion component can we add?”

Start with:
“What state change does the user need to understand?”

Icons
Good general sets:
- Lucide
- Tabler Icons
But a consistent icon library can still look generic if the same obvious AI-associated symbols are used everywhere. Semantic choice matters more than the package.
17. AI-specific visual tells to actively audit
The following cluster is especially suspicious when several appear together:
- centered hero
- tiny pill above hero
- giant bold headline
- one phrase in gradient text
- muted gray subheadline
- two CTA buttons
- dashboard/browser mockup
- purple/blue glow behind mockup
- logo cloud
- three feature cards
- every feature has Lucide icon in rounded square
- bento grid
- “How it works” with 01 / 02 / 03
- fake testimonial cards
- pricing cards with “Most popular” pill
- FAQ accordion
- giant rounded final CTA
- large multi-column footer
- same radius everywhere
- same shadow everywhere
- fade-up-on-scroll everywhere
If the page matches this skeleton, stop and redesign the information architecture before polishing.
18. Preferred alternatives to common AI defaults
Instead of a centered hero:
- use a left editorial column
- make the product itself the first interaction
- lead with a dense useful artefact
- use a statement + evidence layout
- use image-led composition
- use an index/catalogue structure
Instead of three feature cards:
- annotated screenshot
- comparison table
- narrative sequence
- one large feature with smaller supporting details
- compact feature list
- diagram
- timeline
- before/after
- interactive demo
- evidence panel
Instead of a logo cloud:
- named customer story
- case metric with source
- concrete integration list
- quote with attribution
- no social proof if none exists
Instead of bento:
- editorial grid with hierarchy
- masonry only if content sizes genuinely vary
- table/list for comparable items
- full-bleed modules
- split canvas
- index
Instead of glow/gradient:
- typography
- image
- color blocking
- lines/rules
- material texture
- whitespace contrast
- meaningful data color
Instead of generic icon tiles:
- labels
- numbers without leading-zero styling
- small diagrams
- thumbnails
- product screenshots
- typographic markers
- no marker at all
19. Design tokens
Every serious project should explicitly define tokens.
At minimum:
colors:
  canvas:
  surface:
  text-primary:
  text-secondary:
  border:
  accent:
  focus:
  danger:
  success:

typography:
  display:
  heading:
  body:
  label:
  mono-or-data:

spacing:
  xs:
  sm:
  md:
  lg:
  xl:
  section-small:
  section-large:

radius:
  small:
  medium:
  expressive:

motion:
  fast:
  normal:
  slow:
  easing-standard:
  easing-emphasized:
Do not blindly use one mathematical spacing scale for every layout problem. Tokens create coherence, not monotony.
20. State design
A polished interface includes:
- default
- hover where relevant
- focus-visible
- active/pressed
- selected
- disabled
- loading
- empty
- error
- success
- partial/incomplete data
- permission denied where relevant
- offline/retry where relevant
AI-generated mockups often over-focus on the perfect populated state. Production design must not.
21. Accessibility is visual craft
Required:
- meaningful focus indication
- keyboard access
- sufficient contrast
- sensible heading order
- labels for inputs
- non-color status cues
- touch target consideration
- reduced motion support
- readable line lengths
- zoom/reflow resilience
- semantic HTML where possible
Do not “solve” accessibility by making every element visually heavy. Accessibility and visual refinement are compatible.
22. Performance is part of the aesthetic
Do not use:
- multiple WebGL effects for background decoration
- autoplay video without strong benefit
- giant JS animation bundles for tiny interactions
- dozens of custom font files
- high-resolution assets without responsive sizing
- continuous animation offscreen
A page that feels immediate usually feels more intentional.
23. Project-specific variation requirement
To prevent this file itself from creating a new house style, every project must intentionally vary at least these five dimensions:
1. Typography
2. Composition/alignment
3. Shape language
4. Color strategy
5. Density
Do not reuse the exact same combination across unrelated products unless they share one brand system.
24. Generation workflow for coding agents
When asked to “build a page”, do this internally before coding:
A. Understand
Summarize:
- product
- audience
- primary action
- content types
- brand/product register
B. Choose direction
Define:
- visual thesis
- 3 concrete adjectives
- signature move
- restraint
- anti-reference
C. Design structure
Choose information architecture before decoration.
D. Set tokens
Define type, color, spacing, radius, depth, motion.
E. Build the boring skeleton first
Implement:
- semantic layout
- content
- responsive structure
- states
- accessibility
F. Add identity
Add only the visual decisions supported by the thesis.
G. Remove template residue
Search for:
- unnecessary cards
- pills
- rounded rectangles
- glow
- generic icons
- fake metrics
- decorative numbering
- repeated CTA patterns
- generic marketing copy
H. Run the gate below
25. Anti-AI Design Gate
Before declaring UI finished, answer each item PASS/FAIL.
Identity
- Can I explain the visual thesis in one sentence?
- Does the interface visually relate to this specific product/domain?
- Is there at least one distinctive but coherent design decision?
- Would the same styling feel obviously wrong for an unrelated SaaS product?
Layout
- Is the composition driven by content rather than a template?
- Have I avoided unnecessary equal-card grids?
- Are section rhythms varied intentionally?
- Is center alignment used only where appropriate?
- Is decorative leading-zero numbering absent?
Components
- Are cards used for actual grouping/state/action?
- Are radii deliberate rather than universal?
- Are pills limited to appropriate controls/status?
- Are borders and shadows doing a job?
- Have default library styles been customized?
Typography
- Does typography create hierarchy without effects?
- Is the font choice intentional?
- Are measure, leading, tracking and weight considered?
- Are labels/headlines written for this product rather than a generic landing page?
Color
- Does color have semantic/brand roles?
- Are gradients justified?
- Is there a restrained accent strategy?
- Does contrast work?
Content
- Is all visible proof real or clearly marked as demo content?
- Are fake testimonials, fake logos and fake metrics absent?
- Is the copy specific and concrete?
- Do CTA labels describe actual actions?
Motion
- Does motion explain something?
- Is there one coherent motion grammar?
- Is gratuitous fade/stagger/hover movement absent?
- Is reduced-motion behavior supported?
Product quality
- Are empty/loading/error/focus states designed?
- Does mobile recompose rather than merely stack?
- Is keyboard interaction usable?
- Is performance reasonable?
Shipping rule
If 5 or more items fail:
- do not polish the existing styling
- revisit the visual thesis and layout
If 1–4 items fail:
- fix them before shipping
If all pass:
- ship
26. Short reusable prompt
Use this when an agent cannot automatically read this file:
Design and implement this interface as a product-specific system, not as a generic AI/SaaS template. First infer the product, audience, primary action, content density, and whether this is a brand or product surface. Establish a concrete visual thesis, three observable adjectives, one signature move, one restraint, and one anti-reference. Build information architecture before decoration. Avoid default AI patterns: centered badge/headline/two-CTA heroes, decorative 01/02/03 numbering, purple-blue gradients, glow blobs, automatic bento grids, three identical feature cards, card-within-card layouts, universal 16px+ rounding, pill-everything, generic Lucide icon tiles, fake browser frames, fake metrics/testimonials/logos, uniform fade-up animation, and generic “premium/modern” copy. Cards, gradients, shadows, pills, icons and motion are allowed only when they have a clear role. Prefer real content, typographic hierarchy, purposeful alignment, restrained tokens, accessible states, and responsive re-composition. If using shadcn or another styled component library, treat it as source code and replace its visual defaults. Use headless primitives when appropriate. Before finishing, audit the UI against DESIGN.md and remove any remaining template residue.

27. Library shortlist
Use as foundations, not identities.
Behavior/accessibility first
- Radix Primitives
- Base UI
- React Aria
- Ark UI
- Headless UI
- Ariakit
- Floating UI
Source-code component systems
- shadcn/ui — customize heavily; never ship the untouched visual defaults
Theme exploration
- tweakcn — useful to break shadcn/Tailwind theme convergence
Motion
- Motion — purposeful transitions and gestures
Icons
- Lucide
- Tabler Icons
Inspiration / selective components
- 21st.dev
- Cult UI
- React Bits
- Park UI
Rule for inspiration libraries:
take one useful idea, adapt it to the project grammar, and remove the source library’s obvious signature.
28. Final principle
The opposite of AI-looking design is not “handmade-looking design”.
It is decision-rich design.
A human-directed interface has:
- a reason for its hierarchy
- a reason for its density
- a reason for its typography
- a reason for its shapes
- a reason for its color
- a reason for its motion
- content that belongs to the product
- enough restraint that the reasons remain visible

## IPC project brief

### Product truth

IPC helps Dutch IT and AI suppliers turn tender requirements, security questionnaires and customer requests into traceable evidence dossiers. The primary action is to inspect one requirement, understand its source, review suggested evidence and record a human decision.

### Visual thesis

This interface should feel like a calm evidence room translated into a digital workspace for procurement, security and AI reviewers: editorial, technical and quiet, with source-line annotations and no glossy startup theatre.

### Three concrete adjectives

- archival: preserve source, provenance and chronology visibly;
- utilitarian: controls and tables should explain themselves;
- quiet: one navy-green accent system, restrained borders and no decorative glow.

### Signature move

Use a recurring source rule: thin horizontal dividers, monospaced reference labels and short provenance captions should make every important object feel traceable to a document.

### Restraint and anti-reference

Use almost no shadows, avoid excessive rounded cards and avoid the generic purple AI SaaS dashboard. Prefer ruled surfaces, asymmetric editorial composition and meaningful whitespace.
