"""
Forecasting Module - Predict future SEO metrics
Uses statistical models and machine learning for traffic/ranking forecasting
"""

from datetime import date, timedelta
from typing import Dict, List, Tuple
from statistics import mean
import math


class Forecaster:
    """Forecast SEO metrics using statistical models"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    # ==================== LINEAR FORECASTING ====================
    
    def forecast_linear(self, client_id: int, metric_name: str, 
                       days_ahead: int = 90) -> Dict:
        """Simple linear regression forecast"""
        # Get historical data (last 6 months)
        trend_data = self.db.get_metric_trend(client_id, metric_name, months=6)
        
        if len(trend_data) < 3:
            return {"error": "Insufficient data for forecasting"}
        
        # Prepare data
        values = [d['metric_value'] for d in trend_data]
        n = len(values)
        x = list(range(n))
        
        # Calculate linear regression
        x_mean = mean(x)
        y_mean = mean(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return {"error": "Cannot calculate trend"}
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Calculate R-squared for confidence
        y_pred = [slope * x[i] + intercept for i in range(n)]
        ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
        ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Calculate standard error for confidence intervals
        mse = ss_res / (n - 2) if n > 2 else 0
        std_error = math.sqrt(mse)
        
        # Generate forecasts
        forecasts = []
        last_date = date.fromisoformat(trend_data[-1]['metric_date'])
        
        for day in range(1, days_ahead + 1):
            x_forecast = n + day - 1
            predicted = slope * x_forecast + intercept
            
            # 95% confidence interval (±1.96 * std_error)
            margin = 1.96 * std_error * math.sqrt(1 + 1/n + (x_forecast - x_mean)**2 / denominator)
            
            forecast_date = last_date + timedelta(days=day)
            
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_value': max(0, round(predicted, 2)),
                'confidence_low': max(0, round(predicted - margin, 2)),
                'confidence_high': round(predicted + margin, 2),
                'model_type': 'linear'
            })
        
        # Save forecasts to database
        self.db.save_forecast(client_id, metric_name, forecasts)
        
        return {
            'metric': metric_name,
            'model': 'linear_regression',
            'r_squared': round(r_squared, 3),
            'confidence': 'high' if r_squared > 0.7 else 'medium' if r_squared > 0.4 else 'low',
            'slope': round(slope, 4),
            'trend': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
            'forecasts': forecasts[:30],  # Return first 30 days
            'total_forecasts': len(forecasts)
        }
    
    # ==================== MOVING AVERAGE FORECASTING ====================
    
    def forecast_moving_average(self, client_id: int, metric_name: str, 
                               window: int = 7, days_ahead: int = 30) -> Dict:
        """Moving average forecast (good for short-term)"""
        trend_data = self.db.get_metric_trend(client_id, metric_name, months=6)
        
        if len(trend_data) < window:
            return {"error": f"Need at least {window} data points"}
        
        values = [d['metric_value'] for d in trend_data]
        
        # Calculate moving average
        ma_values = []
        for i in range(len(values) - window + 1):
            ma = mean(values[i:i + window])
            ma_values.append(ma)
        
        # Use last MA value as baseline forecast
        last_ma = ma_values[-1]
        last_date = date.fromisoformat(trend_data[-1]['metric_date'])
        
        # Calculate variability for confidence intervals
        recent_std = self._calculate_std(values[-window:])
        
        forecasts = []
        for day in range(1, days_ahead + 1):
            forecast_date = last_date + timedelta(days=day)
            
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_value': round(last_ma, 2),
                'confidence_low': max(0, round(last_ma - 1.96 * recent_std, 2)),
                'confidence_high': round(last_ma + 1.96 * recent_std, 2),
                'model_type': 'moving_average'
            })
        
        return {
            'metric': metric_name,
            'model': 'moving_average',
            'window_size': window,
            'baseline_value': round(last_ma, 2),
            'forecasts': forecasts
        }
    
    # ==================== KEYWORD POSITION FORECASTING ====================
    
    def forecast_keyword_position(self, client_id: int, keyword: str, 
                                  days_ahead: int = 30) -> Dict:
        """Forecast keyword ranking position"""
        history = self.db.get_keyword_history(client_id, keyword)
        
        if len(history) < 5:
            return {"error": "Insufficient keyword history"}
        
        positions = [h['position'] for h in history if h['position']]
        
        if not positions:
            return {"error": "No position data available"}
        
        # Use exponential smoothing (good for ranking data)
        alpha = 0.3  # Smoothing factor
        forecast = positions[-1]
        
        # Calculate trend
        trend_data = self._calculate_trend(positions[-10:] if len(positions) > 10 else positions)
        
        forecasts = []
        last_date = date.fromisoformat(history[-1]['date'])
        
        for day in range(1, days_ahead + 1):
            # Apply trend to forecast
            forecast = max(1, min(100, forecast + trend_data['daily_change']))
            forecast_date = last_date + timedelta(days=day)
            
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_position': round(forecast, 1),
                'confidence': 'medium'
            })
        
        return {
            'keyword': keyword,
            'current_position': positions[-1],
            'forecasted_position_30d': forecasts[29]['predicted_position'] if len(forecasts) >= 30 else None,
            'expected_change': forecasts[29]['predicted_position'] - positions[-1] if len(forecasts) >= 30 else 0,
            'trend': trend_data['direction'],
            'forecasts': forecasts
        }
    
    # ==================== TRAFFIC FORECASTING ====================
    
    def forecast_traffic(self, client_id: int, days_ahead: int = 90) -> Dict:
        """Forecast organic traffic"""
        traffic_trend = self.db.get_traffic_trend(client_id, days=90)
        
        if len(traffic_trend) < 7:
            return {"error": "Insufficient traffic data"}
        
        sessions = [t['total_sessions'] for t in traffic_trend]
        
        # Detect seasonality (weekly pattern)
        weekly_pattern = self._detect_weekly_pattern(sessions)
        
        # Calculate base trend
        n = len(sessions)
        x = list(range(n))
        x_mean = mean(x)
        y_mean = mean(sessions)
        
        numerator = sum((x[i] - x_mean) * (sessions[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # Generate forecasts with seasonality
        forecasts = []
        last_date = date.fromisoformat(traffic_trend[-1]['date'])
        
        for day in range(1, days_ahead + 1):
            x_forecast = n + day - 1
            base_forecast = slope * x_forecast + intercept
            
            # Apply weekly seasonality
            day_of_week = (last_date + timedelta(days=day)).weekday()
            seasonal_factor = weekly_pattern.get(day_of_week, 1.0)
            
            adjusted_forecast = base_forecast * seasonal_factor
            
            forecast_date = last_date + timedelta(days=day)
            
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_sessions': max(0, round(adjusted_forecast)),
                'model_type': 'seasonal_linear'
            })
        
        # Calculate growth rate
        if len(forecasts) >= 30:
            current_avg = mean(sessions[-7:])
            forecast_avg = mean(f['predicted_sessions'] for f in forecasts[:30])
            growth_rate = ((forecast_avg - current_avg) / current_avg * 100) if current_avg != 0 else 0
        else:
            growth_rate = 0
        
        return {
            'current_daily_avg': round(mean(sessions[-7:]), 0),
            'forecasted_daily_avg_30d': round(mean(f['predicted_sessions'] for f in forecasts[:30]), 0) if len(forecasts) >= 30 else 0,
            'expected_growth_rate': round(growth_rate, 2),
            'trend': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
            'seasonality_detected': len(weekly_pattern) > 0,
            'forecasts': forecasts[:30]
        }
    
    # ==================== HELPER METHODS ====================
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0
        
        avg = mean(values)
        variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)
    
    def _calculate_trend(self, values: List[float]) -> Dict:
        """Calculate trend information"""
        if len(values) < 2:
            return {'direction': 'unknown', 'daily_change': 0}
        
        # Simple difference
        total_change = values[-1] - values[0]
        daily_change = total_change / len(values)
        
        direction = 'up' if total_change > 0 else 'down' if total_change < 0 else 'flat'
        
        return {
            'direction': direction,
            'daily_change': daily_change,
            'total_change': total_change
        }
    
    def _detect_weekly_pattern(self, values: List[float]) -> Dict[int, float]:
        """Detect day-of-week seasonality"""
        if len(values) < 14:  # Need at least 2 weeks
            return {}
        
        # Group by day of week
        by_day = {i: [] for i in range(7)}
        
        for idx, value in enumerate(values):
            day_of_week = idx % 7
            by_day[day_of_week].append(value)
        
        # Calculate average for each day
        overall_avg = mean(values)
        pattern = {}
        
        for day, day_values in by_day.items():
            if day_values:
                day_avg = mean(day_values)
                pattern[day] = day_avg / overall_avg if overall_avg != 0 else 1.0
        
        return pattern
    
    # ==================== BATCH FORECASTING ====================
    
    def forecast_all_metrics(self, client_id: int, days_ahead: int = 90) -> Dict:
        """Generate forecasts for all tracked metrics"""
        metrics = self.db.get_metrics(client_id)
        metric_names = set(m['metric_name'] for m in metrics)
        
        forecasts = {}
        
        for metric_name in metric_names:
            try:
                forecast = self.forecast_linear(client_id, metric_name, days_ahead)
                if 'error' not in forecast:
                    forecasts[metric_name] = forecast
            except Exception as e:
                forecasts[metric_name] = {'error': str(e)}
        
        # Add traffic forecast
        try:
            traffic_forecast = self.forecast_traffic(client_id, days_ahead)
            if 'error' not in traffic_forecast:
                forecasts['organic_traffic'] = traffic_forecast
        except Exception:
            pass
        
        return {
            'client_id': client_id,
            'forecasts': forecasts,
            'total_metrics': len(forecasts),
            'generated_at': date.today().isoformat()
        }
