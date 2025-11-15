# Micro-Interactions: Satisfying Experience

## SATISFYING: Adding Micro-Interactions

### Duration Guidelines
- **General micro-interactions**: 150-300ms (avoid interrupting flow)
- **Button presses**: Start within 16ms of click
- **Standard animations**: 200-500ms
- **UI motions**: 0.5-2s typically
- **Rule**: A tenth of a second makes big difference; half second wrong feels jarring

### Basic Effects
- **Fade**: Smooth opacity transitions
- **Slide**: Directional movement (left/right/up/down)
- **Scale**: Size changes (grow/shrink)
- **Rotate**: Angular transformations
- Sequential timing with 0.1s delays between elements

### Easing Curves
Linear motion = robotic. Use easing for natural feel:

**Ease-out** (starts fast, slows down):
- Best for: Elements entering screen
- Makes animation feel responsive
- Allows eye time to focus as element settles
- Most common for UI micro-interactions

**Ease-in** (starts slow, speeds up):
- Best for: Elements leaving screen
- Natural exit motion

**Spring/bounce**:
- Playful, energetic feel
- Use sparingly for emphasis

**Cubic-bezier**:
- Fine-tuned control over motion curves
- Custom easing for specific needs

### Motion Characteristics
- Follow real-world physics (objects speed up when starting, slow down when stopping)
- Subtle curves for micro-interactions
- Bolder curves for attention-grabbing transitions
- Always have purpose—guide users or give feedback

### Performance
- Aim for smooth 60fps
- Prefer hardware-accelerated properties (transforms, opacity)
- Avoid fancy effects causing frame drops or battery drain
- Provide motion-reduced alternatives for accessibility

### Resources
Study 21st.dev for component animations & subtle effects worth emulating.
