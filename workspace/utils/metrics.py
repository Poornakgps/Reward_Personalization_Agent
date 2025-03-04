"""
Utilities for tracking and reporting metrics.
"""
from typing import Dict, Any, List, Optional
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

class MetricsTracker:
    """Utility for tracking and reporting metrics."""
    
    def __init__(self):
        self.metrics = {}
        logger.info("MetricsTracker initialized")
    
    def track(self, metric_name: str, value: Any, 
             tags: Optional[Dict[str, str]] = None) -> None:
        """
        Track a metric value.
        
        Args:
            metric_name: Name of the metric to track
            value: Value of the metric
            tags: Optional dictionary of tags to associate with the metric
        """
        if tags is None:
            tags = {}
            
        logger.debug(f"Tracking metric {metric_name}: {value} with tags {tags}")
        
        # In a real implementation, would send to a metrics service
        
        # Store locally for reporting
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
            
        self.metrics[metric_name].append({
            "value": value,
            "tags": tags,
            "timestamp": "2023-06-15T10:30:00Z"  # Would use actual timestamp
        })
    
    def get_report(self, 
                  metric_names: Optional[List[str]] = None, 
                  tags_filter: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generate a report of tracked metrics.
        
        Args:
            metric_names: Optional list of metric names to include
            tags_filter: Optional dictionary of tags to filter by
            
        Returns:
            Dictionary with metric reports
        """
        logger.info(f"Generating metrics report for {metric_names}")
        
        # Filter metrics by name if specified
        if metric_names is None:
            metrics_to_report = self.metrics
        else:
            metrics_to_report = {
                name: values for name, values in self.metrics.items() 
                if name in metric_names
            }
            
        # Apply tags filter if specified
        if tags_filter is not None:
            for name, values in metrics_to_report.items():
                metrics_to_report[name] = [
                    v for v in values if all(
                        v.get("tags", {}).get(tag_key) == tag_value 
                        for tag_key, tag_value in tags_filter.items()
                    )
                ]
                
        # Calculate basic statistics for each metric
        report = {}
        for name, values in metrics_to_report.items():
            if not values:
                continue
                
            numeric_values = [v["value"] for v in values if isinstance(v["value"], (int, float))]
            
            if numeric_values:
                report[name] = {
                    "count": len(numeric_values),
                    "sum": sum(numeric_values),
                    "mean": sum(numeric_values) / len(numeric_values) if numeric_values else None,
                    "min": min(numeric_values) if numeric_values else None,
                    "max": max(numeric_values) if numeric_values else None
                }
            else:
                report[name] = {
                    "count": len(values),
                    "values": [v["value"] for v in values]
                }
                
        return report
