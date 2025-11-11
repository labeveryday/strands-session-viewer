# UI/UX Redesign Plan: Three-Panel Layout

## Overview
Transform the current stacked vertical layout into a modern three-panel dashboard with collapsible sidebar and dedicated chat panel.

## Layout Structure

### 1. Header Bar (Top, Fixed)
- Add hamburger menu button (left side)
- Keep title and refresh button
- Add session counter badge

### 2. Three-Panel Grid Layout
**Left Sidebar** (Collapsible, 280px when open)
- Sessions list
- Toggle state persisted
- Slide animation on collapse/expand

**Middle Panel** (Flex-grow, main content area)
- Session metadata (top)
- Search and filters
- Messages timeline (scrollable)
- Export button
- Expands to fill space when sidebar hidden

**Right Panel** (Fixed 400px when AI available, hidden otherwise)
- Quick analysis buttons at top
- Analysis results display area
- Chat interface at bottom
- Clear/reset chat button

## Implementation Steps

### Step 1: Update HTML Structure
- Add sidebar toggle state to Alpine.js data
- Restructure grid from `grid-cols-12` to flex-based layout
- Add hamburger button component
- Separate AI analysis into right panel
- Move chat interface to right panel bottom

### Step 2: Update CSS/Tailwind Classes
- Add sidebar transition classes
- Responsive breakpoints (hide sidebar on mobile by default)
- Fixed widths for panels
- Scrollable areas with proper heights
- Right panel sticky positioning

### Step 3: Update Alpine.js State
- Add `sidebarOpen` boolean (default: true)
- Add `toggleSidebar()` function
- Persist sidebar state to localStorage
- Update panel width classes dynamically

### Step 4: Reorganize AI Components
- Move AI analysis buttons to right panel top
- Keep analysis results in right panel
- Move chat input to right panel bottom
- Add chat history scrollable area
- Remove collapsible AI panel (always visible now)

### Step 5: Improve Responsiveness
- Mobile: sidebar hidden by default, overlay when open
- Tablet: all three panels visible, narrower
- Desktop: full three-panel layout
- Add z-index layers for mobile overlay

### Step 6: Visual Improvements
- Add subtle shadows/borders between panels
- Better spacing and padding
- Highlight active session more clearly
- Improve chat message styling
- Add loading states for AI responses

### Step 7: Testing
- Test sidebar toggle on all screen sizes
- Verify chat functionality in new layout
- Check message scrolling
- Test with/without AI features enabled
- Verify export still works

## Files to Modify
- `src/strands_viewer/static/index.html` (major changes)

## Estimated Impact
- Better use of screen space
- Dedicated chat area always visible
- Cleaner separation of concerns
- More professional dashboard appearance
- Improved UX for analysis workflows
