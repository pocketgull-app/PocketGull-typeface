"""
PocketGull Nib Engine — Stroke Expansion for Procedural Type Design

Takes skeleton strokes (center-line paths) and expands them into filled
outlines using an elliptical chisel-tip nib model, matching the PocketGull
felt-tip marker aesthetic.

Coordinate system: SVG space (y=0 top, y=79 baseline)
Output: SVG path `d` attribute strings
"""
import math
from dataclasses import dataclass, field

# ─────────────────────────────────────────────────────────────
# Nib Model
# ─────────────────────────────────────────────────────────────

@dataclass
class NibModel:
    """Elliptical chisel-tip nib at a fixed angle.
    
    The nib is modeled as an ellipse with semi-axes (major, minor)
    rotated by `angle` radians. When a stroke moves at direction φ,
    the perpendicular width is:
    
        w(φ) = sqrt((major·cos(φ-angle))² + (minor·sin(φ-angle))²)
    """
    major: float = 5.5    # Thick axis (SVG units) — vertical stems
    minor: float = 2.8    # Thin axis (SVG units) — horizontal crossbars
    angle: float = -0.07  # Nib tilt in radians (~-4°)
    
    def width_at_direction(self, direction: float) -> float:
        """Compute perpendicular stroke width for a given stroke direction."""
        delta = direction - self.angle
        w = math.sqrt(
            (self.major * math.cos(delta)) ** 2 +
            (self.minor * math.sin(delta)) ** 2
        )
        return w

    def offsets_at(self, direction: float) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute left and right offset vectors perpendicular to stroke direction."""
        w = self.width_at_direction(direction)
        # Normal vector (perpendicular to stroke direction)
        nx = -math.sin(direction)
        ny = math.cos(direction)
        left = (nx * w, ny * w)
        right = (-nx * w, -ny * w)
        return left, right


# PocketGull default nib — extracted from master glyph analysis
# The 'l' glyph is ~10.75 SVG units wide (essentially a vertical stem)
# Accounting for left/right outline expansion: stem_width ≈ 2 * major
POCKETGULL_NIB = NibModel(major=6.5, minor=2.3, angle=-0.07)  # 2.83:1 Caslon display contrast


# ─────────────────────────────────────────────────────────────
# Stroke Primitives
# ─────────────────────────────────────────────────────────────

@dataclass
class Point:
    x: float
    y: float
    pressure: float = 1.0  # 0.0-1.0, modulates nib width


@dataclass
class Stroke:
    """A single stroke path as a sequence of control points."""
    points: list[Point] = field(default_factory=list)
    closed: bool = False
    
    @classmethod
    def line(cls, x1, y1, x2, y2, pressure=1.0):
        return cls([Point(x1, y1, pressure), Point(x2, y2, pressure)])
    
    @classmethod
    def polyline(cls, *coords, pressure=1.0):
        """Create from flat (x1,y1, x2,y2, ...) coordinates."""
        pts = [Point(coords[i], coords[i+1], pressure) for i in range(0, len(coords), 2)]
        return cls(pts)
    
    @classmethod
    def arc(cls, cx, cy, rx, ry, start_deg, end_deg, n_samples=24, pressure=1.0):
        """Elliptical arc as sampled points."""
        pts = []
        start = math.radians(start_deg)
        end = math.radians(end_deg)
        for i in range(n_samples + 1):
            t = start + (end - start) * i / n_samples
            x = cx + rx * math.cos(t)
            y = cy + ry * math.sin(t)
            pts.append(Point(x, y, pressure))
        return cls(pts)
    
    @classmethod
    def oval(cls, cx, cy, rx, ry, n_samples=32, pressure=1.0):
        """Full ellipse as sampled points (closed)."""
        pts = []
        for i in range(n_samples):
            t = 2 * math.pi * i / n_samples
            x = cx + rx * math.cos(t)
            y = cy + ry * math.sin(t)
            pts.append(Point(x, y, pressure))
        stroke = cls(pts, closed=True)
        return stroke
    
    @classmethod
    def dot(cls, cx, cy, r=2.5, n_samples=16, pressure=1.0):
        """Filled circle (for dots in i, j, !, :, etc.)."""
        return cls.oval(cx, cy, r, r, n_samples, pressure)
    
    @classmethod
    def bezier3(cls, p0, p1, p2, p3, n_samples=20, pressure=1.0):
        """Cubic Bézier stroke sampled into points."""
        pts = []
        for i in range(n_samples + 1):
            t = i / n_samples
            t2 = t * t
            t3 = t2 * t
            mt = 1 - t
            mt2 = mt * mt
            mt3 = mt2 * mt
            x = mt3*p0[0] + 3*mt2*t*p1[0] + 3*mt*t2*p2[0] + t3*p3[0]
            y = mt3*p0[1] + 3*mt2*t*p1[1] + 3*mt*t2*p2[1] + t3*p3[1]
            pts.append(Point(x, y, pressure))
        return cls(pts)


@dataclass
class GlyphSkeleton:
    """A complete glyph defined as a set of strokes."""
    char: str
    strokes: list[Stroke]
    width: float  # Total glyph width in SVG units (used for advance width)


# ─────────────────────────────────────────────────────────────
# Stroke Expander
# ─────────────────────────────────────────────────────────────

class StrokeExpander:
    """Expands skeleton strokes into filled SVG outlines using the nib model."""
    
    def __init__(self, nib: NibModel = None):
        self.nib = nib or POCKETGULL_NIB
    
    def _compute_direction(self, p1: Point, p2: Point) -> float:
        """Angle of stroke from p1 to p2."""
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.atan2(dy, dx)
    
    def _expand_open_stroke(self, stroke: Stroke) -> str:
        """Expand an open stroke into a filled outline SVG path."""
        pts = stroke.points
        if len(pts) < 2:
            return ""
        
        left_outline = []
        right_outline = []
        
        for i, pt in enumerate(pts):
            # Compute direction
            if i == 0:
                direction = self._compute_direction(pts[0], pts[1])
            elif i == len(pts) - 1:
                direction = self._compute_direction(pts[-2], pts[-1])
            else:
                direction = self._compute_direction(pts[i-1], pts[i+1])
            
            # Get nib width modulated by pressure
            w = self.nib.width_at_direction(direction) * pt.pressure
            
            # Normal vector
            nx = -math.sin(direction)
            ny = math.cos(direction)
            
            left_outline.append((pt.x + nx * w, pt.y + ny * w))
            right_outline.append((pt.x - nx * w, pt.y - ny * w))
        
        # Build closed path: left forward + right backward + rounded end caps
        path_pts = left_outline + list(reversed(right_outline))
        return self._points_to_svg_path(path_pts, closed=True)
    
    def _expand_closed_stroke(self, stroke: Stroke) -> str:
        """Expand a closed stroke (like an oval) into inner + outer outlines."""
        pts = stroke.points
        n = len(pts)
        if n < 3:
            return ""
        
        outer = []
        inner = []
        
        for i in range(n):
            p_prev = pts[(i - 1) % n]
            p_curr = pts[i]
            p_next = pts[(i + 1) % n]
            
            direction = self._compute_direction(p_prev, p_next)
            w = self.nib.width_at_direction(direction) * p_curr.pressure
            
            nx = -math.sin(direction)
            ny = math.cos(direction)
            
            outer.append((p_curr.x + nx * w, p_curr.y + ny * w))
            inner.append((p_curr.x - nx * w, p_curr.y - ny * w))
        
        # Outer contour (clockwise) + inner contour (counter-clockwise)
        outer_svg = self._points_to_svg_path(outer, closed=True)
        inner_svg = self._points_to_svg_path(list(reversed(inner)), closed=True)
        return outer_svg + inner_svg
    
    def _expand_dot(self, stroke: Stroke) -> str:
        """Expand a dot/circle as a filled shape (no inner contour)."""
        pts = stroke.points
        if not pts:
            return ""
        # For a dot, just use the outer contour of a closed stroke
        n = len(pts)
        outer = []
        for i in range(n):
            p_prev = pts[(i - 1) % n]
            p_curr = pts[i]
            p_next = pts[(i + 1) % n]
            direction = self._compute_direction(p_prev, p_next)
            w = self.nib.width_at_direction(direction) * p_curr.pressure * 0.5
            nx = -math.sin(direction)
            ny = math.cos(direction)
            outer.append((p_curr.x + nx * w, p_curr.y + ny * w))
        return self._points_to_svg_path(outer, closed=True)
    
    def _points_to_svg_path(self, pts: list[tuple[float, float]], closed=True) -> str:
        """Convert a list of points to an SVG path `d` string using smooth curves."""
        if not pts:
            return ""
        
        n = len(pts)
        if n < 3:
            # Fallback to straight lines
            d = f"M{pts[0][0]:.4f},{pts[0][1]:.4f}"
            for p in pts[1:]:
                d += f"L{p[0]:.4f},{p[1]:.4f}"
            if closed:
                d += "Z"
            return d
        
        # Use Catmull-Rom → Cubic Bézier conversion for smooth curves
        d = f"M{pts[0][0]:.4f},{pts[0][1]:.4f}"
        
        for i in range(n - 1 if not closed else n):
            p0 = pts[(i - 1) % n]
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            p3 = pts[(i + 2) % n]
            
            # Catmull-Rom to cubic Bézier control points
            cp1x = p1[0] + (p2[0] - p0[0]) / 6
            cp1y = p1[1] + (p2[1] - p0[1]) / 6
            cp2x = p2[0] - (p3[0] - p1[0]) / 6
            cp2y = p2[1] - (p3[1] - p1[1]) / 6
            
            d += f"C{cp1x:.4f},{cp1y:.4f},{cp2x:.4f},{cp2y:.4f},{p2[0]:.4f},{p2[1]:.4f}"
        
        if closed:
            d += "Z"
        
        return d
    
    def expand_glyph(self, skeleton: GlyphSkeleton) -> str:
        """Expand all strokes in a glyph skeleton into a combined SVG path."""
        parts = []
        for stroke in skeleton.strokes:
            if stroke.closed:
                # Check if it's a small dot or a full oval
                pts = stroke.points
                if pts:
                    xs = [p.x for p in pts]
                    ys = [p.y for p in pts]
                    w = max(xs) - min(xs)
                    h = max(ys) - min(ys)
                    if w < 8 and h < 8:
                        # Small enough to be a dot — fill solid
                        parts.append(self._expand_dot(stroke))
                    else:
                        parts.append(self._expand_closed_stroke(stroke))
                        
            else:
                parts.append(self._expand_open_stroke(stroke))
        
        return " ".join(p for p in parts if p)
