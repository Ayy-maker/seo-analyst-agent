"""
Visualization utilities for generating charts and graphics
Phase 4: Enhanced with time-series, trends, and comparisons
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import matplotlib.dates as mdates
from datetime import datetime, date
import io
from typing import List, Dict, Tuple, Optional
import numpy as np


class ChartGenerator:
    """Generate beautiful charts for PDF reports"""
    
    # Professional color palette inspired by the HTML design
    COLORS = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'success': '#48bb78',
        'warning': '#f39c12',
        'danger': '#dc2626',
        'gray': '#718096',
        'light_gray': '#e2e8f0'
    }
    
    @staticmethod
    def create_kpi_chart(metrics: List[Dict], figsize=(14, 3.5)):
        """
        Create stunning KPI dashboard with gradient boxes and shadows
        
        Args:
            metrics: List of dicts with 'label', 'value', 'trend', 'trend_text'
            figsize: Figure size tuple
        
        Returns:
            BytesIO object containing PNG image
        """
        fig, axes = plt.subplots(1, len(metrics), figsize=figsize)
        fig.patch.set_facecolor('white')
        
        # Beautiful gradient colors
        gradient_colors = [
            [(0.28, 0.74, 0.47), (0.20, 0.64, 0.37)],  # Green gradient
            [(0.40, 0.49, 0.92), (0.46, 0.29, 0.64)],  # Blue-purple gradient
            [(0.95, 0.61, 0.07), (0.95, 0.71, 0.17)],  # Orange gradient
            [(0.46, 0.29, 0.64), (0.60, 0.35, 0.70)]   # Purple gradient
        ]
        
        for idx, (ax, metric) in enumerate(zip(axes if len(metrics) > 1 else [axes], metrics)):
            ax.axis('off')
            
            # Create gradient background with multiple layers for depth
            for i in range(3):
                alpha_val = 0.15 - (i * 0.03)
                offset = i * 0.02
                gradient = gradient_colors[idx % len(gradient_colors)]
                
                box = FancyBboxPatch(
                    (0.08 - offset, 0.15 - offset), 0.84 + (offset*2), 0.7 + (offset*2),
                    boxstyle="round,pad=0.08",
                    edgecolor='none',
                    facecolor=gradient[0],
                    linewidth=0,
                    alpha=alpha_val,
                    zorder=1-i
                )
                ax.add_patch(box)
            
            # Main card with gradient border
            main_box = FancyBboxPatch(
                (0.08, 0.15), 0.84, 0.7,
                boxstyle="round,pad=0.08",
                edgecolor=gradient_colors[idx % len(gradient_colors)][0],
                facecolor='white',
                linewidth=4,
                alpha=1.0,
                zorder=5
            )
            ax.add_patch(main_box)
            
            # Icon/emoji background circle
            circle = plt.Circle((0.5, 0.75), 0.08, 
                              color=gradient_colors[idx % len(gradient_colors)][0],
                              alpha=0.15, zorder=6)
            ax.add_patch(circle)
            
            # Label
            ax.text(0.5, 0.65, metric['label'].upper(), 
                   ha='center', va='center', fontsize=9,
                   color=ChartGenerator.COLORS['gray'], 
                   fontweight='700',
                   zorder=7)
            
            # Large value with gradient effect (simulate with color)
            value_color = gradient_colors[idx % len(gradient_colors)][0]
            ax.text(0.5, 0.45, str(metric['value']),
                   ha='center', va='center', fontsize=32,
                   color=value_color, fontweight='900',
                   zorder=7)
            
            # Trend indicator with background
            trend_color = ChartGenerator.COLORS['success'] if metric.get('trend', 0) >= 0 else ChartGenerator.COLORS['danger']
            arrow = '↗' if metric.get('trend', 0) >= 0 else '↘'
            
            # Trend background
            trend_box = FancyBboxPatch(
                (0.15, 0.22), 0.7, 0.12,
                boxstyle="round,pad=0.02",
                edgecolor='none',
                facecolor=trend_color,
                alpha=0.1,
                zorder=6
            )
            ax.add_patch(trend_box)
            
            ax.text(0.5, 0.28, f"{arrow} {metric.get('trend_text', '')}",
                   ha='center', va='center', fontsize=10,
                   color=trend_color, fontweight='700',
                   zorder=7)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        
        plt.tight_layout(pad=1.5)
        
        # Save to buffer with high DPI
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_trend_chart(data: List[Tuple[str, float]], 
                          title: str = "Trend Over Time",
                          figsize=(10, 4),
                          color='primary'):
        """
        Create line chart with gradient fill
        
        Args:
            data: List of (label, value) tuples
            title: Chart title
            figsize: Figure size
            color: Color key from COLORS dict
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        
        labels, values = zip(*data) if data else ([], [])
        x = np.arange(len(labels))
        
        # Plot line
        line_color = ChartGenerator.COLORS.get(color, ChartGenerator.COLORS['primary'])
        ax.plot(x, values, color=line_color, linewidth=3, marker='o', 
                markersize=8, markerfacecolor='white', markeredgewidth=2)
        
        # Fill gradient
        ax.fill_between(x, values, alpha=0.3, color=line_color)
        
        # Styling
        ax.set_title(title, fontsize=16, fontweight='700', pad=20, 
                    color=ChartGenerator.COLORS['gray'])
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines('right').set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_device_chart(data: Dict[str, float], figsize=(7, 7)):
        """
        Create beautiful donut chart for device distribution
        
        Args:
            data: Dict of device: percentage
            figsize: Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        
        labels = list(data.keys())
        sizes = list(data.values())
        
        # Beautiful colors
        colors = [(0.40, 0.49, 0.92), (0.46, 0.29, 0.64), (0.95, 0.61, 0.07)]
        
        # Create donut with shadow effect
        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, colors=colors,
            autopct='%1.1f%%', startangle=90,
            pctdistance=0.85, 
            textprops={'fontsize': 13, 'fontweight': '700', 'color': 'white'},
            wedgeprops={'linewidth': 3, 'edgecolor': 'white'}
        )
        
        # Draw circle for donut effect with gradient
        centre_circle = plt.Circle((0, 0), 0.65, fc='white', linewidth=0)
        ax.add_artist(centre_circle)
        
        # Center text
        ax.text(0, 0.05, 'Device\nDistribution', ha='center', va='center',
               fontsize=16, fontweight='800', color=ChartGenerator.COLORS['gray'],
               linespacing=1.5)
        
        # Legend with percentages
        legend_labels = [f'{label}: {size:.1f}%' for label, size in zip(labels, sizes)]
        ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                 frameon=False, fontsize=11, labelspacing=1.2)
        
        ax.axis('equal')
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_comparison_chart(before: Dict, after: Dict, 
                               title: str = "Performance Comparison",
                               figsize=(10, 6)):
        """
        Create side-by-side bar chart for before/after comparison
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        
        metrics = list(before.keys())
        before_vals = list(before.values())
        after_vals = list(after.values())
        
        x = np.arange(len(metrics))
        width = 0.35
        
        # Bars
        bars1 = ax.bar(x - width/2, before_vals, width, label='Before',
                      color=ChartGenerator.COLORS['light_gray'], alpha=0.8)
        bars2 = ax.bar(x + width/2, after_vals, width, label='After',
                      color=ChartGenerator.COLORS['success'], alpha=0.9)
        
        # Styling
        ax.set_title(title, fontsize=16, fontweight='700', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=45, ha='right')
        ax.legend(frameon=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_progress_gauge(value: float, max_value: float = 100,
                             label: str = "Score", figsize=(7, 5)):
        """
        Create stunning gauge/speedometer chart for health scores
        
        Args:
            value: Current value
            max_value: Maximum value
            label: Label for the gauge
        """
        fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': 'polar'})
        fig.patch.set_facecolor('white')
        
        # Calculate angle
        percentage = value / max_value
        angle = percentage * np.pi
        
        # Draw gauge background with gradients
        theta = np.linspace(0, np.pi, 200)
        radii = np.ones_like(theta)
        
        # Beautiful color zones with gradients
        colors_zones = [
            (0, 0.4, '#dc2626', 'Poor'),
            (0.4, 0.6, '#f39c12', 'Fair'),
            (0.6, 0.8, '#48bb78', 'Good'),
            (0.8, 1.0, '#10b981', 'Excellent')
        ]
        
        # Draw background track
        ax.plot(theta, radii, color='#e2e8f0', linewidth=30, alpha=0.3, zorder=1)
        
        # Draw colored zones
        for start, end, color, zone_label in colors_zones:
            mask = (theta >= start * np.pi) & (theta <= end * np.pi)
            ax.plot(theta[mask], radii[mask], color=color, linewidth=30, alpha=0.8, zorder=2)
        
        # Determine current zone color
        if percentage < 0.4:
            needle_color = '#dc2626'
            status = 'Needs Work'
        elif percentage < 0.6:
            needle_color = '#f39c12'
            status = 'Fair'
        elif percentage < 0.8:
            needle_color = '#48bb78'
            status = 'Good'
        else:
            needle_color = '#10b981'
            status = 'Excellent'
        
        # Draw progress arc (filled portion)
        progress_theta = np.linspace(0, angle, 100)
        progress_radii = np.ones_like(progress_theta) * 1.05
        ax.plot(progress_theta, progress_radii, color=needle_color, 
               linewidth=35, alpha=0.9, zorder=3, solid_capstyle='round')
        
        # Draw needle with glow effect
        for i, alpha_val in enumerate([0.1, 0.2, 0.4, 0.7, 1.0]):
            width = 8 - i
            ax.plot([angle, angle], [0, 0.85], color=needle_color,
                   linewidth=width, alpha=alpha_val, zorder=4+i, solid_capstyle='round')
        
        # Needle cap (circle at center)
        center_circle = plt.Circle((0, 0), 0.08, color='white', 
                                  transform=ax.transData._b, zorder=10)
        ax.add_patch(center_circle)
        
        center_dot = plt.Circle((0, 0), 0.05, color=needle_color,
                               transform=ax.transData._b, zorder=11)
        ax.add_patch(center_dot)
        
        # Styling
        ax.set_ylim(0, 1.3)
        ax.set_theta_zero_location('W')
        ax.set_theta_direction(1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['polar'].set_visible(False)
        ax.grid(False)
        
        # Add value text with background
        ax.text(np.pi/2, -0.25, f"{int(value)}",
               ha='center', va='center', fontsize=52, fontweight='900',
               color=needle_color, zorder=15)
        
        ax.text(np.pi/2, -0.45, f"out of {int(max_value)}",
               ha='center', va='center', fontsize=12, 
               color=ChartGenerator.COLORS['gray'], fontweight='600', zorder=15)
        
        ax.text(np.pi/2, -0.6, status,
               ha='center', va='center', fontsize=16, fontweight='700',
               color=needle_color, zorder=15)
        
        ax.text(np.pi/2, -0.75, label,
               ha='center', va='center', fontsize=14, 
               color=ChartGenerator.COLORS['gray'], fontweight='600', zorder=15)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    # ==================== PHASE 4: ADVANCED VISUALIZATIONS ====================
    
    @staticmethod
    def create_time_series_chart(data: List[Dict], metric_name: str, 
                                 title: str = None, figsize=(12, 4)):
        """
        Create beautiful time-series chart with trend line
        
        Args:
            data: List of dicts with 'date' and 'value' keys
            metric_name: Name of the metric
            title: Chart title
        
        Returns:
            BytesIO object containing PNG image
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f7fafc')
        
        # Parse dates and values
        dates = [datetime.fromisoformat(d['date']) if isinstance(d['date'], str) 
                else d['date'] for d in data]
        values = [d['value'] for d in data]
        
        # Plot main line with gradient effect
        ax.plot(dates, values, linewidth=3, color=ChartGenerator.COLORS['primary'],
               marker='o', markersize=6, markerfacecolor='white', 
               markeredgewidth=2, markeredgecolor=ChartGenerator.COLORS['primary'],
               label='Actual', zorder=3)
        
        # Add area under curve
        ax.fill_between(dates, values, alpha=0.2, 
                        color=ChartGenerator.COLORS['primary'])
        
        # Calculate and plot trend line
        if len(dates) > 2:
            x_numeric = np.arange(len(dates))
            z = np.polyfit(x_numeric, values, 1)
            p = np.poly1d(z)
            ax.plot(dates, p(x_numeric), "--", linewidth=2, 
                   color=ChartGenerator.COLORS['secondary'],
                   alpha=0.7, label='Trend', zorder=2)
        
        # Styling
        ax.set_title(title or f'{metric_name} Over Time', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Date', fontsize=11, fontweight='600')
        ax.set_ylabel(metric_name, fontsize=11, fontweight='600')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on points
        for i, (dt, val) in enumerate(zip(dates, values)):
            if i % max(1, len(dates) // 6) == 0:  # Show every nth label
                ax.text(dt, val, f'{val:.0f}', 
                       ha='center', va='bottom', fontsize=8,
                       fontweight='600', color=ChartGenerator.COLORS['gray'])
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_comparison_chart(current: Dict, previous: Dict, 
                               metrics: List[str], figsize=(10, 5)):
        """
        Create side-by-side comparison chart
        
        Args:
            current: Dict with current period metrics
            previous: Dict with previous period metrics
            metrics: List of metric names to compare
        
        Returns:
            BytesIO object containing PNG image
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        
        x = np.arange(len(metrics))
        width = 0.35
        
        current_values = [current.get(m, 0) for m in metrics]
        previous_values = [previous.get(m, 0) for m in metrics]
        
        # Create bars
        bars1 = ax.bar(x - width/2, previous_values, width, 
                       label='Previous Period',
                       color=ChartGenerator.COLORS['light_gray'],
                       edgecolor=ChartGenerator.COLORS['gray'],
                       linewidth=1.5)
        
        bars2 = ax.bar(x + width/2, current_values, width,
                       label='Current Period',
                       color=ChartGenerator.COLORS['primary'],
                       edgecolor=ChartGenerator.COLORS['secondary'],
                       linewidth=1.5)
        
        # Add value labels on bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='600')
        
        add_labels(bars1)
        add_labels(bars2)
        
        # Styling
        ax.set_title('Performance Comparison', fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel('Value', fontsize=11, fontweight='600')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontsize=10)
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_forecast_chart(historical: List[Dict], forecast: List[Dict],
                             metric_name: str, figsize=(12, 5)):
        """
        Create chart showing historical data + forecast with confidence intervals
        
        Args:
            historical: List of dicts with 'date' and 'value'
            forecast: List of dicts with 'date', 'predicted_value', 'confidence_low', 'confidence_high'
            metric_name: Name of metric
        
        Returns:
            BytesIO object containing PNG image
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f7fafc')
        
        # Parse historical data
        hist_dates = [datetime.fromisoformat(d['date']) if isinstance(d['date'], str) 
                     else d['date'] for d in historical]
        hist_values = [d['value'] for d in historical]
        
        # Parse forecast data
        fc_dates = [datetime.fromisoformat(d['date']) if isinstance(d['date'], str)
                   else d['date'] for d in forecast]
        fc_values = [d['predicted_value'] for d in forecast]
        fc_low = [d.get('confidence_low', d['predicted_value']) for d in forecast]
        fc_high = [d.get('confidence_high', d['predicted_value']) for d in forecast]
        
        # Plot historical data
        ax.plot(hist_dates, hist_values, linewidth=3, 
               color=ChartGenerator.COLORS['primary'],
               marker='o', markersize=5, label='Historical', zorder=3)
        
        # Plot forecast
        ax.plot(fc_dates, fc_values, linewidth=3, linestyle='--',
               color=ChartGenerator.COLORS['secondary'],
               marker='s', markersize=5, label='Forecast', zorder=3)
        
        # Plot confidence interval
        ax.fill_between(fc_dates, fc_low, fc_high, 
                        alpha=0.2, color=ChartGenerator.COLORS['secondary'],
                        label='95% Confidence')
        
        # Add vertical line at forecast start
        if hist_dates and fc_dates:
            ax.axvline(x=hist_dates[-1], color=ChartGenerator.COLORS['gray'],
                      linestyle=':', linewidth=2, alpha=0.5)
        
        # Styling
        ax.set_title(f'{metric_name} - Historical & Forecast', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Date', fontsize=11, fontweight='600')
        ax.set_ylabel(metric_name, fontsize=11, fontweight='600')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Format dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_multi_metric_chart(metrics_data: Dict[str, List[Dict]], 
                                  figsize=(12, 6)):
        """
        Create chart with multiple metrics on same timeline
        
        Args:
            metrics_data: Dict of metric_name -> list of {date, value} dicts
            figsize: Figure size
        
        Returns:
            BytesIO object containing PNG image
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f7fafc')
        
        colors = [ChartGenerator.COLORS['primary'], 
                 ChartGenerator.COLORS['success'],
                 ChartGenerator.COLORS['warning'],
                 ChartGenerator.COLORS['secondary']]
        
        for idx, (metric_name, data) in enumerate(metrics_data.items()):
            dates = [datetime.fromisoformat(d['date']) if isinstance(d['date'], str) 
                    else d['date'] for d in data]
            values = [d['value'] for d in data]
            
            color = colors[idx % len(colors)]
            ax.plot(dates, values, linewidth=2.5, color=color,
                   marker='o', markersize=4, label=metric_name, zorder=3)
        
        # Styling
        ax.set_title('Multiple Metrics Trend', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Date', fontsize=11, fontweight='600')
        ax.set_ylabel('Value', fontsize=11, fontweight='600')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Format dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return buf
